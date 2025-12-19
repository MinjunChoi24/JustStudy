import os
import time
import kagglehub
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from xgboost import XGBClassifier

# ==========================================
# 0. 설정 및 상수 정의 (Configuration)
# ==========================================
MODEL_SAVE_DIR = "../saved_models"
if not os.path.exists(MODEL_SAVE_DIR):
    os.makedirs(MODEL_SAVE_DIR)


def load_and_preprocess_data():
    """데이터 다운로드, 병합, 전처리 및 밸런싱을 수행합니다."""
    print("=" * 50)
    print("📥 1. 데이터셋 다운로드 및 로딩 중...")

    # Kaggle 데이터셋 다운로드
    path_news = kagglehub.dataset_download("ankurzing/sentiment-analysis-for-financial-news")
    df_news = pd.read_csv(f"{path_news}/all-data.csv", encoding='latin1', header=None, names=['Sentiment', 'Text'])

    path_tweets = kagglehub.dataset_download("yash612/stockmarket-sentiment-dataset")
    df_tweets = pd.read_csv(f"{path_tweets}/stock_data.csv")

    # 전처리
    tweet_map = {-1: 'negative', 1: 'positive'}
    df_tweets['Sentiment'] = df_tweets['Sentiment'].map(tweet_map)
    df_tweets = df_tweets[['Text', 'Sentiment']]

    # 병합
    print("\n🔗 데이터 병합 중...")
    df_total = pd.concat([df_tweets, df_news], ignore_index=True)
    df_total.dropna(subset=['Text', 'Sentiment'], inplace=True)

    # 1. 충돌 라벨 제거
    conflict_mask = df_total.groupby("Text")["Sentiment"].nunique() > 1
    conflict_texts = conflict_mask[conflict_mask].index
    df_total = df_total[~df_total["Text"].isin(conflict_texts)]

    # 2. 나머지 중복 제거
    df_total = df_total.drop_duplicates(subset='Text')

    # 라벨 인코딩
    print("🔢 라벨 인코딩 변환...")
    label_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
    df_total['Sentiment_Encoded'] = df_total['Sentiment'].map(label_mapping)

    # Train / Test 분리 (Stratify)
    X = df_total['Text']
    y = df_total['Sentiment_Encoded']

    X_train_raw, X_test_raw, y_train_raw, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"✂️ 데이터 분리 완료 (Train: {len(X_train_raw)}, Test: {len(X_test_raw)})")

    return X_train_raw, y_train_raw, X_test_raw, y_test


def vectorize_text(X_train, X_test):
    """TF-IDF 벡터화를 수행합니다."""
    print("\n" + "=" * 50)
    print("⚡ 2. TF-IDF 벡터화 수행 중...")

    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=3,
        stop_words=None
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print(f"   -> 생성된 Feature 개수: {X_train_vec.shape[1]}")
    return X_train_vec, X_test_vec, vectorizer


def train_and_evaluate(model, name, X_train, y_train, X_test, y_test):
    """모델을 학습하고 평가 결과를 출력하는 공통 함수입니다."""
    print("\n" + "-" * 50)
    print(f"🚀 [{name}] 학습 및 평가 시작...")

    if name == "XGBoost":
        print("   -> Early Stopping 적용 중...")
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        print(f"   -> 최적의 트리 개수(Best Iteration): {model.best_iteration}")
    else:
        model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"   -> 정확도(Accuracy): {acc:.4f}")
    print("\n[Classification Report]")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Neutral', 'Positive']))

    print(f"📊 [{name}] 혼동행렬 출력 중...")
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Neutral', 'Positive'])
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f"{name} Confusion Matrix")
    plt.show()

    return model, acc


def run_svm_grid_search(X_train, y_train, X_test, y_test):
    """SVM GridSearch 수행 (가장 성능이 좋았던 모델)"""
    print("\n" + "=" * 50)
    print("🔎 4. SVM GridSearch (하이퍼파라미터 튜닝) 수행 중...")

    param_grid = {
        'C': [0.1, 0.5, 1, 5, 10, 50],
        'class_weight': [None, 'balanced']
    }

    base_svm = LinearSVC(random_state=42, dual=False, max_iter=3000)
    grid = GridSearchCV(base_svm, param_grid, cv=5, scoring='f1_macro', n_jobs=-1, verbose=1)

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test)

    print("\n🏆 [SVM 최종 튜닝 결과]")
    print(f"   -> Best Parameters: {grid.best_params_}")
    print(f"   -> 최종 정확도: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Neutral', 'Positive']))

    print("📊 [Best SVM] 혼동행렬 출력 중...")
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=['Negative', 'Neutral', 'Positive'])
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Best SVM Confusion Matrix")
    plt.show()

    return grid, best_model


# ==========================================
# 메인 실행 블록
# ==========================================
if __name__ == "__main__":
    # 1. 데이터 로드 및 전처리
    X_train_text, y_train, X_test_text, y_test = load_and_preprocess_data()

    # 2. 벡터화
    X_train_vec, X_test_vec, vectorizer = vectorize_text(X_train_text, X_test_text)

    # ---------------------------------------------------------
    # [추가된 부분] 3. 튜닝 전 Baseline SVM 평가
    # ---------------------------------------------------------
    print("\n" + "=" * 50)
    print("🏁 3. Baseline SVM (튜닝 전) 성능 평가")

    # 기본값 SVM (dual=False는 샘플 수가 많을 때 권장됨, max_iter는 수렴 경고 방지용)
    baseline_svm = LinearSVC(random_state=42, dual=False, max_iter=3000)

    train_and_evaluate(
        baseline_svm,
        "Baseline SVM (No Tuning)",
        X_train_vec, y_train, X_test_vec, y_test
    )
    # ---------------------------------------------------------

    # 4. SVM 메인 모델 학습 (GridSearch)
    svm_grid, best_svm = run_svm_grid_search(X_train_vec, y_train, X_test_vec, y_test)

    # 5. 모델 저장 (로컬 경로)
    print("\n💾 모델 저장 중...")
    joblib.dump(svm_grid, os.path.join(MODEL_SAVE_DIR, 'my_svm_model.pkl'))
    joblib.dump(vectorizer, os.path.join(MODEL_SAVE_DIR, 'my_tfidf_vectorizer.pkl'))
    print(f"   -> 저장 위치: {os.path.abspath(MODEL_SAVE_DIR)}")

    # 6. 비교용 다른 모델들 실행 (XGBoost 등)
    print("\n" + "=" * 50)
    print("🏁 5. 다른 알고리즘과 비교 평가")

    models = {
        "XGBoost": XGBClassifier(
            n_estimators=1000,
            learning_rate=0.05,
            max_depth=6,
            random_state=42,
            n_jobs=-1,
            eval_metric='mlogloss',
            early_stopping_rounds=50)
    }

    results = {}
    for name, model in models.items():
        _, acc = train_and_evaluate(model, name, X_train_vec, y_train, X_test_vec, y_test)
        results[name] = acc

    print("\n📊 [최종 모델별 정확도 순위]")
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for name, score in sorted_results:
        print(f"{name}: {score:.4f}")
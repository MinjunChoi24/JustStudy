from scraper import get_news
from classifier import analyze_article
from uploader import save_to_notion
from dotenv import load_dotenv

load_dotenv() # .env 파일 로드

if __name__ == "__main__":
    print("🚀 뉴스 수집 시작...")
    news_list = get_news() # 1. 수집

    for news in news_list:
        print(f"Processing: {news['title']}")
        ai_data = analyze_article(news) # 2. AI 분석
        save_to_notion(news, ai_data)   # 3. 노션 저장
from scraper import get_news_data
from classifier import analyze_article
from uploader import save_to_notion

def main():
    print("🚀 뉴스 수집 및 아카이빙 시스템 가동!")
    
    # 1. 뉴스 수집 
    print("\n[1단계] 네이버 뉴스 긁어오는 중...")
    
    news_list = get_news_data()
    
    print(f"--> 총 {len(news_list)}개의 기사를 찾았습니다.")

    # 2. 하나씩 AI 분석 후 노션 저장
    print("\n[2단계] AI 분석 및 노션 저장 시작...")
    

    for i, news in enumerate(news_list):
        print(f"\n[{i+1}/{len(news_list)}] 처리 중: {news['Title']}...")
        
        # AI 분석
        ai_result = analyze_article(news)
        
        # 결과 출력 (확인용)
        print(f"   ㄴ 분류: {ai_result.get('Category')} | 주제: {ai_result.get('Subject')} | {ai_result.get('Sector')}")
        
        # 노션 저장
        save_to_notion(news, ai_result)

    print("\n✨ 모든 작업이 완료되었습니다! 노션을 확인해보세요.")

if __name__ == "__main__":
    main()
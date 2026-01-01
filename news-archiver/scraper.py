import requests
import urllib.parse
import os
import time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def naver_news_api(query="", display=35):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    encoded_query = urllib.parse.quote(query)
    # sort=date로 변경하면 최신순 수집 가능 (현재는 sim: 정확도순)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display={display}&sort=date"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        news_list = []
        for item in data.get('items', []):
            title = item['title'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
            description = item['description'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
            
            # 불필요한 키워드 필터링
            if any(keyword in title for keyword in ["[인사]", "[부고]", "[포토]", "인사", "부고", "포토"]):
                continue

            clean_date = datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %z").isoformat()
            
            news_list.append({
                "Title": title,
                "Date": clean_date,
                "Summary": description,
                "URL": item['originallink'] or item['link'],
                "Keyword": query  # 어떤 키워드로 검색했는지 추적하기 위해 추가
            })
            
        return news_list
    
    except Exception as e:
        print(f"❌ 네이버 API 호출 중 오류 발생 ({query}): {e}")
        return []

# 2. [핵심] 여러 키워드를 통합 수집하여 반환하는 메인 함수
def get_news_data():
    # 수집하고 싶은 키워드 리스트
    keywords = ["금리", "환율", "증시"]
    
    all_news_data = []
    print(f"🔍 총 {len(keywords)}개의 키워드로 뉴스 수집을 시작합니다...")

    # 키워드별 반복 수집
    for keyword in keywords:
        # print(f" -> '{keyword}' 수집 중...")  # 진행상황 출력이 필요하면 주석 해제
        result = naver_news_api(query=keyword, display=1) 
        all_news_data.extend(result)
        time.sleep(0.3) # API 제한 고려

    # 중복 제거 (Title 기준)
    unique_news = list({news['Title']: news for news in all_news_data}.values())

    print(f"✅ 수집 및 중복 제거 완료! (총 {len(unique_news)}개 기사)")
    
    # 여기서 최종 결과 리스트를 반환합니다.
    return unique_news

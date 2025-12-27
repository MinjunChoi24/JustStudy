import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

def get_news_data(query="금융", display=30):

    load_dotenv()

    """
    네이버 뉴스 검색 API를 통해 뉴스 데이터를 가져옵니다.
    :param query: 검색어 (기본값: '경제')
    :param display: 가져올 기사 개수 (최대 100개)
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    # 한글 검색어 인코딩
    encoded_query = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display={display}&sort=sim"

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
            # HTML 태그 제거 (<b>태그 등이 섞여 나옴)
            title = item['title'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
            description = item['description'].replace("<b>", "").replace("</b>", "").replace("&quot;", "\"")
            
            if any(keyword in title for keyword in ["[인사]", "[부고]", "[포토]","인사","부고","포토"]):
                continue

            news_list.append({
                "Title": title,
                "Date": item['pubDate'],
                "Summary": description,
                "URL": item['originallink'] or item['link']
            })
            
        # [마법의 한 줄] 제목(Title)을 기준으로 중복을 제거합니다.
        news_list = list({news['Title']: news for news in news_list}.values())

        return news_list
    
    except Exception as e:
        print(f"❌ 네이버 API 호출 중 오류 발생: {e}")
        return []

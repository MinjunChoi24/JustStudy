import requests
import urllib.parse
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_news_data(query="경제", display=20):

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
            clean_date = datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %z").isoformat()
            news_list.append({
                "Title": title,
                "Date": clean_date,
                "Summary": description,
                "URL": item['originallink'] or item['link']
            })
            
        # 제목(Title)을 기준으로 중복을 제거합니다.
        news_list = list({news['Title']: news for news in news_list}.values())

        return news_list
    
    except Exception as e:
        print(f"❌ 네이버 API 호출 중 오류 발생: {e}")
        return []


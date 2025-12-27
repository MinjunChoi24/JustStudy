import requests
import urllib.parse



def get_news_data(query="경제", display=20):
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
            
            news_list.append({
                "Title": title,
                "Date": item['pubDate'],
                "Summary": description,
                "URL": item['originallink'] or item['link']
            })
        
        return news_list

    except Exception as e:
        print(f"❌ 네이버 API 호출 중 오류 발생: {e}")
        return []


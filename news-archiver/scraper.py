import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_news_data(target_date=None):
    # 날짜 지정이 없으면 오늘 날짜 사용
    if target_date is None:
        target_date = datetime.now().strftime('%Y%m%d')
    
    # 매일경제(009) 지면보기 URL
    url = "https://news.naver.com/section/101"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"📅 {target_date} 매일경제 지면 기사를 수집합니다...")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("❌ 네이버 뉴스 접속 실패")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        div= soup.find_all("div",{"class":"section_article _TEMPLATE"})


        for di in div:
            ul = di.find("ul",{"class":"sa_list"})
            li = ul.find_all("li")

            for i in li:
                sa = i.find("div",{"class":"sa_text"})
                summary = sa.find("div",{"class":"sa_text_lede"}).text
                press = sa.find("div",{"class":"sa_text_press"}).text
                link_title = i.find_all("a")
                for j in link_title:
                    link = j['href']
                    img_tag = j.find("img")
                    if img_tag:
                        title = img_tag['alt']
                        news_item = {
                            "Title": title,
                            "Date": target_date,
                            "Summary": summary,
                            "URL": link,
                            "Press": press
                        }
                        news_list.append(news_item)
            
        return news_list
    
    except Exception as e:
        print(f"에러 발생: {e}")
        return []
    

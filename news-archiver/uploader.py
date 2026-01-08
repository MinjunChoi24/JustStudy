import os
import datetime
from notion_client import Client
from dotenv import load_dotenv
from github import Github
from datetime import datetime


load_dotenv()

# 노션 클라이언트 접속
notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")

def save_to_notion(article, ai_result):
    """
    기사 정보(article)와 AI 분석 결과(ai_result)를 합쳐서 노션에 업로드합니다.
    """
    try:
        # 1. 데이터 가져오기 (없으면 기본값)
        cat_raw = ai_result.get('Category', '기타')
        sub_raw = ai_result.get('Subject', '일반')
        sum_raw = ai_result.get('Summary', '요약 없음')
        sec_raw = ai_result.get('Sector', '')

        # 2. 데이터 정제 (리스트 변환 및 문자열 처리)
        if not isinstance(cat_raw, list):
            cat_raw = [cat_raw]
        
        if not isinstance(sub_raw, list):
            sub_raw = str(sub_raw).split(',')

        if not isinstance(sec_raw, list):
            sec_raw = [sec_raw]

        

        # 다중 선택(Multi-select)용 리스트 만들기
        category_list = [{"name": str(c).replace(",", "")} for c in cat_raw]
        subject_list = [{"name": str(s).replace(",", "")} for s in sub_raw]
        sector_list = [{"name": str(se).replace(",", "")} for se in sec_raw if str(se).strip() != ""]
        
        # [중요 수정] Summary는 rich_text 형식이므로 content에 담아야 함 (2000자 제한)
        summary_content = str(sum_raw)[:2000]
        
        # 3. 노션 업로드 (순서 반영)
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Title": {
                    "title": [{"text": {"content": article['Title']}}]
                },
                "NewsDate":{
                    "date" : {
                        "start" : article['Date']
                }
                },
                "Category": { # 카테고리 (다중선택)
                    "multi_select": category_list
                },
                "Subject": { # 주제 (다중선택)
                    "multi_select": subject_list
                },
                "Summary": { # 요약 (텍스트) 
                    "rich_text": [{"text": {"content": summary_content}}]
                },
                "URL": { # 링크
                    "url": article['URL']
                },
                "Sector":{
                    "multi_select": sector_list
                }

            }
        )
        print(f"✅ 노션 저장 완료: {article['Title']}")
    
    except Exception as e:
        print(f"❌ 노션 저장 실패: {e}")


# GitHub 설정
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "MinjunChoi24/JustStudy" 

def save_to_github(briefing_content):

    
    # 1. GitHub 인증 및 레포지토리 연결
    if not GITHUB_TOKEN:
        print("❌ 오류: GITHUB_TOKEN이 설정되지 않았습니다.")
        return

    g = Github(GITHUB_TOKEN)
    
    try:
        # 'JustStudy/news-archiver' 같은 전체 이름으로 레포지토리를 찾습니다.
        repo = g.get_repo(REPO_NAME)
    except Exception as e:
        print(f"❌ 레포지토리 연결 실패: {e}")
        return
    
    # 2. 파일명 생성 (오늘 날짜)
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"news-archiver/daily_reports/{today}_Briefing.md"
    
    # 3. 마크다운 내용 구성
    # (상단에 날짜 헤더를 붙이고, 그 아래에 전달받은 내용을 그대로 이어 붙입니다)
    content = f"# 📅 {today} Daily Market Briefing\n\n"
    
    # ★ 핵심: 전달받은 긴 텍스트를 변형 없이 그대로 붙여넣기
    content += briefing_content 

    # 4. GitHub에 파일 생성 (또는 업데이트)
    try:
        # 이미 파일이 있으면 가져와서 업데이트(덮어쓰기)
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, f"Update report: {today}", content, contents.sha)
        print(f"✅ GitHub 업데이트 완료: https://github.com/{REPO_NAME}/blob/main/{file_path}")
    except:
        # 파일이 없으면 새로 생성
        repo.create_file(file_path, f"Add report: {today}", content)
        print(f"✅ GitHub 신규 생성 완료: https://github.com/{REPO_NAME}/blob/main/{file_path}")

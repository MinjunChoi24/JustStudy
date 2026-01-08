# 📈 Financial News Archiver & AI Analyst

**Financial News Archiver**는 한국 기준 오전 8시에 금융 시장 뉴스를 자동으로 수집하고, AI를 통해 분석하여 **Notion 데이터베이스**와 **GitHub**에 리포트 형태로 아카이빙하는 자동화 시스템입니다.

## 🌟 Key Features

* 1. 데이터 수집
* **뉴스 자동 수집**: Naver Search API를 활용하여 주요 금융 키워드(금리, 환율, 증시) 관련 최신 뉴스를 실시간으로 수집합니다.
  
* 2. 데이터 분석
* **Daily Market Briefing 생성**: Google **Gemini 2.5 Flash** 모델을 활용하여 수집된 뉴스를 바탕으로 '오늘의 시황 브리핑'을 자동으로 작성합니다.
* **AI 기반 뉴스 분류**: 로컬 LLM인 **Ollama (Gemma 3:4b)** 를 활용하여 뉴스의 Subject,Category,Sector(Category가 Company일 경우)를 정밀하게 분류하고 영문 태깅을 수행합니다.

* 3. 데이터 저장
* **Notion 자동 동기화**: 수집된 뉴스기사들을 NOTION_DATABASE_ID를 통해 News_Archive Database에 저장합니다.
* **GitHub 리포트 발행**: 생성된 브리핑 리포트를 Markdown 파일로 변환하여 GitHub 레포지토리에 자동 커밋합니다.

---

## 🛠 Tech Stack

| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white) | 메인 로직 및 데이터 처리 |
| **Data Source** | **Naver Search API** | 금융 뉴스 데이터 크롤링 |
| **LLM (Cloud)** | **Google Gemini 2.5 Flash** | 데일리 마켓 브리핑 요약 작성 |
| **LLM (Local)** | **Ollama (Gemma 3:4b)** | 뉴스 기사 분류 및 메타데이터 추출 |
| **Database** | **Notion API** | 뉴스 데이터베이스 구축 및 시각화 |
| **VCS** | **PyGithub** | 일일 리포트 자동 커밋 및 저장 |

---

## 📂 Project Structure

```bash
├── main.py             # 프로그램 진입점 (Orchestrator)
├── scraper.py          # 네이버 뉴스 수집 및 Gemini 브리핑 생성
├── classifier.py       # Ollama를 이용한 뉴스 분류 및 분석
├── uploader.py         # Notion 및 GitHub 업로드 처리
├── requirements.txt    # 의존성 라이브러리 목록
└── .env                # API 키 및 환경 변수 설정

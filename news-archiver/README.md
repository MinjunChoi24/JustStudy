# 📈 Financial News AI Archiver (금융 뉴스 AI 자동 수집기)

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Notion API](https://img.shields.io/badge/Notion-API-000000)
![Naver API](https://img.shields.io/badge/Naver-Search_API-03C75A)

### cmd
d:
cd D:\Study_Finance\news-archiver


## 📖 Project Overview
매일 쏟아지는 방대한 금융 뉴스를 효율적으로 관리하기 위한 **자동화 파이프라인**입니다.
Naver 검색 API를 통해 주요 경제 뉴스(금리, 환율, 증시 등)를 수집하고, **LLM(Large Language Model)을 이용해 뉴스의 핵심 주제와 섹터를 분석**한 뒤, Notion 데이터베이스에 자동으로 아카이빙합니다.

단순한 크롤링을 넘어, **AI를 활용한 비정형 데이터의 구조화(Structured Data)**를 목표로 합니다.

## ✨ Key Features
1. **Automated Scraping**: `requests`를 활용해 Naver 뉴스 검색 API에서 경제/금융 관련 최신 기사 수집
2. **AI Analysis**: 수집된 기사의 제목과 요약을 LLM이 분석하여 **Category(분야), Subject(주제), Sector(산업)** 자동 분류
3. **Notion Integration**: 분석된 데이터를 Notion API를 통해 실시간으로 DB에 적재
4. **Keyword Customization**: 시황, 환율, 특징주 등 시장 상황에 맞는 유동적 키워드 설정

## 🛠 Tech Stack
- **Language**: Python 3.x
- **Libraries**: `requests`, `python-dotenv`, `openai` (or `langchain`)
- **APIs**:
  - Naver Search API (News)
  - Notion API
  - LLM API (OpenAI GPT / Ollama etc.)

## 📂 Directory Structure
```bash
├── .gitignore       # API key 등 중요한 정보 유출 방지
├── README.md        # 프로젝트 문서
├── classifier.py    # AI 기반 뉴스 분석 및 분류 모듈
├── main.py          # 프로그램 진입점 (Orchestrator)
├── requirements.txt # 설치가 필요한 라이브러리
├── scraper.py       # 네이버 뉴스 수집 모듈
├── uploader.py      # Notion 데이터베이스 업로드 모듈
├── .env             # 환경 변수 (API Key 관리)
└── README.md        # 프로젝트 문서

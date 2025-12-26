import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Gemini API 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_article(article):
    # ✅ 2025년 최신 모델 사용
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are a financial news analyst. Analyze the following news article and provide the output in strict JSON format.
    
    [Article]
    Title: {article['Title']}
    Summary: {article['Summary']} 
    
    [Requirements]
    1. Category: Classify the news (e.g. Company,Finance,Market,Industry,Real estate,Macro)
    2. Subject: The main entity or keyword (e.g., Samsung, NPS, US Treasury).
    3. Sector: Follow this rule strictly:
        If the Category is 'Company': Identify the specific business sector the company belongs to (e.g., Semiconductor, Automotive, Bio, Banking).
        If the Category is NOT 'Company': Leave this field blank (empty string).
    4. Summary: {article['Summary']} 
    
    Output JSON only. Do NOT use Markdown code blocks. Just raw JSON.
    """

    try:
        response = model.generate_content(prompt)
        text_result = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text_result)

    except Exception as e:
        print(f"❌ Gemini 분석 중 에러: {e}")
        return {"Category": "기타", "Subject": "Error", "Summary": "분석 실패"}


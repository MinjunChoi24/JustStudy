import ollama
import json

def analyze_article(article):
    """
    Analyzes a news article using the gemma3 Ollama model and returns a JSON response.
    """
    # ✅ 2025년 최신 모델 사용
    target_model = "gemma3:4b"

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
    4. Summary: Output the summary content exactly as provided in the [Article] section. Do NOT translate it.
    5. Language & Format Rule: 
   - Translate (Category, Subject, Sector) into English. 
   - Use the official global company name (e.g., use "Samsung Electronics" instead of "Samsung", "Hyundai Motor" instead of "Hyundai").
    
    Output JSON only. Do NOT use Markdown code blocks. Just raw JSON.
    """

    try:
        # ✅ Ollama API 호출
        response = ollama.chat(
            model=target_model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,  # Disable streaming for full JSON output
            format='json'  # ✨ 핵심: JSON 출력을 강제함
        )

        # Ollama는 format='json' 설정 시 코드블록 없이 순수 JSON 텍스트만 반환하려 노력함
        text_result = response['message']['content']

        # Ensure the response is actually valid JSON.  Important for robustness.
        try:
            json_result = json.loads(text_result)
            return json_result
        except json.JSONDecodeError as e:
            print(f"❌ JSON decoding error: {e}.  Raw response: {text_result}")
            return {"Category": "기타", "Subject": "Error", "Summary": article['Summary']}

    except Exception as e:
        print(f"❌ ollama 분석 중 에러: {e}")
        return {"Category": "기타", "Subject": "Error", "Summary": article['Summary']}
    
# # 테스트 실행 예시
# sample_article = {"Title": "삼성전자, 3분기 영업이익 급증", "Summary": "반도체 호황으로 인해..."}
# print(analyze_article(sample_article))


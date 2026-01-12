## Daily_Market_Briefing 모델 비교
### gemini-3-flash-preview <- 현재 사용 모델
### gemini-2.5-pro <- Quata 초과로 쓸 수 없음


</br>

## Classification 모델 비교
### gemma3:4b <- 현재 사용 모델
### Finance-Llama-8B <- 쓰레기
### qwen2.5:7b <- 너무 오래걸림 . 분류 개별로
### qwen3:8b <- 오래걸림. 분류 Not bad

</br>

## Keyword 비교
### [금리,환율,증시]

</br>

## Prompt 비교
### 분류 할때 prompt - Ollama
    
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
    Translate (Category, Subject, Sector) into English. 
    Use the official global company name (e.g., use "Samsung Electronics" instead of "Samsung", "Hyundai Motor" instead of "Hyundai").
    
    Output JSON only. Do NOT use Markdown code blocks. Just raw JSON.
    """
</br>

### <Daily_Market_Briefing> prompt - Gemini
    
    prompt = f"""
    Based on the following news headlines and summaries,
    write a "Daily Market Briefing" that allows the reader
    to quickly grasp today’s financial market conditions.

    Write the briefing in Korean.

    Below is today’s news:

    {news_text_block}
    """

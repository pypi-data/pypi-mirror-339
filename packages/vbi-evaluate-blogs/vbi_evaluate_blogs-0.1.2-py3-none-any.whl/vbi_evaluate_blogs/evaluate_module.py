from text_check_module import text_check
from image_check_module import image_check
from fact_check_module import fact_check

def evaluate(llms: list[AzureChatOpenAI], text_content: str, image_content: list[str], claims: str):
    """
    This function evaluates the given text content, image content, and claims using two language models (LLMs).
    
    Parameters:
    - llms: A list of language model objects. The function expects two models: 'gpt-4o-mini' and 'o3-mini'.
    - text_content: The text data to be analyzed.
    - image_content: The image data to be analyzed.
    - claims: A list of claims to be fact-checked.

    The function performs the following checks:
    1. Text Check: Uses the 'o3-mini' model to analyze the text content.
    2. Image Check: Uses the 'gpt-4o-mini' model to analyze the image content.
    3. Fact Check: Uses the 'o3-mini' model to verify the claims.

    Returns:
    A formatted string containing the results of the text check, image check, and fact check.
    """
    gpt_4o_mini, o3_mini = None, None

    for llm in llms:
        if llm.model_name == 'gpt-4o-mini':
            gpt_4o_mini = llm
        else:
            o3_mini = llm

    result_text_check = text_check(o3_mini, text_content)
    result_image_check = image_check(gpt_4o_mini, image_content)
    result_fact_check = fact_check(o3_mini, claims)

    return f"""
    #Text Check Result:
    {result_text_check}

    #Image Check Result:
    {result_image_check}

    #Fact Check Result:
    {result_fact_check} 
    """

if __name__ == "__main__":
    from extract_module import extract_all
    from dotenv import load_dotenv
    from langchain_openai import AzureChatOpenAI
    import os

    load_dotenv()
    gpt_4o_mini = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="gpt-4o-mini",
        api_version="2024-08-01-preview",
        temperature=0.7,
        max_tokens=16000
    )

    o3_mini = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini",
        api_version="2024-12-01-preview",
    )

    pdf_path = "data/tc13.pdf"
    text_content, image_content, claims = extract_all(o3_mini, pdf_path)

    print(evaluate([gpt_4o_mini, o3_mini], text_content, image_content, claims))
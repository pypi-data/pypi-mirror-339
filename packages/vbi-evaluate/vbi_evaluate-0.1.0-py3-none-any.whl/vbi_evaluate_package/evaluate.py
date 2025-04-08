from text_check import check_text
from image_check import ImageCheck
from fact_check import FactCheck

def Evaluate(llms, text_content, image_content, claims):
    
    gpt_4o_mini = None; o3_mini = None

    for i in llms:
        if i.model_name == 'gpt-4o-mini':
            gpt_4o_mini = i
        else:
            o3_mini = i
    
    result_text_check = check_text(o3_mini, text_content)
    result_image_check = ImageCheck(gpt_4o_mini,image_content)
    result_fact_check = FactCheck(o3_mini,claims)

    return f"""
    #Text Check Result:
    {result_text_check}

    #Image Check Result:
    {result_image_check}

    #Fact Check Result:
    {result_fact_check} 
    """

if __name__ == "__main__":
    from extract import Extract
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
    text_content,image_content,claims = Extract(o3_mini,pdf_path)

    print(Evaluate([gpt_4o_mini,o3_mini],text_content, image_content, claims))
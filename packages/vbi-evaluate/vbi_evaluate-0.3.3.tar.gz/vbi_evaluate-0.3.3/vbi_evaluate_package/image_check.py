from langchain.schema import HumanMessage
from langchain.schema.messages import SystemMessage

def ImageCheck(llm: AzureChatOpenAI, images: list[str]) -> str:
    """
    Đánh giá mức độ liên quan giữa ảnh và phần chữ trong một tài liệu (dạng ảnh).

    Args:
        llm: Đối tượng AzureChatOpenAI đã cấu hình sẵn.
        image_base64 (str): Ảnh đã được mã hóa base64.

    Returns:
        str: Kết quả đánh giá do GPT-4o phản hồi.
    """

    result = []
    page=1

    for image_base64 in images:
        messages = [
            SystemMessage(content="Bạn là một chuyên gia phân tích ảnh và văn bản trong tài liệu."),
            HumanMessage(content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "Trang tài liệu dưới đây có thể bao gồm văn bản và hình ảnh. "
                        "Trả về kết quả có markdown"
                        "Hãy phân tích như sau:\n\n"
                        "1. **Có hình ảnh không?** Nếu không, chỉ cần ghi rõ: `Trang không chứa hình ảnh.` và không cần làm bước 2\n"
                        "2. **Nếu có hình ảnh**, hãy đánh giá:\n"
                        "- Nội dung ảnh mô tả gì?\n"
                        "- Ảnh có liên quan đến phần văn bản không?\n"
                        "- Mức độ hỗ trợ qua lại giữa ảnh và văn bản: **Cao / Trung bình / Thấp** (giải thích ngắn gọn)\n\n"
                        "🎯 Trả kết quả súc tích, chuyên môn, rõ ràng.\n"
                    )
                }
            ])
        ]

        response = llm.invoke(messages)
        result.append(f"Page {page}:\n"+response.content)
        page+=1
    return "\n\n".join(result)

if __name__ == "__main__":
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    import os
    from extract import extract_image

    load_dotenv()

    llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model="gpt-4o-mini",
            api_version="2024-08-01-preview",
            temperature=0.7,
            max_tokens=16000
        )

    pdf_path = "data/tc13.pdf"

    image_base64 = extract_image(pdf_path)
    print(ImageCheck(llm,image_base64))

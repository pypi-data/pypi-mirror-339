# vbi_evaluate_package

vbi_evaluate_package là một gói Python nhằm đánh giá nội dung các tài liệu PDF dựa trên nhiều tiêu chí:
- Kiểm tra cấu trúc bài viết.
- Đánh giá nội dung chi tiết.
- Kiểm tra ngữ pháp, lỗi chính tả, và văn phong.
- Tối ưu phân bổ từ khóa cho SEO.
- Kiểm tra tính độc nhất của nội dung.
- Đánh giá độ dễ đọc và logic.
- Kiểm chứng các phát biểu thông qua fact-check.
- Phân tích và đánh giá sự liên quan của hình ảnh.

## Tính Năng

- Trích xuất text và hình ảnh từ file PDF.
- Đánh giá các khía cạnh văn bản (cấu trúc, nội dung, ngữ pháp, SEO, readability).
- Kiểm tra, so sánh và truy xuất dữ liệu nhằm kiểm chứng tính xác thực của các phát biểu.
- Tích hợp với AzureChatOpenAI để sử dụng LLM cho nhiều nhiệm vụ đánh giá.

## Cấu Trúc Gói

```
e:\Code\py\temp\vbi_evaluate_package\
├── vbi_evaluate_package
│   ├── __init__.py
│   ├── text_check.py
│   ├── evaluate.py
│   ├── extract.py
│   ├── fact_check.py
│   └── image_check.py
└── README.md
```

## Hướng Dẫn Cài Đặt

1. Clone repository:
   ```
   git clone <repository_url>
   ```
2. Tạo môi trường ảo:
   ```
   python -m venv venv
   venv\Scripts\activate         # Trên Windows
   source venv/bin/activate      # Trên Linux/MacOS
   ```
3. Cài đặt các gói cần thiết:
   ```
   pip install -r requirements.txt
   ```
4. Tạo file `.env` chứa:
   - `AZURE_OPENAI_API_KEY`: API key của Azure OpenAI.
   - `AZURE_OPENAI_ENDPOINT`: Endpoint của Azure OpenAI.

## Hướng Dẫn Sử Dụng

### 1. Đánh Giá Toàn Diện File PDF

Module `evaluate.py` cung cấp hàm `Evaluate` để kết hợp đánh giá nội dung, hình ảnh và kiểm tra phát biểu.

Ví dụ:
```python
from vbi_evaluate_package.evaluate import Evaluate
from langchain_openai import AzureChatOpenAI
import os

# Khởi tạo các mô hình AzureChatOpenAI
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
    api_version="2024-12-01-preview"
)

# Đường dẫn file PDF cần đánh giá
pdf_path = "duong_dan_den_file_pdf.pdf"

# Sử dụng module extract để trích xuất nội dung
from vbi_evaluate_package.extract import extract_text, extract_image, extract_claim
text_content = extract_text(pdf_path)
image_content = extract_image(pdf_path)
claims = extract_claim(o3_mini, text_content)

# Thực hiện đánh giá toàn diện
result = Evaluate([gpt_4o_mini, o3_mini], text_content, image_content, claims)
print(result)
```

### 2. Trích Xuất Nội Dung File PDF

Module `extract.py` bao gồm các hàm:
- `extract_text`: Trích xuất text từ PDF.
- `extract_image`: Trích xuất hình ảnh (mã hóa base64).
- `extract_claim`: Trích xuất danh sách phát biểu cần kiểm chứng.

Ví dụ:
```python
from vbi_evaluate_package.extract import extract_text, extract_image, extract_claim

pdf_path = "duong_dan_den_file_pdf.pdf"
text_content = extract_text(pdf_path)
images = extract_image(pdf_path)
claims = extract_claim(o3_mini, text_content)
```

### 3. Kiểm Tra Nội Dung Văn Bản

Module `text_check.py` cung cấp hàm `check_text` để tổng hợp các bài kiểm tra về cấu trúc bài viết, nội dung và ngữ pháp. Hàm này được tích hợp trong quy trình đánh giá của module `evaluate.py`.

## Chạy Ứng Dụng

Để chạy module đánh giá, từ command line thực hiện:
```
python -m vbi_evaluate_package.evaluate
```
Đảm bảo rằng file PDF bạn muốn kiểm tra nằm trong thư mục phù hợp và đường dẫn được cập nhật chính xác.

## Ghi Chú

- Các mô hình LLM được cấu hình qua biến môi trường từ file `.env`.
- Điều chỉnh thông số như `temperature` và `max_tokens` phù hợp với yêu cầu và độ dài nội dung của file PDF.
- Tài liệu hướng dẫn sử dụng được tích hợp chuyên sâu trong mỗi module để dễ dàng tùy chỉnh.

Happy Evaluating!
import fitz
from PIL import Image
import io
import base64
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def extract_image(pdf_path):
    """Extract each page of a PDF as a base64-encoded image."""
    images_base64 = []  # List to store base64-encoded images
    try:
        doc = fitz.open(pdf_path)  # Open the PDF file
    except Exception as e:
        print(f"❌ Error opening PDF file: {e}")
        return images_base64

    for page in doc:  # Iterate through each page in the PDF
        try:
            pix = page.get_pixmap()  # Render the page as a pixmap
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Convert pixmap to an image
            buffered = io.BytesIO()  # Create an in-memory buffer
            img.save(buffered, format="JPEG", quality=75)  # Save the image as JPEG with quality 75
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Encode image to base64
            images_base64.append(str(img_base64))  # Append base64 string to the list
        except Exception as e:
            print(f"⚠️ Error processing PDF page: {e}")

    return images_base64

def extract_text(pdf_path):
    """Extract text from a PDF with improved formatting."""
    text_blocks = []  # List to store extracted text blocks
    try:
        doc = fitz.open(pdf_path)  # Open the PDF file
    except Exception as e:
        print(f"❌ Error opening PDF file: {e}")
        return ""

    for page in doc:  # Iterate through each page in the PDF
        blocks = page.get_text("blocks")  # Extract text blocks from the page
        if not blocks:  # If no blocks, extract plain text
            text_blocks.append(page.get_text("text"))
        else:
            blocks.sort(key=lambda b: (b[1], b[0]))  # Sort blocks by vertical and horizontal position
            text_blocks.extend(b[4] for b in blocks)  # Extract text from each block

    clean_text = " ".join(text_blocks)  # Join all text blocks into a single string
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Remove extra whitespace and clean up text

    return clean_text

def extract_claim(llm, content):
    """Extract claims from text content using a language model."""
    # Define a prompt template for extracting claims
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant specializing in extracting claims that need verification from a text."),
        ("user", "Extract a list of claims that need verification from the following content, each claim on a separate line: {content}")
    ])
    chain = prompt | llm | StrOutputParser()  # Create a processing chain with the prompt, LLM, and output parser
    return str(chain.invoke({"content": content}))  # Invoke the chain with the provided content

def Extract(llm, pdf_path):
    """Extract images, text, and claims from a PDF."""
    image_content = extract_image(pdf_path)  # Extract images as base64
    text_content = extract_text(pdf_path)  # Extract text content
    claims = extract_claim(llm, text_content)  # Extract claims from the text
    return text_content,image_content, claims  # Return all extracted data

if __name__ == "__main__":
    pdf_path = "data/tc8.pdf"  # Path to the PDF file

    # Extract images from the PDF
    images = extract_image(pdf_path)
    print(f"Extracted {len(images)} images from the PDF.")
    for i, img_base64 in enumerate(images, start=1):
        print(f"Image {i}: {img_base64[:50]}...")  # Print the first 50 characters of each base64 image

    # Extract text from the PDF
    text = extract_text(pdf_path)
    print("\nExtracted Text:")
    print(text)

    # Load environment variables and initialize the Azure OpenAI LLM
    from langchain_openai import AzureChatOpenAI
    import os
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from a .env file

    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # API key for Azure OpenAI
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  # Endpoint for Azure OpenAI
        model="gpt-4o-mini",  # Model name
        api_version="2024-08-01-preview",  # API version
        temperature=0.7,  # Sampling temperature for randomness
        max_tokens=10000  # Maximum number of tokens in the response
    )

    # Extract claims from the text using the LLM
    print("\nExtracted Claims:")
    print(extract_claim(llm, text))  # Print the extracted claims

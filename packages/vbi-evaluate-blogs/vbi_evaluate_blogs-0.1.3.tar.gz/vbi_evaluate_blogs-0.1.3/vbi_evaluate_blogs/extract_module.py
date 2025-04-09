import fitz
import io
import base64
import re
from PIL import Image
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def extract_image(pdf_path):
    """
    This function extracts each page of a PDF as a base64-encoded image.

    Parameters:
    - pdf_path: The file path of the PDF to be processed.

    Functionality:
    1. Opens the PDF file using the `fitz` library.
    2. Iterates through each page of the PDF.
    3. Converts each page into an image using the `get_pixmap` method.
    4. Encodes the image into a base64 string for easy storage or transmission.
    5. Handles errors gracefully, such as issues with opening the PDF or processing individual pages.

    Returns:
    - A list of base64-encoded strings, where each string represents an image of a PDF page.
    """
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
    """
    This function extracts text from a PDF file with improved formatting.

    Parameters:
    - pdf_path: The file path of the PDF to be processed.

    Functionality:
    1. Opens the PDF file using the `fitz` library.
    2. Iterates through each page of the PDF.
    3. Extracts text blocks from each page. If no blocks are found, extracts plain text.
    4. Sorts text blocks by their vertical and horizontal positions to maintain proper order.
    5. Cleans up the extracted text by removing extra whitespace and joining all text blocks into a single string.

    Returns:
    - A cleaned and formatted string containing the extracted text from the PDF.
    """
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
    """
    This function extracts claims from text content using a language model (LLM) and translates them into English.

    Parameters:
    - llm: The language model object used to process the content.
    - content: The text content from which claims need to be extracted.

    Functionality:
    1. Defines a prompt template to instruct the LLM to extract claims requiring verification and translate them into English.
    2. The prompt specifies that each claim should be listed on a separate line.
    3. Ensures the output contains only the necessary results without any explanations, symbols, or markings.
    4. Creates a processing chain that combines the prompt, the LLM, and an output parser.
    5. Invokes the chain with the provided content to extract and translate claims.

    Returns:
    - A string containing the extracted and translated claims, with each claim on a separate line.
    """
    # Define a prompt template for extracting and translating claims
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant specializing in extracting claims that need verification from a text and translating them into English."),
        ("user", "Extract a list of claims that need verification from the following content, translate each claim into English, and list them on separate lines. Only provide the necessary results without any explanations, symbols, or markings: {content}")
    ])
    chain = prompt | llm | StrOutputParser()  # Create a processing chain with the prompt, LLM, and output parser
    return str(chain.invoke({"content": content}))  # Invoke the chain with the provided content

def extract_all(llm, pdf_path):
    """
    This function extracts images, text, and claims from a PDF file.

    Parameters:
    - llm: The language model object used to process the text content and extract claims.
    - pdf_path: The file path of the PDF to be processed.

    Functionality:
    1. Calls the `extract_image` function to extract each page of the PDF as a base64-encoded image.
    2. Calls the `extract_text` function to extract and clean the text content from the PDF.
    3. Calls the `extract_claim` function to extract claims from the text content using the provided language model.

    Returns:
    - A tuple containing:
      1. The extracted text content as a string.
      2. A list of base64-encoded images representing the pages of the PDF.
      3. A string containing the extracted claims, with each claim on a separate line.
    """
    image_content = extract_image(pdf_path)  # Extract images as base64
    text_content = extract_text(pdf_path)  # Extract text content
    claims = extract_claim(llm, text_content)  # Extract claims from the text
    return text_content,image_content, claims  # Return all extracted data

if __name__ == "__main__":
    pdf_path = "data/tc13.pdf"  # Path to the PDF file

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
        model="o3-mini",  # Model name
        api_version="2024-12-01-preview",  # API version
    )

    # Extract claims from the text using the LLM
    print("\nExtracted Claims:")
    print(extract_claim(llm, text))  # Print the extracted claims

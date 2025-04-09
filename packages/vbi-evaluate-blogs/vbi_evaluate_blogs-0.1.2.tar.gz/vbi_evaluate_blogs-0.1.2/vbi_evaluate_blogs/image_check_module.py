from langchain.schema import HumanMessage
from langchain.schema.messages import SystemMessage
from langchain_openai import AzureChatOpenAI

def image_check(llm: AzureChatOpenAI, images: list[str]) -> str:
    """
    Evaluate the relevance between images and text in a document (in image format).

    Args:
        llm: Pre-configured AzureChatOpenAI object.
        images (list[str]): List of images encoded in base64 format.

    Returns:
        str: Evaluation results provided by GPT-4o.
    """

    result = []
    page = 1

    for image_base64 in images:
        messages = [
            SystemMessage(content="You are an expert in analyzing images and text in documents."),
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
                        "The document page below may include text and images. "
                        "Return the results in markdown format.\n"
                        "Analyze as follows:\n\n"
                        "1. **Is there an image?** If not, simply state: `The page does not contain an image.` and skip step 2.\n"
                        "2. **If there is an image**, evaluate:\n"
                        "- What does the image depict?\n"
                        "- Is the image relevant to the text?\n"
                        "- The level of mutual support between the image and text: **High / Medium / Low** (provide a brief explanation).\n\n"
                        "🎯 Provide concise, professional, and clear results.\n"
                    )
                }
            ])
        ]

        response = llm.invoke(messages)
        result.append(f"Page {page}:\n" + response.content)
        page += 1
    return "\n\n".join(result)

if __name__ == "__main__":
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    import os
    from extract_module import extract_image

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
    print(image_check(llm, image_base64))

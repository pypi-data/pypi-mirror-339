import gradio as gr
import os
from extract import Extract
from evaluate import Evaluate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLMs
llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    model="gpt-4o-mini",
    api_version="2024-08-01-preview",
    temperature=0.7,
    max_tokens=16000
)

llm1 = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    model="o3-mini",
    api_version="2024-12-01-preview",
)

file_num = -1

# Function to process PDF and evaluate
def process_pdf(pdf_file):
    global file_num
    file_num+=1
    pdf_path = f"input/input{file_num}.pdf"
    os.makedirs("input", exist_ok=True)

    # pdf_file là NamedString => copy file từ đường dẫn pdf_file.name
    with open(pdf_file.name, "rb") as src, open(pdf_path, "wb") as dst:
        dst.write(src.read())

    # Tiếp tục như cũ
    image_content, text_content, claims = Extract(llm1, pdf_path)
    evaluation_result = Evaluate(llm, llm1, text_content, image_content, claims)

    return evaluation_result

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# PDF Evaluation App")
    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        process_button = gr.Button("Process")
    result_output = gr.Textbox(label="Evaluation Result", lines=20, interactive=False)

    process_button.click(process_pdf, inputs=pdf_input, outputs=result_output)

# Launch the app
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)

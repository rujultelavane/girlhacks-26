import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI

# 1. Initialize and authenticate Azure services
load_dotenv()

# Setup Azure OpenAI client
ai_client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview" # Standard stable API version
)

# Setup Azure Document Intelligence client
doc_client = DocumentAnalysisClient(
    endpoint=os.getenv("AZURE_DOC_INTEL_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_DOC_INTEL_KEY"))
)
def extract_text_from_file(file_path):
    """
    Uses Azure Document Intelligence to extract layout-aware text
    from a PDF, image, Word document, or audio transcript log.
    """
    print(f"Reading file with Azure Document Intelligence: {file_path}...")
    
    with open(file_path, "rb") as f:
        # 'prebuilt-layout' handles tables, paragraphs, and lists beautifully
        poller = doc_client.begin_analyze_document("prebuilt-layout", document=f)
        result = poller.result()
        
    # Combine all extracted paragraphs into one unified text block
    full_text = "\n".join([paragraph.content for paragraph in result.paragraphs])
    return full_text

def summarize_text(extracted_text, summary_style="bullet points"):
    """
    Sends the extracted text block to Azure OpenAI to synthesize a summary.
    """
    print("Generating summary with Azure OpenAI...")
    
    system_prompt = (
        "You are an expert AI assistant specializing in administrative synthesis. "
        "Your task is to analyze the provided input text (which could be a document or "
        "a meeting transcript) and generate a clear, highly structured summary. "
        f"Format your output primarily as {summary_style}."
    )
    
    # Use gpt-4o-mini for cost-effective, high-speed document synthesis
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please summarize the following text:\n\n{extracted_text}"}
        ],
        temperature=0.3 # Low temperature ensures factual consistency
    )
    
    return response.choices[0].message.content

# 2. Execution Wrapper
if __name__ == "__main__":
    # Replace this with the path to your meeting transcript file or PDF document
    target_file = "meeting_notes.pdf" 
    
    try:
        # Step A: Parse the text out of the file
        raw_text = extract_text_from_file(target_file)
      
        # Step B: Pass that text to the LLM for summary processing
        ai_summary = summarize_text(raw_text, summary_style="action items and key decisions")
        
        print("\n=== AI SUMMARY RESULT ===")
        print(ai_summary)
        
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        print("Please ensure your endpoint URLs, API keys, and file paths are correct.")
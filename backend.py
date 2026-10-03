import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI

def get_azure_clients():
    """Initializes Azure OpenAI and Document Intelligence clients."""
    load_dotenv()
    
    endpoint_openai = os.getenv("AZURE_OPENAI_ENDPOINT")
    key_openai = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint_doc = os.getenv("AZURE_DOC_INTEL_ENDPOINT")
    key_doc = os.getenv("AZURE_DOC_INTEL_KEY")
    
    # Fallback check for Streamlit secrets if running on Streamlit Community Cloud
    try:
        import streamlit as st
        endpoint_openai = endpoint_openai or st.secrets.get("AZURE_OPENAI_ENDPOINT")
        key_openai = key_openai or st.secrets.get("AZURE_OPENAI_API_KEY")
        endpoint_doc = endpoint_doc or st.secrets.get("AZURE_DOC_INTEL_ENDPOINT")
        key_doc = key_doc or st.secrets.get("AZURE_DOC_INTEL_KEY")
    except Exception:
        pass

    if not all([endpoint_openai, key_openai, endpoint_doc, key_doc]):
        return None, None

    ai_client = AzureOpenAI(
        azure_endpoint=endpoint_openai,
        api_key=key_openai,
        api_version="2024-08-01-preview"
    )
    
    doc_client = DocumentAnalysisClient(
        endpoint=endpoint_doc,
        credential=AzureKeyCredential(key_doc)
    )
    
    return ai_client, doc_client

def extract_text(doc_client, uploaded_file):
    """Parses text directly from file bytes using Azure Document Intelligence."""
    if not doc_client:
        return ""
    file_bytes = uploaded_file.read()
    poller = doc_client.begin_analyze_document("prebuilt-layout", document=file_bytes)
    result = poller.result()
    return "\n".join([paragraph.content for paragraph in result.paragraphs])

def generate_summary(ai_client, text, style):
    """Generates a structured summary using Azure OpenAI."""
    if not ai_client:
        return ""
    system_prompt = (
        "You are an expert AI assistant specializing in administrative synthesis. "
        f"Format your output explicitly as {style.lower()}."
    )
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def audit_summary_accuracy(ai_client, original_text, summary_text):
    """Audits the generated summary against the source text to ensure factual accuracy."""
    if not ai_client:
        return ""
    system_prompt = (
        "You are an impartial AI Compliance and Verification Auditor. "
        "Your task is to compare the GENERATED SUMMARY against the ORIGINAL TEXT. "
        "Provide:\n"
        "1. Accuracy Score (0-100%)\n"
        "2. Verification Status (Passed / Caution / Failed)\n"
        "3. Fact Check Breakdown (Highlight missing key points or hallucinated claims)."
    )
    user_prompt = f"--- ORIGINAL TEXT ---\n{original_text}\n\n--- GENERATED SUMMARY ---\n{summary_text}"
    
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def query_document_insights(ai_client, user_question, document_text, chat_history):
    """Answers user questions based strictly on the uploaded document text."""
    if not ai_client:
        return ""
    system_prompt = (
        "You are a Document Insights Expert. Answer user questions accurately based on "
        "the uploaded document content provided below. If a metric or answer isn't "
        "mentioned in the text, state that clearly.\n\n"
        f"DOCUMENT CONTENT:\n{document_text}"
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_question})
    
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content
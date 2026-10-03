import os
import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI

# 1. Page Configuration & Title
st.set_page_config(page_title="Azure AI Document & Insight Studio", page_icon="📝", layout="wide")
st.title("📝 Azure AI Summarizer & Document Intelligence Studio")
st.markdown("Upload documents, evaluate summary accuracy with AI, and chat directly with your document.")

# 2. Session State Initialization
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary_str" not in st.session_state:
    st.session_state.summary_str = ""
if "accuracy_report" not in st.session_state:
    st.session_state.accuracy_report = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# 3. Azure Services Initialization
@st.cache_resource
def get_azure_clients():
    """Initializes and caches Azure clients."""
    load_dotenv()
    
    endpoint_openai = os.getenv("AZURE_OPENAI_ENDPOINT") or st.secrets.get("AZURE_OPENAI_ENDPOINT")
    key_openai = os.getenv("AZURE_OPENAI_API_KEY") or st.secrets.get("AZURE_OPENAI_API_KEY")
    endpoint_doc = os.getenv("AZURE_DOC_INTEL_ENDPOINT") or st.secrets.get("AZURE_DOC_INTEL_ENDPOINT")
    key_doc = os.getenv("AZURE_DOC_INTEL_KEY") or st.secrets.get("AZURE_DOC_INTEL_KEY")
    
    if not all([endpoint_openai, key_openai, endpoint_doc, key_doc]):
        st.error("Missing Azure Credentials! Please check your .env or Streamlit secrets configuration.")
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

ai_client, doc_client = get_azure_clients()

# 4. Core Processing Functions

def extract_text(uploaded_file):
    """Parses text directly from file bytes using Azure Document Intelligence."""
    if not doc_client:
        return ""
    file_bytes = uploaded_file.read()
    poller = doc_client.begin_analyze_document("prebuilt-layout", document=file_bytes)
    result = poller.result()
    return "\n".join([paragraph.content for paragraph in result.paragraphs])

def generate_summary(text, style):
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

# AI MODEL 1: Accuracy & Hallucination Auditor
def audit_summary_accuracy(original_text, summary_text):
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

# CHUNKING HELPER FUNCTION
def chunk_text(text, max_chars=5000):
    """Splits long documents into manageable chunks."""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]



# AI MODEL 2: Interactive Insights & Q&A Chatbot
def query_document_insights(user_question, document_text, chat_history):
    """Answers user questions based strictly on the uploaded document text."""
    if not ai_client:
        return ""

    chunks = chunk_text(document_text)

    system_prompt = (
        "You are a Document Insights Expert. When answering:\n"
        "1. Quote the exact lines from the document you used.\n"
        "2. If the answer is not present, say 'The document does not mention this.'\n\n"
    )

    for i, chunk in enumerate(chunks):
        system_prompt += f"\n--- DOCUMENT CHUNK {i+1} ---\n{chunk}\n"

        # Build messages: system + history + new question
        messages = [{"role": "system", "content": system_prompt}]

        # Only append user/assistant messages (not system)
        for msg in chat_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append(msg)

        messages.append({"role": "user", "content": user_question})

        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3
        )

    return response.choices[0].message.content

# def query_document_insights(user_question, document_text, chat_history):
#     """Answers user questions based strictly on the uploaded document text."""
#     if not ai_client:
#         return ""
#     system_prompt = (
#         "You are a Document Insights Expert. Answer user questions accurately based on "
#         "the uploaded document content provided below. If a metric or answer isn't "
#         "mentioned in the text, state that clearly.\n\n"
#         f"DOCUMENT CONTENT:\n{document_text}"
#     )
    
#     messages = [{"role": "system", "content": system_prompt}]
#     for msg in chat_history:
#         messages.append({"role": msg["role"], "content": msg["content"]})
#     messages.append({"role": "user", "content": user_question})
    
#     response = ai_client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages,
#         temperature=0.3
#     )
#     return response.choices[0].message.content



# 5. Sidebar Controls
st.sidebar.header("⚙️ Configuration")
summary_style = st.sidebar.selectbox(
    "Choose Summary Format:",
    ["Action Items and Key Decisions", "Executive Summary Paragraph", "Bullet Points", "Detailed Study Notes"]
)

if st.sidebar.button("🧹 Clear App State"):
    st.session_state.extracted_text = ""
    st.session_state.summary_str = ""
    st.session_state.accuracy_report = ""
    st.session_state.chat_messages = []
    st.rerun()

# 6. Main UI Layout
uploaded_file = st.file_uploader("Upload document (PDF, DOCX, PNG, JPG):", type=["pdf", "png", "jpg", "jpeg", "docx"])

if uploaded_file is not None:
    st.info(f"File uploaded: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 2)} KB)")
    
    if st.button("✨ Process Document & Generate Summary", type="primary"):
        if ai_client and doc_client:
            with st.spinner("Extracting text via Azure Document Intelligence..."):
                try:
                    st.session_state.extracted_text = extract_text(uploaded_file)
                except Exception as e:
                    st.error(f"Failed to extract text: {e}")

            if st.session_state.extracted_text:
                with st.spinner("Synthesizing summary via Azure OpenAI..."):
                    st.session_state.summary_str = generate_summary(st.session_state.extracted_text, summary_style)
                
                with st.spinner("Auditing accuracy (Model 1)..."):
                    st.session_state.accuracy_report = audit_summary_accuracy(
                        st.session_state.extracted_text, 
                        st.session_state.summary_str
                    )
                st.success("Document processing complete!")

# 7. Results Dashboard (Tabs)
if st.session_state.summary_str:
    tab1, tab2, tab3 = st.tabs(["📋 Summary & Audit", "💬 Interactive Chatbot", "📄 Raw Text"])
    
    with tab1:
        st.subheader(f"Summary ({summary_style})")
        st.markdown(st.session_state.summary_str)
        st.divider()
        st.subheader("🔍 Accuracy Audit Report (AI Model 1)")
        st.info(st.session_state.accuracy_report)
        
    with tab2:
        st.subheader("💬 Document Insights & Q&A (AI Model 2)")
        st.caption("Ask questions, query metrics, or extract specific details from your file.")
        
        # Display chat history
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat input prompt
        if user_query := st.chat_input("Ask a question about your uploaded document..."):
            st.session_state.chat_messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
                
            with st.chat_message("assistant"):
                with st.spinner("Analyzing document..."):
                    bot_response = query_document_insights(
                        user_query, 
                        st.session_state.extracted_text, 
                        st.session_state.chat_messages
                    )
                    st.markdown(bot_response)
            
            st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})

    with tab3:
        st.subheader("Extracted Raw Text")
        st.text_area("Source text extracted from Document Intelligence:", st.session_state.extracted_text, height=350)
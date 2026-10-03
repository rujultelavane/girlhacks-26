import streamlit as st
from mockbackend import (
    get_azure_clients,
    extract_text,
    generate_summary,
    audit_summary_accuracy,
    query_document_insights
)

# 1. Page Configuration & Layout
st.set_page_config(page_title="Azure AI Document Studio", page_icon="📝", layout="wide")

# Custom CSS to draw red section borders matching your wireframe
st.markdown("""
<style>
    /* Styling section containers */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"] {
        border-radius: 8px;
    }
    
    .section-box {
        border: 2px solid #ff4b4b;
        border-radius: 6px;
        padding: 16px;
        background-color: #f9f9fb;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary_str" not in st.session_state:
    st.session_state.summary_str = ""
if "accuracy_report" not in st.session_state:
    st.session_state.accuracy_report = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# 3. Client Initialization
@st.cache_resource
def cached_clients():
    ai_client, doc_client = get_azure_clients()
    if not ai_client or not doc_client:
        st.error("Missing Azure Credentials! Check your configuration.")
    return ai_client, doc_client

ai_client, doc_client = cached_clients()

# 4. Layout Grid Split (Left Sidebar Panel vs. Main Dashboard)
col_left, col_right = st.columns([1, 2.5], gap="large")

# ==========================================
# LEFT COLUMN: Chatbot & File Upload Sections
# ==========================================
with col_left:
    # Top Box: Chatbot Section
    with st.container(border=True):
        st.subheader("💬 Chatbot")
        
        if not st.session_state.extracted_text:
            st.info("Upload a document below to start chatting with your file.")
        else:
            # Display chat message history inside height-bounded box
            chat_box = st.container(height=300)
            for msg in st.session_state.chat_messages:
                chat_box.chat_message(msg["role"]).markdown(msg["content"])
                
            if user_query := st.chat_input("Ask a question..."):
                st.session_state.chat_messages.append({"role": "user", "content": user_query})
                chat_box.chat_message("user").markdown(user_query)
                
                with chat_box.chat_message("assistant"):
                    with st.spinner("Analyzing..."):
                        bot_response = query_document_insights(
                            ai_client,
                            user_query, 
                            st.session_state.extracted_text, 
                            st.session_state.chat_messages[:-1]
                        )
                        st.markdown(bot_response)
                
                st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})

    # Bottom Box: File Upload Section
    with st.container(border=True):
        st.subheader("📁 Upload file(s)")
        uploaded_file = st.file_uploader(
            "Upload PPT, Audio/Transcripts, Notes, PDFs", 
            type=["pdf", "png", "jpg", "jpeg", "docx", "pptx", "txt"]
        )
        
        summary_style = st.selectbox(
            "Summary Format:",
            ["Action Items and Key Decisions", "Executive Summary Paragraph", "Bullet Points", "Detailed Study Notes"]
        )
        
        if uploaded_file is not None:
            if st.button("✨ Process Document", type="primary", use_container_width=True):
                if ai_client and doc_client:
                    with st.spinner("Extracting text..."):
                        try:
                            st.session_state.extracted_text = extract_text(doc_client, uploaded_file)
                        except Exception as e:
                            st.error(f"Extraction failed: {e}")

                    if st.session_state.extracted_text:
                        with st.spinner("Generating summary..."):
                            st.session_state.summary_str = generate_summary(
                                ai_client, st.session_state.extracted_text, summary_style
                            )
                        with st.spinner("Auditing accuracy..."):
                            st.session_state.accuracy_report = audit_summary_accuracy(
                                ai_client, st.session_state.extracted_text, st.session_state.summary_str
                            )
                        st.success("Complete!")

# ==========================================
# RIGHT COLUMN: Personal Dashboard Section
# ==========================================
with col_right:
    with st.container(border=True):
        st.title("📊 Personal Dashboard")
        
        if st.session_state.summary_str:
            tab1, tab2, tab3 = st.tabs(["📋 Summary & Audit Report", "🔍 Key Insights", "📄 Raw Text"])
            
            with tab1:
                st.subheader(f"Summary ({summary_style})")
                st.markdown(st.session_state.summary_str)
                st.divider()
                st.subheader("🔍 Accuracy Audit Report")
                st.info(st.session_state.accuracy_report)

            with tab2:
                st.subheader("Extracted Metrics & Insights")
                st.write("Dynamic dashboard analytics or document breakdown go here.")

            with tab3:
                st.subheader("Extracted Raw Text")
                st.text_area("Source Text", st.session_state.extracted_text, height=450)
        else:
            st.info("Your processed document summary, analysis, and insights will appear here.")
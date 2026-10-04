import streamlit as st
from mockbackend import (
    get_azure_clients,
    extract_text,
    generate_summary,
    audit_summary_accuracy,
    query_document_insights
)

# 1. Page Configuration & Layout
st.set_page_config(page_title="Enchanted Document Studio", page_icon="🌙", layout="wide")

# Custom Twilight Enchanted Forest & Whimsy CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&family=Vollkorn:ital,wght@0,400;0,700;1,400&display=swap');

/* Force Pale Mint Text Everywhere */
html, body, [class*="css"], p, span, div, label {
    font-family: 'Quicksand', sans-serif;
    color: #d3fcd5 !important;
}

/* Main Background */
.stApp {
    background-color: #44344f;
    background-image: radial-gradient(circle at 50% 0%, #564d80 0%, #44344f 80%);
}

/* Glowing Lime Green Headers */
h1, h2, h3, h4, h5, h6, [data-testid="stSubheader"] {
    font-family: 'Vollkorn', serif !important;
    color: #c2f970 !important; 
    text-shadow: 0 0 15px rgba(194, 249, 112, 0.4);
    letter-spacing: 1px;
}

/* 🌿 MAGIC CONTAINERS */
[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stForm"],
.stContainer {
    background: rgba(86, 77, 128, 0.35) !important;
    border: 2px solid #98a6d4 !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(20, 15, 25, 0.6), inset 0 0 20px rgba(152, 166, 212, 0.1) !important;
    padding: 15px;
}

/* 🍄 AGGRESSIVE OVERRIDE FOR WHITE INPUT BOXES */
/* File Uploader Container */
[data-testid="stFileUploader"] {
    background-color: rgba(68, 52, 79, 0.95) !important;
    border: 1px solid #c2f970 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
[data-testid="stFileUploadDropzone"] {
    background-color: transparent !important;
}
[data-testid="stFileUploader"] section {
    background-color: transparent !important;
}
/* File Uploader 'Browse Files' Button */
[data-testid="stFileUploader"] button {
    background-color: #564d80 !important;
    color: #d3fcd5 !important;
    border: 1px solid #98a6d4 !important;
    border-radius: 8px !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background-color: rgba(68, 52, 79, 0.95) !important; 
    border: 1px solid #c2f970 !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] * { color: #d3fcd5 !important; }

/* 📜 INFO ALERTS */
div[data-testid="stAlert"] {
    background-color: rgba(86, 77, 128, 0.8) !important;
    border: 1px solid #98a6d4 !important;
    border-left: 5px solid #c2f970 !important;
    border-radius: 8px !important;
}
div[data-testid="stAlert"] * {
    font-weight: 600 !important;
}

/* ✨ GLOWING POTION BUTTONS */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(180deg, #564d80 0%, #44344f 100%) !important;
    color: #c2f970 !important;
    border: 2px solid #c2f970 !important;
    border-radius: 20px !important; 
    padding: 10px 24px;
    font-family: 'Vollkorn', serif;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(194, 249, 112, 0.2);
    transition: all 0.3s ease;
}

button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-3px) scale(1.02) !important;
    background: linear-gradient(180deg, #98a6d4 0%, #564d80 100%) !important;
    box-shadow: 0 0 25px rgba(194, 249, 112, 0.6) !important;
    color: #ffffff !important;
    border-color: #d3fcd5 !important;
}

/* 🦉 CHAT INPUT & MESSAGES */
div[data-testid="stChatInput"] {
    background-color: rgba(68, 52, 79, 0.9) !important;
    border: 1px solid #98a6d4 !important;
    border-radius: 20px !important;
}
div[data-testid="stChatInput"] * { color: #d3fcd5 !important; }

[data-testid="stChatMessage"] {
    background-color: rgba(86, 77, 128, 0.4) !important;
    border-radius: 12px;
    border-left: 3px solid #c2f970;
    padding: 15px;
    margin-bottom: 15px;
}
[data-testid="chatAvatarIcon-user"] { background-color: #98a6d4 !important; }
[data-testid="chatAvatarIcon-assistant"] { background-color: #c2f970 !important; color: #44344f !important; }

/* 🍃 TABS STYLING */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    color: #98a6d4 !important;
    font-family: 'Vollkorn', serif;
    font-size: 1.2rem;
}
button[aria-selected="true"] {
    color: #c2f970 !important;
    border-bottom: 3px solid #c2f970 !important;
    text-shadow: 0 0 8px rgba(194, 249, 112, 0.5);
}

/* 🧚 WHIMSICAL ANIMATIONS */
@keyframes floatUp {
    0% { transform: translateY(0px) translateX(0px) scale(1); opacity: 0.1; }
    50% { transform: translateY(-40px) translateX(20px) scale(1.2); opacity: 0.9; }
    100% { transform: translateY(-80px) translateX(-15px) scale(1); opacity: 0.1; }
}
@keyframes sparkleGlow {
    0%, 100% { opacity: 0.5; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

.firefly {
    position: fixed;
    width: 6px;
    height: 6px;
    background-color: #c2f970;
    border-radius: 50%;
    box-shadow: 0 0 12px #c2f970, 0 0 24px #d3fcd5;
    animation: floatUp 6s infinite ease-in-out;
    pointer-events: none;
    z-index: 999;
}
.sparkle { display: inline-block; animation: sparkleGlow 2s infinite ease-in-out; }
.magic-divider {
    text-align: center; color: #98a6d4; font-size: 1.5rem; margin: 20px 0; letter-spacing: 5px; opacity: 0.7;
}
</style>

<!-- Bioluminescent Firefly Particles -->
<div class="firefly" style="top: 85%; left: 10%; animation-delay: 0s;"></div>
<div class="firefly" style="top: 60%; left: 85%; animation-delay: 1.5s;"></div>
<div class="firefly" style="top: 75%; left: 20%; animation-delay: 3s;"></div>
<div class="firefly" style="top: 35%; left: 70%; animation-delay: 2.2s;"></div>
<div class="firefly" style="top: 85%; left: 37%; animation-delay: 0.5s;"></div>
<div class="firefly" style="top: 20%; left: 92%; animation-delay: 4.5s;"></div>
<div class="firefly" style="top: 95%; left: 57%; animation-delay: 3.1s;"></div>
<div class="firefly" style="top: 15%; left: 77%; animation-delay: 1.2s;"></div>
<div class="firefly" style="top: 50%; left: 5%; animation-delay: 2.8s;"></div>
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
        st.error("Missing Azure Credentials! Please check your configuration.")
    return ai_client, doc_client

ai_client, doc_client = cached_clients()

def magic_divider():
    st.markdown("<div class='magic-divider'>✧･ﾟ: *✧･ﾟ:* ✨ *:･ﾟ✧*:･ﾟ✧</div>", unsafe_allow_html=True)

# 4. Layout Grid Split
col_left, col_right = st.columns([1, 2.5], gap="large")

with col_left:
    with st.container(border=True):
        st.subheader("🦉 Chat Assistant")
        
        if not st.session_state.extracted_text:
            st.info("Upload a document below to start chatting.")
        else:
            chat_box = st.container(height=300)
            for msg in st.session_state.chat_messages:
                chat_box.chat_message(msg["role"]).markdown(msg["content"])
                
            if user_query := st.chat_input("Ask a question about your document..."):
                st.session_state.chat_messages.append({"role": "user", "content": user_query})
                chat_box.chat_message("user").markdown(user_query)
                
                with chat_box.chat_message("assistant"):
                    with st.spinner("Processing..."):
                        bot_response = query_document_insights(
                            ai_client, user_query, st.session_state.extracted_text, st.session_state.chat_messages[:-1]
                        )
                        st.markdown(bot_response)
                st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})

    magic_divider()

    with st.container(border=True):
        st.subheader("📜 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload files (PDF, DOCX, PPTX, TXT, Images)", 
            type=["pdf", "png", "jpg", "jpeg", "docx", "pptx", "txt"]
        )
        
        summary_style = st.selectbox(
            "Select Summary Format:",
            ["Action Items & Key Decisions", "Executive Summary Paragraph", "Bullet Points", "Detailed Notes"]
        )
        
        if uploaded_file is not None:
            if st.button("✨ Process Document ✨", type="primary", use_container_width=True):
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
                        st.success("Analysis Complete!")

with col_right:
    with st.container(border=True):
        # Center the main title using HTML
        st.markdown("<h1 style='text-align: center;'>🌿 Document Dashboard</h1>", unsafe_allow_html=True)
        
        if st.session_state.summary_str:
            tab1, tab2, tab3 = st.tabs(["🍄 Summary", "🍃 Insights", "📜 Raw Text"])
            
            with tab1:
                st.subheader(f"✨ {summary_style}")
                st.markdown(st.session_state.summary_str)
                magic_divider()
                st.subheader("🔍 Accuracy Report")
                st.info(st.session_state.accuracy_report)
            with tab2:
                st.subheader("Metrics & Insights")
                st.write("Dashboard analytics and extracted metrics will manifest here.")
                st.markdown("<h1 style='text-align: center; font-size: 5rem; opacity: 0.5;'>🧚‍♂️ 🦋 🌸</h1>", unsafe_allow_html=True)
            with tab3:
                st.subheader("Raw Extracted Text")
                st.text_area("Source Text", st.session_state.extracted_text, height=450)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 50px 20px;">
                <h1 style="font-size: 4rem; opacity: 0.8; margin-bottom: 10px;"><span class="sparkle">✨</span> 📖 <span class="sparkle">✨</span></h1>
                <h3 style="color: #98a6d4;">Dashboard is empty.</h3>
                <p style="font-size: 1.2rem; color: #d3fcd5; opacity: 0.8;">Upload a file on the left to reveal its insights.</p>
            </div>
            """, unsafe_allow_html=True)
            magic_divider()
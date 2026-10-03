import time

def get_azure_clients():
    """Mock client setup — returns True, True so app logic proceeds without API keys."""
    return True, True

def extract_text(doc_client, uploaded_file):
    """Simulates text extraction from an uploaded file."""
    time.sleep(1.5)  # Simulate processing delay
    return (
        f"--- MOCK EXTRACTED TEXT FROM: {uploaded_file.name} ---\n\n"
        "Project Scope & Goals:\n"
        "1. Launch Azure AI Document Insights Studio by Q3 2026.\n"
        "2. Implement document parsing using Document Intelligence API.\n"
        "3. Integrate GPT-4o-mini models for accuracy auditing and conversational chat.\n"
        "4. Project Budget: Estimated at $15,000 for cloud infrastructure and model usage.\n"
        "5. Key Risks: High API latency during peak hours and missing secret environment keys."
    )

def generate_summary(ai_client, text, style):
    """Simulates summary generation based on the selected format style."""
    time.sleep(1.0)  # Simulate model latency
    
    if style == "Action Items and Key Decisions":
        return (
            "### 🎯 Action Items & Key Decisions\n"
            "- [ ] Finalize Azure subscription setup and API keys by end of week.\n"
            "- [ ] Test Document Intelligence parsing throughput with large PDFs.\n"
            "- [ ] Integrate user feedback on chatbot responsiveness."
        )
    elif style == "Executive Summary Paragraph":
        return (
            "**Executive Summary:** The Azure AI Document Insights project aims to deliver automated "
            "document extraction, audit evaluation, and multi-turn conversational support by Q3 2026 with "
            "an estimated budget of $15,000."
        )
    elif style == "Bullet Points":
        return (
            "### 📌 Key Highlights\n"
            "- Target Launch: Q3 2026\n"
            "- Primary Budget: $15,000\n"
            "- Key Features: Document layout analysis, summary verification, and interactive document chat."
        )
    else:  # Detailed Study Notes
        return (
            "### 📚 Detailed Notes\n"
            "**Overview:** Comprehensive architecture combining Azure AI Document Intelligence and OpenAI models.\n"
            "**Financials:** Allocated cloud spend is $15,000.\n"
            "**Mitigation:** Monitor latency and set up fallback credential loading."
        )

def audit_summary_accuracy(ai_client, original_text, summary_text):
    """Simulates Model 1 (Accuracy & Hallucination Audit Report)."""
    time.sleep(1.0)
    return (
        "✅ **Accuracy Score:** 98%\n"
        "🟢 **Verification Status:** Passed\n\n"
        "**Fact-Check Breakdown:**\n"
        "- Launch timeline (Q3 2026) verified against source.\n"
        "- Project budget ($15,000) verified against source.\n"
        "- No missing critical points or hallucinated claims detected."
    )

def query_document_insights(ai_client, user_question, document_text, chat_history):
    """Simulates Model 2 (Document Chatbot Response)."""
    time.sleep(1.0)
    
    question_lower = user_question.lower()
    if "budget" in question_lower or "cost" in question_lower:
        return "According to the document, the estimated project budget is **$15,000** for cloud infrastructure and model usage."
    elif "launch" in question_lower or "date" in question_lower or "when" in question_lower:
        return "The document states that the target launch for the Azure AI Document Insights Studio is **Q3 2026**."
    elif "risk" in question_lower:
        return "The primary risks mentioned are high API latency during peak hours and missing environment API keys."
    else:
        return f"*(Mock Answer)* Based on the document, here is what was found regarding '{user_question}': The project scope focuses on building a streamlined Streamlit dashboard with document intelligence and AI-backed summary auditing."
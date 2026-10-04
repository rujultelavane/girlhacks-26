# 🌿 Long Story Short

> **Turn messy conversations and documents into clear insights, decisions, and next steps.**

**Long Story Short** is an AI-powered enterprise productivity tool that transforms meeting notes, documents, and other unstructured information into actionable insights. Upload a document, choose how you want it summarized, ask questions through the built-in chatbot, and quickly identify the decisions and action items that matter.

Built for the **[AI for the Modern Enterprise: AI-Powered Actionable Insights]**.

---

## 💡 The Problem

Important information gets buried in:

* 📝 Messy meeting notes
* 💬 Long conversations
* 📄 Project documents
* 📋 Decisions scattered across different sections
* ⏰ Action items that are easy to forget

Reading through everything takes time, and traditional summarization tools often stop at **"here's what happened"**.

But in an enterprise environment, the more important question is:

> **"Okay... what do we do next?"**

---

## 🚀 Our Solution

**Long Story Short** turns unstructured information into an interactive, actionable dashboard.

### 📄 Upload

Upload a document containing meeting notes, project information, or other enterprise content.

### ✨ Summarize

Choose the format that best fits your needs, including summaries focused on:

* Key decisions
* Action items
* Important takeaways
* Executive-level information

### 💬 Ask

Use the built-in chatbot to ask questions about the uploaded document without having to search through it yourself.

### 🎯 Act

Automatically surface actionable next steps, responsibilities, and important decisions so nothing gets lost.

### 🔎 Verify

An accuracy audit provides additional context around the generated insights and highlights information that may require verification.

---

## ⭐ Key Features

| Feature                      | Description                                                                |
| ---------------------------- | -------------------------------------------------------------------------- |
| 📄 **Document Upload**       | Upload PDF, DOCX, PNG, and JPG files                                       |
| 🧠 **AI Summarization**      | Convert long or messy content into concise summaries                       |
| 🎯 **Action Items**          | Identify tasks and next steps from the source material                     |
| 🔑 **Key Decisions**         | Surface important decisions made in meetings or documents                  |
| 💬 ** Chatbot**              | Ask a RAG chatbot questions about the uploaded content                     |
| 🔍 **Accuracy Audit**        | Review generated insights and identify information that should be verified |
| 📑 **Raw Text View**         | Switch between generated insights and the original extracted content       |
| 🎨 **Custom Summary Styles** | Choose the type of summary that best fits your use case                    |

---

## 🖥️ How It Works

```text
                    ┌──────────────────┐
                    │  Upload Document │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Extract & Process    │
                 │      Content         │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌───────────┐  ┌──────────┐
        │ Summary  │  │  Chatbot  │  │  Audit   │
        └────┬─────┘  └─────┬─────┘  └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                  ┌──────────────────┐
                  │ Actionable       │
                  │ Insights &       │
                  │ Next Steps       │
                  └──────────────────┘
```

---

## 🧩 Example

A team uploads messy meeting notes containing:

> discussions about a login bug, database fields, dashboard design, testing, and deadlines

Instead of manually reading through the entire document, **Long Story Short** can surface:

### Key Decisions

* Core functionality takes priority over visual polish.
* Only in-app notifications will be included in the first version.
* The dashboard layout needs to be finalized before development begins.

The information goes from **messy → understandable → actionable**.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **OpenAI API**
* **Azure Document Intelligence API**
* **Retrieval-Augmented Generation (RAG)**
* **Document processing / text extraction**
* **AI-powered summarization and question answering**

---

## 🔐 Responsible AI

Because AI-generated summaries can occasionally miss context or make incorrect assumptions, **Long Story Short** is designed with verification in mind.

The application includes an **Accuracy Audit** to encourage users to review generated information rather than blindly relying on AI output.

The goal isn't to replace human decision-making.

It's to make the information humans need to make those decisions **easier to find**.

---

## 🎯 Why This Matters

Enterprise information is often not difficult to create — it's difficult to **keep track of**.

A single meeting can contain:

**20 minutes of discussion → 5 decisions → 8 action items → 3 deadlines**

And if those details stay buried in a document, they can easily be forgotten.

**Long Story Short** closes that gap by turning unstructured information into a clear path forward.

> **Don't just summarize what happened. Know what happens next.**

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install streamlit python-dotenv openai azure-ai-formrecognizer azure-core
```

### 4. Configure your API key

Create a `.env` file and add your OpenAI API key and Azure API Keys:

```env
OPENAI_API_KEY=your_api_key_here
AZURE_DOC_INTEL_ENDPOINT=your_api_key_here
AZURE_DOC_INTEL_KEY=your_api_key_here
```

> Never commit your API key or `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run updated_chatbot2.py
```

The application will open in your browser.
---

## 👥 Team

Built with ❤️ for the hackathon by:

**Rujul Telavane**
**Shreya Kamath**
**Sumaiya Shaik**
**Mudra Raval**

---

## 🔮 Future Improvements

* 🔗 Support for additional enterprise document sources
* 📅 Automatic deadline and calendar integration
* 👤 Smarter assignment of action items to team members
* 🔔 Notifications for upcoming action items
* 🧠 Improved conversational memory across multiple documents
* 📊 Analytics for recurring decisions and unresolved action items
* 🔐 Enterprise authentication and permission controls


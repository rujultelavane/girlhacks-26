import os

import numpy as np
import faiss

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()

# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Check your .env file."
    )

# Create OpenAI client
client = OpenAI(api_key=api_key)


EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def create_embeddings(chunks):
    """Create an embedding for every document chunk."""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=chunks
    )

    embeddings = np.array(
        [item.embedding for item in response.data],
        dtype="float32"
    )

    return embeddings


def create_vector_store(chunks):
    """Create a FAISS index from document chunks."""

    embeddings = create_embeddings(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, chunks


def retrieve_chunks(question, index, chunks, top_k=4):
    """Find the chunks most relevant to the user's question."""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[question]
    )

    question_embedding = np.array(
        [response.data[0].embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        question_embedding,
        top_k
    )

    retrieved_chunks = []

    for index_position in indices[0]:
        if index_position < len(chunks):
            retrieved_chunks.append(
                chunks[index_position]
            )

    return retrieved_chunks


def answer_question(question, retrieved_chunks, chat_history):
    """Generate an answer using only retrieved document context."""

    context = "\n\n".join(
        [
            f"--- SOURCE {i + 1} ---\n{chunk}"
            for i, chunk in enumerate(retrieved_chunks)
        ]
    )

    system_prompt = """
You are a document question-answering assistant.

Answer the user's question using ONLY the provided document context.

Rules:
1. Do not invent information.
2. If the answer is not contained in the context, say:
   "The document does not contain enough information to answer that."
3. Explain your answer clearly.
4. When possible, identify which source chunk supports your answer.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add previous conversation
    for message in chat_history:
        messages.append(message)

    messages.append(
        {
            "role": "user",
            "content": f"""
DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""
        }
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content
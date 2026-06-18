import os
import logging

import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.document_repository import get_all_documents

logger = logging.getLogger(__name__)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model used for answer generation
model = genai.GenerativeModel("gemini-2.5-flash")

# Embedding model used for semantic document retrieval
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def ask_gemini(question: str):
    try:

        logger.info(f"Question received: {question}")

        # Retrieve relevant documents from knowledge base
        context = retrieve_relevant_document(question)

        if context is None:
            logger.warning("No relevant context found")
            return "I could not find relevant information in the knowledge base."

        logger.info(f"Retrieved context: {context}")

        # Build RAG prompt using retrieved context
        prompt = f"""
        You are a helpful AI assistant.

        Answer only in English.

        Use the context below to answer the question.

        If the context does not contain enough information,
        say:
        "I could not find relevant information in the knowledge base."

        Context:
        {context}

        Question:
        {question}
        """

        logger.info("Sending prompt to Gemini")

        response = model.generate_content(prompt)

        logger.info("Response received from Gemini")

        return response.text

    except Exception as e:

        logger.error(f"Gemini Error: {str(e)}")

        return f"LLM service temporarily unavailable. Error: {str(e)}"


def retrieve_relevant_document(question: str):

    logger.info(f"Searching documents for: {question}")

    documents = get_all_documents()

    if not documents:
        logger.warning("No documents found in database")
        return None

    logger.info(f"Documents found: {len(documents)}")

    document_texts = [doc.content for doc in documents]

    # Generate embeddings for stored documents
    document_vectors = embedding_model.encode(document_texts)

    # Generate embedding for user question
    question_vector = embedding_model.encode([question])

    # Calculate semantic similarity between question and documents
    similarities = cosine_similarity(question_vector, document_vectors)

    max_score = similarities.max()

    logger.info(f"Maximum similarity score: {max_score}")

    # Ignore results with very low similarity
    if max_score < 0.2:
        logger.warning("No relevant document found")
        return None

    # Select top 3 most relevant documents
    top_indices = similarities[0].argsort()[-3:][::-1]

    logger.info(f"Top matching indices: {top_indices}")

    context = "\n".join(document_texts[i] for i in top_indices)

    logger.info("Context prepared successfully")

    return context

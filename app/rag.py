import os
import logging

import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.document_repository import get_all_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(question: str):
    try:

        logger.info(f"Question received: {question}")

        context = retrieve_relevant_document(question)

        logger.info(f"Retrieved context: {context}")

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

        return (
            "LLM service temporarily unavailable. "
            f"Error: {str(e)}"
        )


def retrieve_relevant_document(question: str):

    logger.info(f"Searching documents for: {question}")

    documents = get_all_documents()

    if not documents:
        logger.warning("No documents found in database")
        return "No documents available in the knowledge base."

    logger.info(f"Documents found: {len(documents)}")

    document_texts = [
        doc.content
        for doc in documents
    ]

    vectorizer = TfidfVectorizer()

    document_vectors = vectorizer.fit_transform(
        document_texts
    )

    question_vector = vectorizer.transform(
        [question]
    )

    similarities = cosine_similarity(
        question_vector,
        document_vectors
    )

    logger.info(f"Similarity scores: {similarities}")

    max_score = similarities.max()

    logger.info(f"Maximum similarity score: {max_score}")

    if max_score < 0.1:
        logger.warning("No relevant document found")
        return "No relevant context found."

    top_indices = similarities[0].argsort()[-3:][::-1]

    logger.info(f"Top matching indices: {top_indices}")

    context = "\n".join(
        document_texts[i]
        for i in top_indices
    )

    logger.info("Context prepared successfully")

    return context
from fastapi import FastAPI
from app.schemas import (
    QuestionRequest,
    DocumentRequest,
    QuestionResponse,
    DocumentResponse,
)
from app.rag import ask_gemini
from app.document_repository import save_document
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Assignment API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/documents", response_model=DocumentResponse)
def create_document(request: DocumentRequest):

    logger.info(f"Saving document: {request.content}")

    document = save_document(request.content)

    logger.info(f"Document saved with ID: {document.id}")

    return DocumentResponse(id=document.id, content=document.content)


@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):

    logger.info(f"Question received: {request.question}")

    answer = ask_gemini(request.question)

    logger.info(f"Answer generated successfully")

    return QuestionResponse(question=request.question, answer=answer)

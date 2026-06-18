from fastapi import FastAPI, HTTPException
from app.database import engine
from app.models import Base
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

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    # Health check endpoint
    return {"status": "healthy"}


@app.post("/documents", response_model=DocumentResponse)
def create_document(request: DocumentRequest):

    try:
        # Save document to PostgreSQL database
        document = save_document(request.content)
        logger.info(f"Document saved with ID: {document.id}")

        return DocumentResponse(id=document.id, content=document.content)

    except Exception as e:
        logger.error(str(e))

        raise HTTPException(status_code=500, detail="Failed to save document")


@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):

    logger.info(f"Question received: {request.question}")

    # Generate answer using RAG pipeline
    answer = ask_gemini(request.question)

    logger.info("Answer generated successfully")

    return QuestionResponse(question=request.question, answer=answer)

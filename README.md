# AI Assignment API

A Retrieval-Augmented Generation (RAG) API built using FastAPI, PostgreSQL, Gemini, and Sentence Transformers.

## Features

* Store documents in PostgreSQL
* Retrieve relevant documents using semantic search
* Generate answers using Google's Gemini model
* REST APIs built with FastAPI
* Request and response validation using Pydantic
* Logging for monitoring and debugging
* Health check endpoint

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Gemini 2.5 Flash
* Sentence Transformers
* Scikit-Learn
* Pydantic

## Project Structure

```text
.
├── app
│   ├── database.py
│   ├── document_repository.py
│   ├── main.py
│   ├── models.py
│   ├── rag.py
│   └── schemas.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Setup Instructions

### Clone Repository

```bash
git clone <your-github-repository-url>
cd ai-assignment
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_assignment
GEMINI_API_KEY=your_gemini_api_key
```

### Run Application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

## API Endpoints

### Health Check

**Request**

```http
GET /health
```

**Response**

```json
{
  "status": "healthy"
}
```

### Create Document

**Request**

```http
POST /documents
```

```json
{
  "content": "PostgreSQL is an open-source relational database."
}
```

**Response**

```json
{
  "id": 1,
  "content": "PostgreSQL is an open-source relational database."
}
```

### Ask Question

**Request**

```http
POST /ask
```

```json
{
  "question": "What are the benefits of PostgreSQL?"
}
```

**Response**

```json
{
  "question": "What are the benefits of PostgreSQL?",
  "answer": "PostgreSQL is known for reliability, scalability, extensibility, and is open-source."
}
```

## Retrieval Workflow

1. User submits a question.
2. Documents are retrieved from PostgreSQL.
3. Sentence Transformer generates embeddings.
4. Cosine similarity finds the most relevant documents.
5. Top matching documents are selected as context.
6. Gemini generates the final answer using the retrieved context.

## Future Improvements

* Store embeddings in PostgreSQL
* Add document chunking for large documents
* Integrate a vector database such as FAISS or ChromaDB
* Add authentication and authorization
* Improve retrieval ranking strategies

## Author

Mary Jose
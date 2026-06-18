from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        description="Question to ask the knowledge base",
        example="What is PostgreSQL?",
    )


class DocumentRequest(BaseModel):
    content: str = Field(
        ...,
        description="Document content to store",
        example="PostgreSQL is an open-source relational database.",
    )


class DocumentResponse(BaseModel):
    id: int
    content: str


class QuestionResponse(BaseModel):
    question: str
    answer: str

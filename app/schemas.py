from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class DocumentRequest(BaseModel):
    content: str


class DocumentResponse(BaseModel):
    id: int
    content: str


class QuestionResponse(BaseModel):
    question: str
    answer: str

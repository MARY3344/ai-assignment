from app.database import SessionLocal
from app.models import Document


def save_document(content: str):
    db = SessionLocal()

    try:
        document = Document(content=content)

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    finally:
        db.close()


def get_all_documents():
    db = SessionLocal()

    try:
        return db.query(Document).all()

    finally:
        db.close()
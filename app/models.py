from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Text


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
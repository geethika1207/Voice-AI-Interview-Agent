from sqlalchemy import Column, String, INTEGER, ForeignKey, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship


class USER(Base):
    __tablename__ = "Users"

    id = Column(INTEGER, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))


class Interview(Base):
    __tablename__ = "conversation"

    id = Column(INTEGER, primary_key = True)
    user_id = Column(INTEGER, ForeignKey("Users.id", ondelete = "CASCADE"), nullable = False) 
    title = Column(String, nullable = False)
    topics = Column(String, nullable = False)
    status = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()')) 
    Reviews = relationship("Response", back_populates="submission", cascade="all, delete-orphan")

class Response(Base):
    __tablename__ = "Interview_response"

    id = Column(INTEGER, primary_key = True)
    interview_id = Column(INTEGER, ForeignKey("conversation.id", ondelete = "CASCADE"), nullable = False) 
    question = Column(String, nullable = False)
    difficulty = Column(String, nullable=True)
    answer = Column(String, nullable = True)
    evaluation = Column(String, nullable = True)
    marks = Column(INTEGER, nullable = True)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    submission = relationship("Interview", back_populates="Reviews")

class interview_analysis(Base):
    __tablename__ = "analysis"

    id = Column(INTEGER, primary_key = True)
    interview_id = Column(INTEGER, ForeignKey("conversation.id", ondelete = "CASCADE"), nullable = False) 
    summary = Column(String, nullable=False)
    positive_aspects = Column(JSON, nullable=False)
    suggestions = Column(JSON, nullable=False)
    learning_tags = Column(JSON, nullable=False)
    overall_difficulty = Column(String, nullable=False)
    marks = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
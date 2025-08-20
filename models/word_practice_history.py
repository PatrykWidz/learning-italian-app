from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.connection import Base

# Define the word practice history table mode
class WordPracticeHistory(Base):
    __tablename__ = 'word_practice_history'  # Table name in the database

    # Primary key column, auto-incrementing ID
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Column for the English word
    word_id = Column(Integer, ForeignKey("english_italian_dictionary.id"), nullable=False)

    # Column for the Italian translation
    last_practiced_on = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Column for the word class
    practiced_counter = Column(Integer, nullable=False)

    word = relationship(
        'Dictionary',
        back_populates='practice_history'
    )
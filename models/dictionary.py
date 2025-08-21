from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from db.connection import Base

# Define the Dictionary table model
class Dictionary(Base):
    __tablename__ = 'english_italian_dictionary'  # Table name in the database

    # Primary key column, auto-incrementing ID
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Column for the English word
    english = Column(String(50), nullable=False)

    # Column for the Italian translation
    italian = Column(String(50), nullable=False)

    #Column for the Italian article
    italian_article = Column(String(5), nullable=True)

    # Column for the word classy
    word_class = Column(String(50), nullable=False)

    practice_history = relationship(
        'WordPracticeHistory',
        back_populates='word',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Word: id={self.id}, english={self.english}, italian={self.italian}'

    def __str__(self):
        return f'{self.english} - {self.italian}'

    __table_args__ = (
        UniqueConstraint('english', 'italian', name="uq_english_italian"),
    )
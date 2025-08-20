from sqlalchemy import nullsfirst

from models.dictionary import Dictionary
from sqlalchemy.orm import Session

from models.word_practice_history import WordPracticeHistory


class DictionaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_word(self, english: str, italian: str, word_class: str):
        word_entry = Dictionary(
            english = english,
            italian = italian,
            word_class = word_class
        )
        self.db.add(word_entry)
        self.db.commit()
        return word_entry

    def add_word_list(self, word_list):
        word_entry_list = [Dictionary(**word) for word in word_list]
        self.db.bulk_save_objects(word_entry_list)
        self.db.commit()
        return word_entry_list

    def get_word_by_id(self, word_id):
        return self.db.query(Dictionary).filter(Dictionary.id == word_id).first()

    def get_all_words(self):
        return self.db.query(Dictionary).all()

    def get_all_words_except(self, excluded_word_id_list):
        word_list = self.db.query(Dictionary).where(Dictionary.id.notin_(excluded_word_id_list)).all()
        return word_list

    def get_least_practiced_words(self, word_count):
        word_list = (
            self.db.query(Dictionary)
            .outerjoin(WordPracticeHistory)
            .order_by(
                WordPracticeHistory.practiced_counter.asc(),
                WordPracticeHistory.last_practiced_on.asc())
            .limit(word_count)
            .all()
        )

        return word_list
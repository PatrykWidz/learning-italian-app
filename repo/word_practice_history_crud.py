from sqlalchemy.orm import Session
from models.word_practice_history import WordPracticeHistory
from typing import Union, List

class WordPracticeHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_update_practice_records(self, word_ids: Union[int, List[int]]):

        if isinstance(word_ids, int):

            practice_record = self.db.query(WordPracticeHistory).filter(WordPracticeHistory.word_id == word_ids).first()

            if practice_record:
                practice_record.practiced_counter += 1
            else:
                new_practice_record = WordPracticeHistory(
                    word_id = word_ids,
                    practiced_counter = 1
                )
                self.db.add(new_practice_record)

        elif isinstance(word_ids, list):

            practice_records = self.db.query(WordPracticeHistory).filter( WordPracticeHistory.word_id.in_(word_ids) ).all()
            practice_records_dict = { p.word_id:p for p in practice_records }

            for w_id in word_ids:
                practice_record = practice_records_dict.get(w_id)

                if practice_record:
                    practice_record.practiced_counter += 1
                else:
                    new_practice_record = WordPracticeHistory(
                        word_id=w_id,
                        practiced_counter=1
                    )
                    self.db.add(new_practice_record)

        self.db.commit()
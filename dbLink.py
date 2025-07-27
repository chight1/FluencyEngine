import os
import sqlite3
from datetime import datetime, timedelta

class dbLink:
    def __init__(self, language='japanese', db_file="fluency_progress.db"):
        # Ensure the database file is always relative to the script's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, db_file)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.language = language
        self._initialize_db()

    def is_table_empty(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.language}")
        return self.cursor.fetchone()[0] == 0

    def _initialize_db(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.language} (
                lemma TEXT PRIMARY KEY,
                usages INTEGER DEFAULT 0,
                next_review_date TEXT,
                duplicate_sentences TEXT DEFAULT ''
            )
        """)
        self.conn.commit()

    def update_progress(self, lemma_usages, sentence):
        for lemma, data in lemma_usages.items():
            next_review_date = data['next_review_date']

            self.cursor.execute(f"SELECT duplicate_sentences FROM {self.language} WHERE lemma = ?", (lemma,))
            row = self.cursor.fetchone()
            duplicate_sentences = sentence if not row or not row[0] else f"{row[0]} ||| {sentence}"

            self.cursor.execute(f"""
                INSERT INTO {self.language} (lemma, usages, next_review_date, duplicate_sentences)
                VALUES (?, 1, ?, ?)
                ON CONFLICT(lemma) DO UPDATE SET 
                    usages = usages + 1,
                    next_review_date = excluded.next_review_date,
                    duplicate_sentences = CASE 
                        WHEN usages + 1 >= 10 THEN '' 
                        ELSE excluded.duplicate_sentences 
                    END
            """, (lemma, next_review_date, duplicate_sentences))

        self.conn.commit()

    def get_usages(self, lemma):
        self.cursor.execute(f"SELECT usages FROM {self.language} WHERE lemma = ?", (lemma,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return 0

    def get_unseen_lemmas(self, lemmas):
        placeholders = ','.join('?' for _ in lemmas)
        query = f"SELECT lemma FROM {self.language} WHERE lemma IN ({placeholders})"
        self.cursor.execute(query, lemmas)
        known_lemmas = {row[0] for row in self.cursor.fetchall()}

        unseen = [lemma for lemma in lemmas if lemma not in known_lemmas or self.get_usages(lemma) == 0]
        return set(unseen)

    def get_next_lemma(self):
        current_time = datetime.now().isoformat()

        self.cursor.execute(f"""
            SELECT lemma FROM {self.language}
            WHERE usages > 0 AND next_review_date <= ?
            ORDER BY next_review_date ASC
            LIMIT 1
        """, (current_time,))
        row = self.cursor.fetchone()

        if row:
            return row[0]

        self.cursor.execute(f"""
            SELECT lemma FROM {self.language}
            WHERE usages = 0
            LIMIT 1
        """)
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_total_lemmas(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.language}")
        return self.cursor.fetchone()[0]
    
    def get_learned_lemmas_count(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.language} WHERE usages > 9")
        return self.cursor.fetchone()[0]
    
    def get_learning_lemmas_count(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.language} WHERE usages = 0")
        return self.cursor.fetchone()[0]

    def get_due_lemmas(self):

        current_time = datetime.now().isoformat()
        self.cursor.execute(f"""
            SELECT COUNT(*) FROM {self.language}
            WHERE usages > 0 AND next_review_date <= ?
        """, (current_time,))
        return self.cursor.fetchone()[0]
    
    # Gets a lemma that has been reviewed more than once, to provide a contextually relevant sentence
    def get_reviewing_lemma(self):
        self.cursor.execute(f"""
            SELECT lemma FROM {self.language}
            WHERE usages > 1
            ORDER BY usages ASC
            LIMIT 1
        """)
        row = self.cursor.fetchone()
        return row[0] if row else None



    def delete_lemma(self, lemma):
        self.cursor.execute(f"DELETE FROM {self.language} WHERE lemma = ?", (lemma,))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = dbLink(language='english')

    print("\nDatabase head:")
    db.cursor.execute(f"SELECT * FROM {db.language} LIMIT 50")

    column_names = [description[0] for description in db.cursor.description]
    print(column_names)

    for row in db.cursor.fetchall():
        print(row)

    lang = db.language
    total = db.get_total_lemmas()
    learned = db.get_learned_lemmas_count()
    learning = db.get_learning_lemmas_count()

    db.close()

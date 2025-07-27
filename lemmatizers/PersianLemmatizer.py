import subprocess
import json
from collections import Counter
from .BaseLemmatizer import BaseLemmatizer
import os

class PersianLemmatizer(BaseLemmatizer):
    def __init__(self, language='persian'):
        super().__init__(language)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.python_311_path = os.path.join(current_dir, ".venv", "Scripts", "python.exe")
        self.script_path = os.path.join(current_dir, "persian_subprocess.py")

    def get_lemma_counts(self, text):
        result = subprocess.run(
            [self.python_311_path, self.script_path, text],
            capture_output=True,
            text=True,
            encoding='utf-8'  # explicitly required on Windows
        )

        if result.returncode != 0:
            raise RuntimeError(f"Persian subprocess failed: {result.stderr}")

        lemma_counts = json.loads(result.stdout)
        return Counter(lemma_counts)

if __name__ == "__main__":
    lemmatizer = PersianLemmatizer()
    text = "من کتاب جدیدی می‌خوانم."
    print(lemmatizer.get_lemma_counts(text))
from collections import Counter
import classla
from .base_lemmatizer import BaseLemmatizer

class ClasslaLemmatizer(BaseLemmatizer):
    def __init__(self, language='serbian'):
        super().__init__(language)
        classla.download('sr')  # downloads model once if not downloaded
        self.nlp = classla.Pipeline('sr')

    def get_lemma_counts(self, text):
        lemma_counter = Counter()
        doc = self.nlp(text)
        for sentence in doc.sentences:
            for word in sentence.words:
                lemma = word.lemma.lower()
                if lemma.isalpha():
                    lemma_counter[lemma] += 1
        return lemma_counter

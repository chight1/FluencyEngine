import spacy
import re
from collections import Counter
from .base_lemmatizer import BaseLemmatizer

MODELS = {
    'english': 'en_core_web_sm',
    'japanese': 'ja_core_news_sm',
    'russian': 'ru_core_news_sm',
    'spanish': 'es_core_news_sm',
    'french': 'fr_core_news_sm',
    'german': 'de_core_news_sm',
    'portuguese': 'pt_core_news_sm',
}

class SpacyLemmatizer(BaseLemmatizer):
    def __init__(self, language):
        super().__init__(language)
        if language not in MODELS:
            raise ValueError(f"Unsupported spaCy language: {language}")
        self.nlp = spacy.load(MODELS[language])

    def get_lemma_counts(self, text):
        lemma_counter = Counter()
        doc = self.nlp(text)
        if self.nlp.lang in ['ja', 'zh']:
            for token in doc:
                if token.is_alpha and not re.match(r'[A-Za-z0-9]', token.text):
                    lemma_counter[token.lemma_] += 1
        else:
            for token in doc:
                if token.is_alpha:
                    lemma_counter[token.lemma_.lower()] += 1
        return lemma_counter

if __name__ == "__main__":
    # Example usage
    lemmatizer = SpacyLemmatizer('english')
    text = "The cats are running and the dog is running too."
    lemma_counts = lemmatizer.get_lemma_counts(text)
    print(lemma_counts.most_common(5))
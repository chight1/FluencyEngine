from collections import Counter

class BaseLemmatizer:
    def __init__(self, language):
        self.language = language

    def get_lemma_counts(self, text):
        raise NotImplementedError("Must override get_lemma_counts")

    def create_frequency_list(self, text, top_n=None):
        counts = self.get_lemma_counts(text)
        return counts.most_common(top_n) if top_n else counts

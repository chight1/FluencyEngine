from .spacy_lemmatizer import SpacyLemmatizer
from .persian_lemmatizer import PersianLemmatizer
from .serbian_lemmatizer import ClasslaLemmatizer
from .chinese_lemmatizer import ChineseLemmatizer
from .kazakh_lemmatizer import KazakhLemmatizer

def get_lemmatizer(language):
    lemmatizers = {
        'japanese': SpacyLemmatizer,
        'chinese': ChineseLemmatizer,
        'serbian': ClasslaLemmatizer,
        'kazakh': KazakhLemmatizer,
        'persian': PersianLemmatizer,
        'english': SpacyLemmatizer,
        'russian': SpacyLemmatizer,
        'spanish': SpacyLemmatizer,
        'french': SpacyLemmatizer,
        'german': SpacyLemmatizer,
        'portuguese': SpacyLemmatizer,
    }
    lemmatizer_class = lemmatizers.get(language.lower())
    
    if not lemmatizer_class:
        raise ValueError(f"No lemmatizer available for language '{language}'.")
    
    return lemmatizer_class()
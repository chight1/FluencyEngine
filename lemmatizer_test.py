from lemmatizers import get_lemmatizer

# lemmatizer = get_lemmatizer('english')
# text = "I am reading a new book."
# print(lemmatizer.get_lemma_counts(text))

# hazm_lemmatizer = get_lemmatizer('persian')
# persian_text = "من کتاب جدیدی می‌خوانم."
# print(hazm_lemmatizer.get_lemma_counts(persian_text))

# classla_lemmatizer = get_lemmatizer('serbian')
# serbian_text = "Moja mama voli da peva."
# print(classla_lemmatizer.get_lemma_counts(serbian_text))
# print(classla_lemmatizer.get_lemma_counts(serbian_text))
# print(classla_lemmatizer.get_lemma_counts(serbian_text))

# chinese_lemmatizer = get_lemmatizer('chinese')
# chinese_text = "我喜欢学习新的语言。"
# print(chinese_lemmatizer.get_lemma_counts(chinese_text))

kazakh_lemmatizer = get_lemmatizer('kazakh')
kazakh_text = "Мен жаңа кітап оқып жатырмын."
print(kazakh_lemmatizer.get_lemma_counts(kazakh_text))
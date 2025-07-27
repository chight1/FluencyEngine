import sys
import json
from hazm import Lemmatizer, word_tokenize
from collections import Counter

def main(text):
    lemmatizer = Lemmatizer()
    tokens = word_tokenize(text)
    lemma_counter = Counter()

    for token in tokens:
        lemma = lemmatizer.lemmatize(token)
        if lemma.isalpha():
            lemma_counter[lemma] += 1

    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(lemma_counter, ensure_ascii=False))

if __name__ == "__main__":
    text = sys.argv[1]
    main(text)

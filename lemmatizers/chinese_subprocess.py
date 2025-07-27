import sys
import json
import spacy
from collections import Counter

# Load spaCy's Chinese language model
nlp = spacy.load("zh_core_web_sm")

# Count lemmas (tokens) in text
def get_lemma_counts(text):
    doc = nlp(text)
    return Counter(token.text for token in doc if token.is_alpha)


# Main execution
def main(text):
    lemma_counter = get_lemma_counts(text)

    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(lemma_counter, ensure_ascii=False))

if __name__ == "__main__":
    input_text = sys.argv[1]
    main(input_text)

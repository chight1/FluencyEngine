#WIP
import sys
import json
from collections import Counter
from ufal.udpipe import Model, Pipeline

# Load UDPipe Kazakh model
model = Model.load("kazakh-ktb-ud-2.5-191206.udpipe")
pipeline = Pipeline(model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")

# Count lemmas in text
def get_lemma_counts(text):
    processed = pipeline.process(text)
    lemma_counter = Counter()

    for line in processed.split("\n"):
        if line and not line.startswith("#"):
            parts = line.split("\t")
            if len(parts) > 2:
                lemma = parts[2].lower()
                if lemma.isalpha():
                    lemma_counter[lemma] += 1
    return lemma_counter

# Main execution
def main(text):
    lemma_counter = get_lemma_counts(text)
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(lemma_counter, ensure_ascii=False))

if __name__ == "__main__":
    input_text = sys.argv[1]
    main(input_text)

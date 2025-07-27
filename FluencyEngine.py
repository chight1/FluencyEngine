import os
import time
from dbLink import dbLink
from ttsLink import speak_sentence
from textHelpers import get_helper_text
from gptLink import get_practice_sentence, get_definitions, translate
from datetime import datetime, timedelta
from lemmatizers import get_lemmatizer


SUPPORTED_LANGUAGES = ["japanese", "chinese", "english", "russian", "spanish", "french", "german", "portuguese",
                       "arabic", "hindi", "indonesian", "malay", "turkish", "vietnamese", "serbian", "persian", "kazakh"]

def get_next_sentence(db, language, lemmatizer):
    """
    Fetch the next sentence based on the learning status of lemmas.
    """
    next_lemma = db.get_next_lemma()
    reviewing_lemma = db.get_reviewing_lemma()
    practice_sentence = get_practice_sentence(language, next_lemma, db.get_total_lemmas(), reviewing_lemma)
    # Lemmatize explicitly once here
    lemma_counts = lemmatizer.get_lemma_counts(practice_sentence)

    return {
        'sentence': practice_sentence,
        'lemma_counts': lemma_counts,
        'cur_lemma': next_lemma,
        'reviewing_lemma': reviewing_lemma,
    }


def update_progress(db, sentence, difficulty, lemma_counts):
    difficulties = {'easy': 1.3, 'medium': 1.0, 'hard': 0.7}
    base_intervals = [1, 3, 7, 14, 30, 60]

    lemma_updates = {}
    for lemma, lemma_count in lemma_counts.items():
        current_usages = db.get_usages(lemma)
        review_count = min(current_usages, len(base_intervals) - 1)
        interval_days = base_intervals[review_count]

        modified_interval = interval_days * difficulties[difficulty]
        next_review_date = datetime.now() + timedelta(days=modified_interval)

        lemma_updates[lemma] = {
            'count': lemma_count,
            'next_review_date': next_review_date.isoformat()
        }

    db.update_progress(lemma_updates, sentence)


def run_learning_session(db, language):
    try:
        lemmatizer = get_lemmatizer(language)
    except ValueError as e:
        print(e)
        print("Please select another language.")
        return  # Return to main to re-select language

    print(f"Initialized lemmatizer for {language}.")
    print(f"Running learning session for '{language}'...")

    # Rest of your original function...

    lemmatizer = get_lemmatizer(language)
    print(f"Initialized lemmatizer for {language}.")
    print(f"Running learning session for '{language}'...")

    option_text = (
        "\nOptions:\n"
        "  [r] - Repeat audio\n"
        "  [t] - Show English translation\n"
        "  [p] - Show pronunciation\n"
        "  [d] - Show definitions\n"
        "  [1] - Easy\n"
        "  [2] - Medium\n"
        "  [3] - Hard\n"
        "  [exit] - Exit session\n"
        "  [Enter] - Skip to next sentence\n"
    )

    while True:
        cur_sentence_data = get_next_sentence(db, language, lemmatizer)
        cur_sentence = cur_sentence_data['sentence']
        lemma_counts = cur_sentence_data['lemma_counts']
        cur_lemma = cur_sentence_data['cur_lemma']
        partially_learned_lemma = cur_sentence_data['reviewing_lemma']
        unseen_lemmas = db.get_unseen_lemmas(list(lemma_counts.keys()))

        definitions = get_definitions(unseen_lemmas, language).replace('\n\n', '\n')
        cur_sentence_with_definitions = f"{definitions}\n\n{cur_sentence}" if definitions else cur_sentence
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"lemma_counts: {lemma_counts}")
        print(f"Current lemma: {cur_lemma}")
        print(f"Lemma for difficulty context: {partially_learned_lemma}")
        print(cur_sentence_with_definitions)
        speak_sentence(cur_sentence, language=language)

        actions = {
            'r': lambda: speak_sentence(cur_sentence, language=language),
            't': lambda: print(f"Translation: {translate(cur_sentence, language, 'English')}"),
            'p': lambda: print(f"Pronunciation: {get_helper_text(cur_sentence, language, 'pronunciation')}"),
            'd': lambda: print(get_definitions(lemma_counts.keys(), language).replace('\n\n', '\n') + '\n\n' + cur_sentence),
            '1': lambda: update_progress(db, cur_sentence, 'easy', lemma_counts),
            '2': lambda: update_progress(db, cur_sentence, 'medium', lemma_counts),
            '3': lambda: update_progress(db, cur_sentence, 'hard', lemma_counts),
            'del': lambda: db.delete_lemma(cur_lemma),
        }

        while True:
            user_input = input(f"{option_text}\nChoose an option: ").strip().lower()
            os.system('cls' if os.name == 'nt' else 'clear')

            if user_input == '':
                break
            elif user_input == 'exit':
                print("Learning session ended by user.")
                return
            elif user_input in actions:
                if user_input not in ['1', '2', '3', 'd']:
                    print(cur_sentence_with_definitions)
                actions[user_input]()
                if user_input in ['1', '2', '3', 'del']:
                    break # Exit the inner loop after updating progress to move to the next sentence
            else:
                print("Invalid option. Choose again.")


def main():
    while True:
        try:
            print("Select a language:")
            for idx, lang in enumerate(SUPPORTED_LANGUAGES, 1):
                db_temp = dbLink(lang)
                total = db_temp.get_total_lemmas()
                learned = db_temp.get_learned_lemmas_count()
                learning = db_temp.get_learning_lemmas_count()
                due = db_temp.get_due_lemmas()
                print(f"{idx}. {lang.capitalize()}\t(Total: {total}, Learned: {learned}, Learning: {learning}, Due: {due})")
                db_temp.close()

            choice = int(input("Enter the number corresponding to your choice: "))

            if 1 <= choice <= len(SUPPORTED_LANGUAGES):
                language = SUPPORTED_LANGUAGES[choice - 1]
                db = dbLink(language=language)
                run_learning_session(db, language)
                db.close()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error occurred: {e}. Please try again.")



if __name__ == "__main__":
    main()
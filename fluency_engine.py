import os
import time
from db_link import dbLink
from tts_link import speak_sentence
from text_helpers import get_helper_text
from gpt_link import get_practice_sentence, get_definitions, translate
from datetime import datetime, timedelta
from lemmatizers import get_lemmatizer
from db_backup import upload_backup


SUPPORTED_LANGUAGES = ["japanese", "chinese", "english", "russian", "spanish", "french", "german", "portuguese",
                       "arabic", "hindi", "indonesian", "malay", "turkish", "vietnamese", "serbian", "persian", "kazakh"]

# Get the next sentence based on if the user is reviewing a lemma or not
def get_next_sentence(db, language, lemmatizer):
    next_lemma = db.get_next_lemma()
    reviewing_lemma = db.get_reviewing_lemma()
    practice_sentence = get_practice_sentence(language, next_lemma, db.get_total_lemmas(), reviewing_lemma)
    lemma_counts = lemmatizer.get_lemma_counts(practice_sentence)

    return {
        'sentence': practice_sentence,
        'lemma_counts': lemma_counts,
        'cur_lemma': next_lemma,
        'reviewing_lemma': reviewing_lemma,
    }

# Upsert the progress of the user based on their input
# Updates the next review date based on the difficulty selected
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

# Handle diplaying menu options and executing actions
def handle_menu_display(user_input, actions, sentence_displayed):
    if user_input in actions:
        os.system('cls' if os.name == 'nt' else 'clear')
        if user_input not in ['1', '2', '3', 'del', 'd']:
            print(sentence_displayed)
        actions[user_input]() # Translation etc goes after the sentence is displayed
        return user_input in ['1', '2', '3', 'del']
    print("Invalid option. Choose again.")
    return False


# Run the learning session for the selected language
# This is the main loop that will keep running until the user decides to exit
def run_learning_session(db, language):
    try:
        lemmatizer = get_lemmatizer(language)
    except ValueError as e:
        print(e)
        print("Please select another language.")
        return  # Return to main to re-select language

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
        "  [menu] - Return to main menu\n"
        "  [exit] - Backup and close application\n"
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
            'd': lambda: print(cur_sentence_with_definitions),
            '1': lambda: update_progress(db, cur_sentence, 'easy', lemma_counts),
            '2': lambda: update_progress(db, cur_sentence, 'medium', lemma_counts),
            '3': lambda: update_progress(db, cur_sentence, 'hard', lemma_counts),
            'del': lambda: db.delete_lemma(cur_lemma),
        }

        while True:
            user_input = input(f"{option_text}\nChoose an option: ").strip().lower()

            if user_input == '':
                break
            if user_input == 'menu':
                print("Returning to main menu.")
                return
            if user_input == 'exit':
                print("Backing up database and exiting.")
                upload_backup()
                exit()

            should_break = handle_menu_display(user_input, actions, cur_sentence_with_definitions)
            if should_break:
                break

# Entry point for selecting languages and initiating learning sessions.
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
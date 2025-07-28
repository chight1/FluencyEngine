import random
import openai
import os
import json
import bisect

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "language_prompts.json"), encoding='utf-8') as f:
    LANGUAGE_PROMPTS = json.load(f)

def prompt(system, user, temp, max_tokens):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temp,
        max_tokens=max_tokens,
    )
    choices = response.choices
    if not choices:
        raise RuntimeError("No response received from OpenAI.")
    return choices[0].message.content

skill_lemma_thresholds = [
    50, 100, 200, 350, 500, 750, 1000, 1500, 2000, 
    2500, 3000, 4000, 5000, 6500, 8000, 10000, 
    12500, 15000, 17500, 20000
]

skill_levels = [
    "Absolute Beginner",
    "Novice",
    "Beginner",
    "Upper Beginner",
    "Elementary",
    "Upper Elementary",
    "Lower Intermediate",
    "Intermediate",
    "Upper Intermediate",
    "Lower Advanced",
    "Advanced",
    "Upper Advanced",
    "Highly Advanced",
    "Lower Expert",
    "Expert",
    "Upper Expert",
    "Near-Native",
    "Lower Near-Native",
    "Upper Near-Native",
    "Native-Like Fluency",
    "Educated Native Fluency"
]

def get_difficulty_level(total_lemmas_seen):
    index = bisect.bisect_right(skill_lemma_thresholds, total_lemmas_seen)
    return skill_levels[min(index, len(skill_levels)-1)] # min to avoid index error when total lemmas is over 20k

def get_practice_sentence(language, lemma=None, lemmas_seen=0, reviewing_lemma=None):
    prompt_list = LANGUAGE_PROMPTS.get(language.lower())
    if prompt_list:
        lang_prompt = random.choice(prompt_list)
    else:
        lang_prompt = f"The user is learning {language}. Provide a unique sentence naturally in context."

    lemma_part = (
        f"The user is currently reviewing the lemma '{lemma}', provide a sentence using '{lemma}' in context."
        if lemma else
        f"The user has just started reviewing the lemma '{reviewing_lemma}'. Do not use '{reviewing_lemma}' in the sentence, but provide a sentence around that level that will definitely show the user one word that is new; don't worry about the word being a little above their level."
    )

    current_skill_level = get_difficulty_level(lemmas_seen)

    system_prompt = (
        f"{lang_prompt}\n{lemma_part}\n"
        f"The sentence must match the user's current skill level of {current_skill_level}. "
        "Always vary the context, phrasing, and scenario. "
        f"Do not include non-{language} words, pronunciation guides, definitions, greetings, or tiny sentences of one or two words. Provide only full sentences."
    )

    user_prompt = "Generate a unique sentence based on the instructions provided."

    temperature = 1.0 if language.lower() == 'english' else 1.1
    max_tokens = 100

    return prompt(system_prompt, user_prompt, temperature, max_tokens)

def translate(sentence, source_language, target_language):
    temperature = 0.5
    max_tokens = 100
    if source_language.lower() == 'english' and target_language.lower() == 'english':
        system_prompt = (
            "You are an expert teacher. "
            f"Explain the following sentence to the user so they can learn about this stuff: '{sentence}'."
        )
        user_prompt = f"Explain this sentence: '{sentence}'."
        temperature = 0.7
        max_tokens = 400
    else:
        system_prompt = (
            f"You are a professional translator. Translate the following {source_language} sentence into {target_language}: '{sentence}'."
            " Do not include any definitions, explanations, or additional context, only the translation."
        )
        user_prompt = f"Translate this sentence: '{sentence}' from {source_language} to {target_language}."

    return prompt(system_prompt, user_prompt, temperature, max_tokens)

def get_definitions(lemmas, language='Japanese'):
    if not lemmas:
        return ""
    lemma_list = ', '.join(f"'{lemma}'" for lemma in lemmas)
    pronunciation_blurb = ""
    if language.lower() == 'japanese':
        pronunciation_blurb = ", furigana,"
    elif language.lower() == 'chinese':
        pronunciation_blurb = ", pinyin,"
    system_prompt = (
        f"You are providing annotations for a language learning app. "
        f"Provide brief English definitions for each of the following {language} word(s): {lemma_list}. "
        f"Include only part of speech{pronunciation_blurb} and clear definition(s) in English. "
        "Do NOT include example sentences. "
        "Return each definition explicitly structured in the format: lemma: (part of speech) definition in English."
    )
    user_prompt = f"Define these words: {lemma_list}."
    temperature = 0.1
    max_tokens = 750

    return prompt(system_prompt, user_prompt, temperature, max_tokens)

if __name__ == "__main__":
    lemma_sentence = get_practice_sentence("Japanese", lemma="新しい")
    print(f"Lemma sentence: {lemma_sentence}")

    general_sentence = get_practice_sentence("Japanese", '', lemmas_seen=0)
    print(f"General sentence: {general_sentence}")

    definitions = get_definitions(["新しい", "言葉", "走る"], "Japanese")
    print("Definitions:")
    print(definitions)

import os
import winsound
import subprocess

import azure.cognitiveservices.speech as speechsdk  # type: ignore

SUPPORTED_LANGUAGES = ["japanese", "chinese", "english", "russian", "spanish", "french", "german", "portuguese",
                       "arabic", "hindi", "indonesian", "malay", "turkish", "vietnamese", "serbian"]

lang_dict = {
    "English": {"language": "en-US", "voice":  "en-US-JennyNeural"},
    # "English": {"language": "en-US", "voice": "en-US-AnaNeural"},
    # "English": {"language": "en-US", "voice": "en-US-AriaNeural"},
    # "English": {"language": "en-US", "voice": "en-US-JaneNeural"},
    "Chinese": {"language": "zh-CN", "voice": "zh-CN-XiaoyiNeural"},
    # "Chinese": {"language": "zh-CN", "voice": "zh-CN-XiaoxiaoNeural"},
    "Japanese": {"language": "ja-JP", "voice": "ja-JP-NanamiNeural"},
    "Russian": {"language": "ru-RU", "voice": "ru-RU-DariyaNeural"},
    "Spanish": {"language": "es-MX", "voice": "es-MX-DaliaNeural"},
    "German": {"language": "de-DE", "voice": "de-DE-KatjaNeural"},
    "Kazakh": {"language": "kk-KZ", "voice": "kk-KZ-AigulNeural"},
    "French": {"language": "fr-FR", "voice": "fr-FR-DeniseNeural"},
    "Portuguese": {"language": "pt-BR", "voice": "pt-BR-FranciscaNeural"},
    "Arabic": {"language": "ar-SA", "voice": "ar-SA-HamedNeural"},
    "Hindi": {"language": "hi-IN", "voice": "hi-IN-AaravNeural"},
    "Indonesian": {"language": "id-ID", "voice": "su-ID-TutiNeural"},
    "Malay": {"language": "ms-MY", "voice": "ta-MY-KaniNeural"},
    "Turkish": {"language": "tr-TR", "voice": "tr-TR-EmelNeural"},
    "Vietnamese": {"language": "vi-VN", "voice": "vi-VN-HoaiMyNeural"},
    "Serbian": {"language": "sr-LATN-RS", "voice": "sr-LATN-RS-SophieNeural"},
    "Persian": {"language": "fa-IR", "voice": "fa-IR-DilaraNeural"},
}

def speak_sentence(sentence, language="English"):
    language = language.capitalize()  # Ensure proper casing
    if language not in lang_dict:
        raise ValueError(f"Unsupported language: {language}")

    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_TTS_API_KEY"),
        region="centralus"
    )
    speech_config.speech_synthesis_language = lang_dict[language]["language"]
    speech_config.speech_synthesis_voice_name = lang_dict[language]["voice"]


    # Synthesize directly to speaker
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)
    result = synthesizer.speak_text_async(sentence).get()
    # only log if the result is not successful
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"TTS failed for '{sentence}' in {language}: {result.reason}")

def play_audio_file(filename):
    if os.name == "nt":
        winsound.PlaySound(filename, winsound.SND_FILENAME)

if __name__ == "__main__":
    # Example usage
    speak_sentence("Hello, this is a test sentence.", language="English")
    speak_sentence("你好，这是一个测试句子。", language="Chinese")
    speak_sentence("こんにちは、これはテスト文です。", language="Japanese")
    speak_sentence("Привет, это тестовое предложение.", language="Russian")
    speak_sentence("Hola, esta es una frase de prueba.", language="Spanish")
    speak_sentence("Hallo, dies ist ein Testsatz.", language="German")
    speak_sentence("Сәлем, бұл тест сөйлемі.", language="Kazakh")
    speak_sentence("Bonjour, ceci est une phrase de test.", language="French")
    speak_sentence("Olá, esta é uma frase de teste.", language="Portuguese")
    speak_sentence("مرحبا، هذه جملة اختبار.", language="Arabic")
    speak_sentence("नमस्ते, यह एक परीक्षण वाक्य है।", language="Hindi")
    speak_sentence("Halo, ini adalah kalimat uji.", language="Indonesian")
    speak_sentence("Halo, ini adalah kalimat uji.", language="Malay")
    speak_sentence("Merhaba, bu bir test cümlesidir.", language="Turkish")
    speak_sentence("Xin chào, đây là một câu thử nghiệm.", language="Vietnamese")
    speak_sentence("Здраво, ово је тест реченица.", language="Serbian")
    speak_sentence("سلام، این یک جمله آزمایشی است.", language="Persian")
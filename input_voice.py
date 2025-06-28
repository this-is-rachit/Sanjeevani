# input_voice.py

import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq
from langdetect import detect

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
STT_MODEL = "whisper-large-v3"

def record_audio(file_path: str, timeout: int = 20, phrase_time_limit: int = None):
    """Record from the default microphone and save as WAV."""
    rec = sr.Recognizer()
    with sr.Microphone() as src:
        logging.info("Adjusting for ambient noise...")
        rec.adjust_for_ambient_noise(src, duration=1)
        logging.info("Please speak now...")
        audio = rec.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)
    wav = audio.get_wav_data()
    # convert and export to WAV
    seg = AudioSegment.from_wav(BytesIO(wav))
    seg.export(file_path, format="wav")
    logging.info(f"Saved recording to {file_path}")

def transcribe_audio_and_detect_language(audio_filepath: str):
    """Return (transcript, lang_code) using Groq STT + langdetect."""
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as fd:
        result = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=fd,
            language=None  # let Whisper auto-detect
        )
    text = result.text.strip()
    lang = detect(text)
    logging.info(f"Transcribed '{text}' (lang: {lang})")
    return text, lang

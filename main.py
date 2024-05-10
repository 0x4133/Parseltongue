import sqlite3
import speech_recognition as sr
from pydub import AudioSegment
import os
from concurrent.futures import ThreadPoolExecutor

# Database setup
def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS speech_data (
        id INTEGER PRIMARY KEY,
        file_name TEXT NOT NULL,
        transcription TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Audio conversion
def convert_wav(wav_path, target_path):
    audio = AudioSegment.from_wav(wav_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(target_path, format="wav", bitrate="256k")

# Speech-to-text
def speech_to_text(wav_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except (sr.UnknownValueError, sr.RequestError):
        return "Error recognizing audio"

# Save data to the database
def save_to_database(db_path, file_name, transcription):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO speech_data (file_name, transcription) VALUES (?, ?)', (file_name, transcription))
    conn.commit()
    conn.close()

# Fetch all records from the database
def fetch_records(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM speech_data')
    records = cursor.fetchall()
    conn.close()
    return records

# Process a single file
def process_single_file(wav_path, db_path):
    print("Processing file:", wav_path)
    target_path = "converted_" + os.path.basename(wav_path)
    convert_wav(wav_path, target_path)
    transcription = speech_to_text(target_path)
    save_to_database(db_path, wav_path, transcription)

# Main function to process files using multithreading
def process_audio_files(directory_path, db_path):
    with ThreadPoolExecutor() as executor:
        for file in os.listdir(directory_path):
            if file.endswith(".wav"):
                wav_path = os.path.join(directory_path, file)
                executor.submit(process_single_file, wav_path, db_path)

# Initialize database
db_path = "speech_data.db"
initialize_db(db_path)

# Process all WAV files in a directory
directory_path = "/Users/aaron/PycharmProjects/sssssnak/wavs"
process_audio_files(directory_path, db_path)

# Fetch and print the database contents
records = fetch_records(db_path)
for record in records:
    print("ID:", record[0], "File Name:", record[1], "Transcription:", record[2])

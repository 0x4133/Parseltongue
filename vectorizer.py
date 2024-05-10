import librosa
import numpy as np
import sqlite3
import pandas as pd
import os

# Function to extract MFCCs from audio file
def extract_mfcc(wav_path, n_mfcc=13):
    y, sr = librosa.load(wav_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    return mfccs_mean

# Initialize database for storing MFCCs
def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mfcc_data (
        id INTEGER PRIMARY KEY,
        file_name TEXT NOT NULL,
        mfccs TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Save MFCCs to database
def save_mfccs_to_db(db_path, file_name, mfccs):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Convert numpy array to string for storage
    mfccs_str = ','.join(map(str, mfccs))
    cursor.execute('INSERT INTO mfcc_data (file_name, mfccs) VALUES (?, ?)', (file_name, mfccs_str))
    conn.commit()
    conn.close()

# Save MFCCs to CSV
def save_mfccs_to_csv(csv_path, file_name, mfccs):
    df = pd.DataFrame([mfccs], columns=[f'mfcc_{i}' for i in range(len(mfccs))])
    df['file_name'] = file_name
    df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)

# Process all WAV files in a directory and store results
def process_audio_files(directory_path, db_path, csv_path=None):
    initialize_db(db_path)
    for file in os.listdir(directory_path):
        if file.endswith(".wav"):
            wav_path = os.path.join(directory_path, file)
            print(f"Processing file: {wav_path}")
            mfccs = extract_mfcc(wav_path)
            save_mfccs_to_db(db_path, wav_path, mfccs)
            if csv_path:
                save_mfccs_to_csv(csv_path, wav_path, mfccs)

# Main function to run the program
def main():
    directory_path = '/Users/aaron/PycharmProjects/sssssnak'
    db_path = 'mfcc_data.db'
    csv_path = 'mfcc_data.csv'
    process_audio_files(directory_path, db_path, csv_path)

if __name__ == "__main__":
    main()

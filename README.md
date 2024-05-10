# Speech-to-Text Transcription and NLP Analysis

This project consists of two Python scripts that work together to transcribe audio files, store the transcriptions in a SQLite database, and perform natural language processing (NLP) tasks on the transcribed data.

## Requirements

- Python 3.x
- SQLite3
- SpeechRecognition
- Pydub
- NLTK
- scikit-learn

## Installation

1. Clone the repository:

```
git clone https://github.com/0x4133/Parseltongue.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

### Script 1: Audio Transcription

1. Place your WAV audio files in the `wavs` directory.

2. Run the `audio_transcription.py` script:

```
python audio_transcription.py
```

The script will process each WAV file in the `wavs` directory, convert it to the required format, transcribe the audio using Google Speech Recognition API, and store the transcriptions in the `speech_data.db` SQLite database.

3. The script will print the contents of the database after processing all the files.

### Script 2: NLP Analysis

1. Make sure you have run the `audio_transcription.py` script and have the `speech_data.db` database file.

2. Run the `nlp_analysis.py` script:

```
python nlp_analysis.py
```

The script will fetch the transcriptions from the `speech_data.db` database, preprocess the data by tokenizing and removing stop words, train a Naive Bayes model using the preprocessed data, and provide a query interface to answer questions based on the transcriptions.

3. Modify the `training_data` variable in the script to provide question-answer pairs for training the model.

4. Test the model by modifying the `query` variable with your desired question and running the script.

## File Structure

- `audio_transcription.py`: Script for audio transcription and database storage.
- `nlp_analysis.py`: Script for NLP analysis and question-answering.
- `wavs/`: Directory to store WAV audio files for transcription.
- `speech_data.db`: SQLite database file to store transcriptions.
- `README.md`: Project documentation.

## Notes

- The audio transcription script uses the Google Speech Recognition API, which requires an active internet connection.
- The NLP analysis script provides a basic example of training a Naive Bayes model using the transcriptions. You can extend and customize the script based on your specific NLP requirements.
- Make sure to handle any errors or exceptions that may occur during the execution of the scripts.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to modify and adapt the scripts according to your needs.

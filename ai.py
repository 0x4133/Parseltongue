import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Database Reading
def fetch_transcriptions(db_path):
    """Fetch transcriptions from the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT transcription FROM speech_data')
    data = [row[0] for row in cursor.fetchall() if row[0] is not None]
    conn.close()
    return data

# Data Preprocessing
def preprocess_data(transcriptions):
    """Preprocess transcription data for NLP tasks."""
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    processed_data = []
    for text in transcriptions:
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        processed_data.append(' '.join(filtered_tokens))
    return processed_data

# Model Training
def train_model(data):
    """Train a model to respond to questions based on the transcriptions."""
    X_train = [pair['question'] for pair in data]  # Example, adjust according to your data
    y_train = [pair['answer'] for pair in data]    # Example, adjust according to your data
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    return model

# Query Interface
def answer_question(model, query):
    """Use the trained model to answer a question."""
    response = model.predict([query])
    return response[0]

# Main function
def main():
    db_path = 'speech_data.db'
    transcriptions = fetch_transcriptions(db_path)
    processed_transcriptions = preprocess_data(transcriptions)

    # Example: You need to create training data pairs manually or by another method
    training_data = [{'question': 'give me a summery of files', 'answer': processed_transcriptions[0]}]

    model = train_model(training_data)

    # Test the model with a question
    query = 'What is commonly said about pets?'
    print("Answer:", answer_question(model, query))

if __name__ == "__main__":
    main()

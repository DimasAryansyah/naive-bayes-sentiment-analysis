from flask import Flask, request, jsonify
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model dan vectorizer yang telah dilatih
nlp = spacy.load("en_core_web_sm")
df = pd.read_csv('Data_Emosi.csv')

def preprocess(text):
    doc = nlp(text)
    filtered_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(filtered_tokens)

df['new'] = df['Comment'].apply(preprocess)
df['Emotion_num'] = df['Emotion'].map({'joy': 0, 'fear': 1, 'anger': 2})

X_train, X_test, y_train, y_test = train_test_split(df['new'], df['Emotion_num'],
                                                    test_size=0.2, random_state=42, stratify=df['Emotion_num'])
vectorizer = TfidfVectorizer()
X_train_cv = vectorizer.fit_transform(X_train)
X_test_cv = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_cv, y_train)

def predict_emotion(comment):
    processed_comment = preprocess(comment)
    comment_vector = vectorizer.transform([processed_comment])
    predicted_emotion = model.predict(comment_vector)
    return predicted_emotion[0]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    comment = data['comment']
    emotion = predict_emotion(comment)
    emotion_map = {0: 'joy', 1: 'fear', 2: 'anger'}
    return jsonify({'emotion': emotion_map[emotion]})

if __name__ == '__main__':
    app.run(debug=True)
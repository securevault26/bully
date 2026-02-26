import os
import re
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ==============================
# Load Resources
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "best_multilabel_model.pkl"))
tfidf = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
label_columns = joblib.load(os.path.join(MODEL_DIR, "label_columns.pkl"))

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


# ==============================
# Text Cleaning Function
# ==============================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]
    return " ".join(words)


# ==============================
# Prediction Function
# ==============================

def predict_multilabel(text):
    cleaned = clean_text(text)
    vectorized = tfidf.transform([cleaned])
    prediction = model.predict(vectorized)[0]

    detected_labels = []

    for label, value in zip(label_columns, prediction):
        if value == 1:
            detected_labels.append(label.replace("_", " ").title())

    print("\n========================================")
    print("Input Text:")
    print(text)
    print("----------------------------------------")

    if detected_labels:
        print("⚠ Toxic Categories Detected:")
        for label in detected_labels:
            print(f"  • {label}")
        print(f"\nTotal Categories Detected: {len(detected_labels)}")
    else:
        print("✅ No Toxic Content Detected")

    print("========================================\n")

    return detected_labels


# ==============================
# Run Directly From Terminal
# ==============================

if __name__ == "__main__":
    while True:
        user_input = input("Enter text (or type 'exit'): ")
        if user_input.lower() == "exit":
            break
        predict_multilabel(user_input)
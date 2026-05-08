import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# File paths
MODEL_FILE = "model.pkl"
VEC_FILE = "vectorizer.pkl"
DATA_FILE = os.path.join("data", "synthetic_cyberbullying_dataset.csv")


def train_and_save_model():
    """Train SVM model on dataset and save model + vectorizer."""
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"❌ Dataset not found at {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['text'])
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = SVC(kernel="linear", probability=True)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model trained. Accuracy: {acc:.4f}")

    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VEC_FILE)
    print("✅ Model and vectorizer saved.")


def load_model():
    """Load saved model & vectorizer. Train if missing."""
    if not (os.path.exists(MODEL_FILE) and os.path.exists(VEC_FILE)):
        print("⚠️ Model files not found. Training new model...")
        train_and_save_model()

    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VEC_FILE)
    print("✅ Model and vectorizer loaded.")
    return model, vectorizer


if __name__ == "__main__":
    train_and_save_model()
    
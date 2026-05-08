import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    # Load dataset
    df = pd.read_csv('synthetic_cyberbullying_dataset.csv')
    
    # Plot label distribution
    plt.figure(figsize=(6,4))
    sns.countplot(x='label', data=df)
    plt.title('Distribution of Labels in Dataset')
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.xticks([0,1], ['Non-Cyberbullying', 'Cyberbullying'])
    plt.show()
    
    # Vectorize text
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train SVM model
    model = SVC(kernel='linear', probability=True)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred, target_names=['Non-Cyberbullying', 'Cyberbullying']))
    
    # Plot training vs validation accuracy
    train_acc = []
    test_acc = []
    fractions = np.linspace(0.1, 1.0, 10)
    for frac in fractions:
        if frac == 1.0:
            X_frac, y_frac = X_train, y_train
        else:
            X_frac, _, y_frac, _ = train_test_split(X_train, y_train, train_size=float(frac), random_state=42)
        model.fit(X_frac, y_frac)
        train_acc.append(model.score(X_frac, y_frac))
        test_acc.append(model.score(X_test, y_test))
    
    plt.figure(figsize=(8,5))
    plt.plot(fractions, train_acc, label='Training Accuracy')
    plt.plot(fractions, test_acc, label='Validation Accuracy')
    plt.title('Model Accuracy vs. Training Data Fraction')
    plt.xlabel('Fraction of Training Data Used')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
    
    # Interactive input for cyberbullying detection
    print("Enter a sentence to detect cyberbullying (type 'exit' to quit):")
    while True:
        user_input = input(">> ")
        if user_input.lower() == 'exit':
            print("Exiting.")
            break
        user_vec = vectorizer.transform([user_input])
        prediction = model.predict(user_vec)[0]
        label = 'Cyberbullying' if prediction == 1 else 'Non-Cyberbullying'
        print(f"Prediction: {label}")

if __name__ == "__main__":
    main()
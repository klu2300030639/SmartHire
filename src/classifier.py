import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from src.preprocessing import clean_text

# Paths for saving models
MODEL_DIR = "models"
CLASSIFIER_PATH = os.path.join(MODEL_DIR, "resume_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

def train_classifier(data_path="data/raw_resumes.csv"):
    """Loads dataset, splits into train/test, trains a TF-IDF + Logistic Regression model, and saves artifacts."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Please generate it first.")
        
    df = pd.read_csv(data_path)
    
    # Preprocess texts
    print("Preprocessing resume texts...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    X = df['cleaned_text']
    y = df['category']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Vectorization
    print("Vectorizing text using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=2500, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Model Training
    print("Training Logistic Regression model...")
    model = LogisticRegression(random_state=42, max_iter=200)
    model.fit(X_train_vec, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    
    # Ensure models directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save artifacts
    with open(CLASSIFIER_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
        
    print(f"Models saved successfully in '{MODEL_DIR}'.")
    return accuracy, report

def predict_category(text):
    """Loads the model & vectorizer, predicts the category and category probabilities for a given raw text."""
    if not os.path.exists(CLASSIFIER_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("Models not found. Training model now...")
        train_classifier()
        
    with open(CLASSIFIER_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
        
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    
    pred_label = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]
    
    # Map probabilities to classes
    classes = model.classes_
    prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}
    
    # Sort probability dictionary
    prob_dict = dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True))
    
    return pred_label, prob_dict

if __name__ == "__main__":
    train_classifier()

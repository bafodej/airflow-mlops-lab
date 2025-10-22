import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "advertising.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "logistic_regression_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"

def load_data():
    """Charge le dataset advertising.csv"""
    print(f"Loading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully. Shape: {df.shape}")
    return df

def preprocess_data(df):
    """Prétraite les données"""
    print("Preprocessing data...")
    df = df.dropna()
    
    if 'Clicked on Ad' in df.columns:
        X = df.drop('Clicked on Ad', axis=1)
        y = df['Clicked on Ad']
    else:
        X = df.select_dtypes(include=[np.number])
        y = np.random.randint(0, 2, len(df))
    
    X = X.select_dtypes(include=[np.number])
    print(f"Features shape: {X.shape}, Target shape: {y.shape}")
    return X, y

def separate_data(X, y, test_size=0.2, random_state=42):
    """Sépare les données en train/test"""
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def build_model(X_train, y_train):
    """Entraîne le modèle"""
    print("Training model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return model

def evaluate_model(model, X_test, y_test):
    """Évalue le modèle"""
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    return accuracy


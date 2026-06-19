# tests/test_model.py
# Step 4: ML Model Testing using pytest

import pytest
import pickle
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split

# ── Load model and data once for all tests ──────────────────
@pytest.fixture(scope="module")
def model_data():
    with open('model/spam_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('model/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    df = pd.read_csv('data/spam.csv', encoding='latin-1')
    df = df[['v1', 'v2']]
    df.columns = ['label', 'message']
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})

    _, X_test, _, y_test = train_test_split(
        df['message'], df['label_num'], test_size=0.2, random_state=42
    )
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)

    return {
        'model': model, 'vectorizer': vectorizer,
        'y_test': y_test, 'y_pred': y_pred,
        'X_test': X_test, 'df': df
    }


# ── TEST 1: Accuracy must be above 95% ──────────────────────
def test_accuracy(model_data):
    acc = metrics.accuracy_score(model_data['y_test'], model_data['y_pred'])
    print(f"\nAccuracy: {acc:.4f}")
    assert acc > 0.95, f"Accuracy too low: {acc:.4f}"


# ── TEST 2: Precision must be above 85% ─────────────────────
def test_precision(model_data):
    precision = metrics.precision_score(model_data['y_test'], model_data['y_pred'])
    print(f"\nPrecision: {precision:.4f}")
    assert precision > 0.85, f"Precision too low: {precision:.4f}"


# ── TEST 3: Recall must be above 70% ────────────────────────
def test_recall(model_data):
    recall = metrics.recall_score(model_data['y_test'], model_data['y_pred'])
    print(f"\nRecall: {recall:.4f}")
    assert recall > 0.70, f"Recall too low: {recall:.4f}"


# ── TEST 4: Model rejects empty messages ────────────────────
def test_empty_message(model_data):
    vec = model_data['vectorizer'].transform([""])
    pred = model_data['model'].predict(vec)
    print(f"\nEmpty message prediction: {'spam' if pred[0]==1 else 'ham'}")
    assert pred[0] == 0, "Empty message should not be classified as spam"


# ── TEST 5: Obvious spam is detected ────────────────────────
def test_obvious_spam(model_data):
    spam_msg = ["FREE! Win $1000 cash prize! Call now! Claim your reward!"]
    vec = model_data['vectorizer'].transform(spam_msg)
    pred = model_data['model'].predict(vec)
    print(f"\nObvious spam prediction: {'spam' if pred[0]==1 else 'ham'}")
    assert pred[0] == 1, "Obvious spam message was not detected!"


# ── TEST 6: Normal message is not spam ──────────────────────
def test_normal_message(model_data):
    normal_msg = ["Hi, are we still meeting tomorrow for lunch?"]
    vec = model_data['vectorizer'].transform(normal_msg)
    pred = model_data['model'].predict(vec)
    print(f"\nNormal message prediction: {'spam' if pred[0]==1 else 'ham'}")
    assert pred[0] == 0, "Normal message incorrectly flagged as spam!"


# ── TEST 7: No missing values in dataset ────────────────────
def test_no_missing_values(model_data):
    missing = model_data['df'].isnull().sum().sum()
    print(f"\nTotal missing values: {missing}")
    assert missing == 0, f"Dataset has {missing} missing values!"


# ── TEST 8: Class imbalance check ───────────────────────────
def test_class_imbalance(model_data):
    counts = model_data['df']['label'].value_counts()
    spam_ratio = counts['spam'] / len(model_data['df'])
    print(f"\nSpam ratio: {spam_ratio:.2%}")
    assert spam_ratio > 0.05, "Spam samples too few — model may be biased!"
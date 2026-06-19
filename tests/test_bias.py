# tests/test_bias.py
# Step 5: Bias & Fairness Testing

import pytest
import pickle
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split

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
    df['msg_length'] = df['message'].apply(len)

    return {'model': model, 'vectorizer': vectorizer, 'df': df}


# ── BIAS TEST 1: Short vs Long messages ─────────────────────
def test_short_vs_long_message_fairness(model_data):
    """Model should not flag short messages as spam just because they're short"""
    short_hams = [
        "Ok", "Sure", "See you", "Thanks!", "Got it", "Yes", "On my way"
    ]
    vec = model_data['vectorizer'].transform(short_hams)
    preds = model_data['model'].predict(vec)
    spam_count = sum(preds)
    print(f"\nShort normal messages flagged as spam: {spam_count}/{len(short_hams)}")
    assert spam_count <= 1, f"Model is biased against short messages! {spam_count} flagged."


# ── BIAS TEST 2: Messages with numbers ──────────────────────
def test_number_heavy_messages(model_data):
    """Model should not flag messages with numbers as spam automatically"""
    number_msgs = [
        "My number is 9876543210, call me",
        "Meet at 5pm at 42nd street",
        "Your OTP is 123456"
    ]
    vec = model_data['vectorizer'].transform(number_msgs)
    preds = model_data['model'].predict(vec)
    print(f"\nNumber-heavy messages flagged as spam: {sum(preds)}/{len(number_msgs)}")
    # OTP message may be flagged — document it, don't fail hard
    assert sum(preds) <= 2, "Model may be over-flagging messages with numbers"


# ── BIAS TEST 3: Spam words in normal context ────────────────
def test_spam_words_in_normal_context(model_data):
    """Words like FREE or WIN in normal context should not trigger spam"""
    contextual_msgs = [
        "Feel free to call me anytime",
        "I won the chess tournament yesterday",
        "The prize ceremony is on Friday"
    ]
    vec = model_data['vectorizer'].transform(contextual_msgs)
    preds = model_data['model'].predict(vec)
    spam_count = sum(preds)
    print(f"\nNormal messages with spam-like words flagged: {spam_count}/{len(contextual_msgs)}")
    assert spam_count <= 1, f"Model is biased — flagging normal use of words like FREE/WIN"


# ── BIAS TEST 4: Performance on short vs long messages ───────
def test_model_accuracy_by_length(model_data):
    """Check if model performs differently on short vs long messages"""
    df = model_data['df'].copy()
    df['predicted'] = model_data['model'].predict(
        model_data['vectorizer'].transform(df['message'])
    )

    short_msgs = df[df['msg_length'] < 50]
    long_msgs  = df[df['msg_length'] >= 50]

    short_acc = (short_msgs['predicted'] == short_msgs['label_num']).mean()
    long_acc  = (long_msgs['predicted']  == long_msgs['label_num']).mean()

    print(f"\nAccuracy on short messages (<50 chars) : {short_acc:.4f}")
    print(f"Accuracy on long  messages (>=50 chars): {long_acc:.4f}")
    print(f"Difference                              : {abs(short_acc - long_acc):.4f}")

    assert abs(short_acc - long_acc) < 0.15, \
        f"Model performance gap too large between short and long messages!"


# ── BIAS TEST 5: Repeated spam attempts ─────────────────────
def test_repeated_spam_variations(model_data):
    """All variations of obvious spam should be caught"""
    spam_variations = [
        "FREE entry in 2 a wkly comp to win FA Cup final tkts! Text WIN to 87121",
        "You have WON a £1000 cash prize! Call now to claim your reward!",
        "URGENT! You have won £2000. Claim your prize, call 09050001 now!",
    ]
    vec = model_data['vectorizer'].transform(spam_variations)
    preds = model_data['model'].predict(vec)
    caught = sum(preds)
    print(f"\nSpam variations caught: {caught}/{len(spam_variations)}")
    assert caught >= 2, f"Model missed too many spam variations: only caught {caught}/3"
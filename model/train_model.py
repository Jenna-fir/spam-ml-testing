import pickle

import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def main() -> None:
	df = pd.read_csv("data/spam.csv", encoding="latin-1")[["v1", "v2"]]
	df.columns = ["label", "message"]

	print(df["label"].value_counts().to_string())
	print("\nMissing values:")
	print(df.isnull().sum().to_string())

	df["label_num"] = df["label"].map({"ham": 0, "spam": 1})

	X_train, X_test, y_train, y_test = train_test_split(
		df["message"], df["label_num"], test_size=0.2, random_state=42
	)

	print(f"\nTraining samples: {len(X_train)}")
	print(f"Testing samples: {len(X_test)}")

	vectorizer = TfidfVectorizer()
	X_train_vec = vectorizer.fit_transform(X_train)
	X_test_vec = vectorizer.transform(X_test)

	model = MultinomialNB()
	model.fit(X_train_vec, y_train)

	y_pred = model.predict(X_test_vec)

	print("\nModel performance:")
	print(f"Accuracy: {metrics.accuracy_score(y_test, y_pred):.4f}")
	print(f"Precision: {metrics.precision_score(y_test, y_pred):.4f}")
	print(f"Recall: {metrics.recall_score(y_test, y_pred):.4f}")
	print(f"F1 score: {metrics.f1_score(y_test, y_pred):.4f}")

	print("\nConfusion matrix:")
	print(metrics.confusion_matrix(y_test, y_pred))

	with open("model/spam_model.pkl", "wb") as model_file:
		pickle.dump(model, model_file)
	with open("model/vectorizer.pkl", "wb") as vectorizer_file:
		pickle.dump(vectorizer, vectorizer_file)

	print("\nModel saved to model/spam_model.pkl")


if __name__ == "__main__":
	main()
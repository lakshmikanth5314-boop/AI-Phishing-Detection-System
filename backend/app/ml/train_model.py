import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from ucimlrepo import fetch_ucirepo
from feature_extraction import extract_features

import os

DATASET_FILE = "backend/app/ml/phishing_dataset.csv"

if os.path.exists(DATASET_FILE):
    print("Loading local phishing dataset...")

    data = pd.read_csv(DATASET_FILE)

    urls = data["URL"]
    labels = data["label"]

else:
    print("Downloading UCI phishing dataset...")

    dataset = fetch_ucirepo(id=967)

    urls = dataset.data.features["URL"]
    labels = dataset.data.targets["label"]

    # Save dataset locally for future training
    local_data = pd.DataFrame({
        "URL": urls,
        "label": labels
    })

    local_data.to_csv(DATASET_FILE, index=False)

    print("Dataset saved locally.")

print("Dataset loaded.")
print("Total URLs:", len(urls))


# Extract the SAME 10 features used by the website
print("Extracting URL features...")

feature_list = []

for url in urls:
    features = extract_features(str(url))
    feature_list.append(features)

X = pd.DataFrame(feature_list)

# Convert labels to integers
y = pd.to_numeric(labels, errors="coerce")

# UCI PhiUSIIL dataset:
# 0 = Phishing
# 1 = Legitimate
#
# Convert to our application convention:
# 0 = Legitimate
# 1 = Phishing
y = 1 - y

# Remove invalid rows
valid_rows = y.notna()

X = X.loc[valid_rows]
y = y.loc[valid_rows].astype(int)


print("Features extracted:", X.shape)
print("Phishing URLs:", (y == 1).sum())
print("Legitimate URLs:", (y == 0).sum())


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Create Random Forest model
print("Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# Train
model.fit(X_train, y_train)


# Test
predictions = model.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

cm = confusion_matrix(y_test, predictions)


print("\n========================================")
print("       MODEL EVALUATION RESULTS")
print("========================================")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1-Score  : {f1 * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Legitimate", "Phishing"]
))

print("Confusion Matrix:")
print(cm)

print("========================================")
# Save model
model_path = "backend/app/ml/phishing_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved as:")
print(model_path)
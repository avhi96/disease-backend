import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
data = pd.read_csv("kidney_disease.csv")

# Drop ID column if exists
if "id" in data.columns:
    data.drop("id", axis=1, inplace=True)

# Convert target column
data["classification"] = data["classification"].map({
    "ckd": 1,
    "notckd": 0
})

# REMOVE rows where target is NaN
data = data.dropna(subset=["classification"])

# Separate target and features
y = data["classification"]
X = data.drop("classification", axis=1)

# Encode categorical columns in features
for column in X.columns:
    if X[column].dtype == "object":
        X[column] = X[column].astype("category").cat.codes

# Fill missing feature values
X.fillna(X.mean(numeric_only=True), inplace=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
with open("kidney_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Kidney disease model trained successfully")

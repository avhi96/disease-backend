import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
data = pd.read_csv("indian_liver_patient.csv")

# Convert gender to numeric
data["Gender"] = data["Gender"].map({"Male": 1, "Female": 0})

# Target column
y = data["Dataset"]
X = data.drop("Dataset", axis=1)

# Fill missing values
X.fillna(X.mean(numeric_only=True), inplace=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
with open("liver_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Liver disease model trained successfully")

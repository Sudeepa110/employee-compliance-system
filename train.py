import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("employee-policy-compliance-dataset.csv")

# Drop unnecessary columns
df = df.drop(['Employee_ID', 'Name', 'Non_Compliance_Reason'], axis=1)

# Encode target variable
df['Policy_Compliance'] = df['Policy_Compliance'].map({'Yes': 1, 'No': 0})

# Handle month (convert to number if in string form)
if df['Month'].dtype == 'object':
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df['Month'] = df['Month'].map(month_map)

# Features and labels
X = df.drop('Policy_Compliance', axis=1)
y = df['Policy_Compliance']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "compliance_model.pkl")
print("✅ Model trained and saved as compliance_model.pkl")

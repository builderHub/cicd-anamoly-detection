import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

# Fetch latest Jenkins build data
os.system("python3 fetch_jenkins_data.py")

# Load dataset
df = pd.read_csv("resources/all_jenkins_builds.csv")

# Features: job name, build duration, previous failures, test pass percentage
X = df[['build_duration', 'previous_failures', 'test_pass_rate']]
y = df['build_status']  # 1 = Success, 0 = Failure

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "resources/anomaly_detector.pkl")

print("✅ ML model trained using all Jenkins jobs' data!")


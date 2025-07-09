import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config

def train_model():
    # Get configuration
    config = get_config()
    secrets = config.secrets
    
    # Load data
    df = pd.read_csv(secrets.DATA_FILE_NAME)
    
    # Prepare features and target
    X = df[secrets.FEATURE_COLUMNS]
    y = df[secrets.TARGET_COLUMN].map(secrets.TARGET_MAPPING)

    # Train model
    model = RandomForestClassifier(n_estimators=secrets.RANDOM_FOREST_ESTIMATORS)
    model.fit(X, y)

    # Save model
    joblib.dump(model, secrets.MODEL_FILE_NAME)
    print("Model trained and saved successfully")

if __name__ == "__main__":
    train_model()
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib # For saving/loading models
import os
from config import Config

class MLRiskModel:
    def __init__(self, model_path=Config.RISK_MODEL_PATH):
        self.model = None
        self.model_path = model_path
        self.feature_columns = None # Store feature names used during training

    def train_model(self, X_train, y_train, feature_names):
        """
        Trains a classification model.
        X_train: DataFrame of features
        y_train: Series of target labels (e.g., 'Approved', 'Declined', 'High_Risk')
        feature_names: List of column names used as features
        """
        print("Training ML Risk Model...")
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        self.feature_columns = feature_names
        print("Model training complete.")

    def evaluate_model(self, X_test, y_test):
        if self.model is None:
            print("Model not trained or loaded.")
            return
        predictions = self.model.predict(X_test)
        print("\nML Model Evaluation:")
        print(classification_report(y_test, predictions))
        print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")

    def predict_risk(self, features_dict):
        if self.model is None:
            print("Model not trained or loaded. Cannot predict.")
            return "UNKNOWN_RISK"

        # Convert input features to a DataFrame in the correct order
        input_df = pd.DataFrame([features_dict])
        
        # Ensure all training features are present, fill missing with 0 or mean
        # This is a critical step for real-world robustness
        for col in self.feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0 # Or a default value based on your data

        # Select and order features correctly
        input_df = input_df[self.feature_columns]

        prediction = self.model.predict(input_df)[0]
        probability = self.model.predict_proba(input_df)[0]
        
        # Map prediction to a more readable format if needed
        # (e.g., if '0' is 'Low Risk', '1' is 'High Risk')
        return {
            "predicted_label": prediction,
            "probabilities": dict(zip(self.model.classes_, probability))
        }

    def save_model(self):
        if self.model:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            print(f"Model saved to {self.model_path}")

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            # In a real model, you'd also save/load self.feature_columns
            # For this example, assume features are known or derived dynamically
            print(f"Model loaded from {self.model_path}")
            return True
        print(f"No model found at {self.model_path}")
        return False

# Example Training (You'd do this in a separate notebook or script)
# from sklearn.preprocessing import LabelEncoder
#
# # Dummy Data for demonstration
# data = {
#     'text_square_footage': [1500, 2000, 1200, 3000, 1800],
#     'text_year_built': [1990, 2010, 1960, 2005, 1975],
#     'text_roof_condition_classified': ['good', 'good', 'poor', 'good', 'fair'],
#     'image_num_defects': [0, 0, 3, 1, 2],
#     'multimodal_roof_conflict': [False, False, False, False, True],
#     'combined_property_condition_score': [4, 4, 1, 3, 2],
#     'risk_label': ['LOW_RISK', 'LOW_RISK', 'HIGH_RISK', 'MEDIUM_RISK', 'HIGH_RISK']
# }
# df = pd.DataFrame(data)
#
# # One-hot encode categorical features
# df = pd.get_dummies(df, columns=['text_roof_condition_classified'], drop_first=True)
#
# # Prepare data for ML model
# X = df.drop('risk_label', axis=1)
# y = df['risk_label']
#
# # Store feature names before splitting to ensure consistency
# feature_names = X.columns.tolist()
#
# X_train_ml, X_test_ml, y_train_ml, y_test_ml = train_test_split(X, y, test_size=0.3, random_state=42)
#
# ml_model = MLRiskModel()
# ml_model.train_model(X_train_ml, y_train_ml, feature_names)
# ml_model.evaluate_model(X_test_ml, y_test_ml)
# ml_model.save_model()
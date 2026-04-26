import numpy as np
from sklearn.metrics import classification_report, accuracy_score

def evaluate_model(model, X_test, y_test):
    print("Evaluating model...")
    y_pred_test_raw = model.predict(X_test)
    
    # Convert IF outputs (-1 anomaly, 1 normal) to our format (1 anomaly, 0 normal)
    y_pred_test = np.where(y_pred_test_raw == -1, 1, 0)
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred_test, target_names=["Normal", "Anomaly"]))
    print(f"Accuracy: {accuracy_score(y_test, y_pred_test):.4f}")

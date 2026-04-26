import os
import joblib
from data_loader import load_data
from preprocess import preprocess_data
from train import train_model
from evaluate import evaluate_model

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    df_train, df_test = load_data()
    X_train_p, X_test_p, y_train, y_test, preprocessor = preprocess_data(df_train, df_test)

    model = train_model(X_train_p, y_train)
    evaluate_model(model, X_test_p, y_test)
    
    # Save artifacts
    model_path = os.path.join(MODEL_DIR, "model_v1.pkl")
    preprocessor_path = os.path.join(MODEL_DIR, "preprocessor.pkl")
    
    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    
    print(f"Saving preprocessor to {preprocessor_path}...")
    joblib.dump(preprocessor, preprocessor_path)
    
    print("ML Pipeline completed successfully.")

if __name__ == "__main__":
    main()

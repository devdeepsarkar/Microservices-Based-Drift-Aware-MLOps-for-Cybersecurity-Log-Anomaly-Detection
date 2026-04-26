import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

CATEGORICAL_COLS = ["protocol_type", "service", "flag"]

def preprocess_data(df_train, df_test):
    print("Preprocessing data...")
    
    columns = df_train.columns.tolist()
    numeric_cols = [c for c in columns if c not in CATEGORICAL_COLS + ["label", "difficulty_level"]]

    # We map 'normal' -> 0, others -> 1 (Anomaly)
    y_train = (df_train["label"] != "normal").astype(int)
    y_test = (df_test["label"] != "normal").astype(int)
    
    X_train = df_train.drop(columns=["label", "difficulty_level"])
    X_test = df_test.drop(columns=["label", "difficulty_level"])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL_COLS)
        ])
    
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    return X_train_processed, X_test_processed, y_train, y_test, preprocessor

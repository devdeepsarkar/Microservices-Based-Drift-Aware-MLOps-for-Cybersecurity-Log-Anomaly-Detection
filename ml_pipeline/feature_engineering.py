def apply_feature_engineering(X_train_processed, X_test_processed):
    """
    Apply any custom feature engineering here.
    For now, Isolation Forest works well on standard preprocessed data,
    so this acts as a passthrough.
    """
    print("Applying feature engineering...")
    return X_train_processed, X_test_processed

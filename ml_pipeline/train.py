from sklearn.ensemble import IsolationForest

def train_model(X_train):
    print("Training Isolation Forest...")
    # IsolationForest outputs 1 for normal, -1 for anomalies
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X_train)
    return model

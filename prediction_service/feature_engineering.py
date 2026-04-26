"""
feature_engineering.py
-----------------------
Defines the AdvancedFeatureEngineer transformer used inside the preprocessor.pkl pipeline.

This file is a mirror of ml_pipeline/feature_engineering.py.
It is required here so joblib can locate the class definition when
loading preprocessor.pkl — no feature engineering logic is executed
directly from this file in the prediction service.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class AdvancedFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom scikit-learn transformer that applies domain-specific feature
    engineering to the NSL-KDD cybersecurity dataset:

    1. Log Transform — Applies np.log1p() to src_bytes and dst_bytes.
    2. Byte Ratio   — Creates a 'byte_ratio' feature (dst_bytes / src_bytes)
                      as a data exfiltration signal.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        if not isinstance(X_new, pd.DataFrame):
            X_new = pd.DataFrame(X_new)

        if 'src_bytes' in X_new.columns:
            X_new['src_bytes'] = np.log1p(X_new['src_bytes'].astype(float))
        if 'dst_bytes' in X_new.columns:
            X_new['dst_bytes'] = np.log1p(X_new['dst_bytes'].astype(float))

        if 'src_bytes' in X_new.columns and 'dst_bytes' in X_new.columns:
            X_new['byte_ratio'] = (
                X_new['dst_bytes'].astype(float) /
                (X_new['src_bytes'].astype(float) + 1.0)
            )

        return X_new

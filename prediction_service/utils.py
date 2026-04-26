import os
import csv
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_storage", "logs.csv")

def log_prediction(features, prediction):
    """
    Logs the prediction to data_storage/logs.csv.
    Format: features..., prediction, timestamp
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        row = list(features) + [prediction, datetime.utcnow().isoformat()]
        writer.writerow(row)

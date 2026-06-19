import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest

# load data
df = pd.read_csv("data/train_test_network.csv")

fitur = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "src_ip_bytes",
    "dst_ip_bytes"
]

X = df[fitur]

# model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# pastikan folder ada
os.makedirs("models", exist_ok=True)

# simpan model (INI YANG WAJIB NYAMBUNG)
joblib.dump(model, "models/anomaly_model (1).pkl")

print("TRAINING DONE + MODEL SAVED")
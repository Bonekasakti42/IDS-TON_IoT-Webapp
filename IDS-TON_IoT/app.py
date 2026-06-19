import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

st.set_page_config(
    page_title="IDS TON-IoT",
    layout="wide"
)

st.title(
    "Intrusion Detection System (TON-IoT)"
)

# ==========================
# LOAD MODEL TRAINING
# ==========================

model = joblib.load(
    "models/anomaly_model (1).pkl"
)

# ==========================
# GENERATE 500 SAMPLE
# ==========================

n_sample = 500

start_time = datetime.strptime(
    "16:52",
    "%H:%M"
)

times = [
    (
        start_time +
        timedelta(minutes=i)
    ).strftime("%H:%M")
    for i in range(n_sample)
]

input_df = pd.DataFrame({

    "time": times,

    "duration": np.random.uniform(
        0,
        0.0499,
        n_sample
    ),

    "src_bytes": np.random.uniform(
        0,
        130,
        n_sample
    ),

    "dst_bytes": np.random.uniform(
        0,
        89,
        n_sample
    ),

    "src_ip_bytes": np.random.uniform(
        48,
        415,
        n_sample
    ),

    "dst_ip_bytes": np.random.uniform(
        0,
        134,
        n_sample
    )

})

# ==========================
# MODEL INPUT
# ==========================

X = input_df[

    [
        "duration",
        "src_bytes",
        "dst_bytes",
        "src_ip_bytes",
        "dst_ip_bytes"
    ]

]

# ==========================
# PREDICTION
# ==========================

pred = model.predict(X)

prediction = np.where(
    pred == -1,
    "Attack",
    "Normal"
)

result_df = pd.DataFrame({

    "time": input_df["time"],

    "prediction": prediction

})

# ==========================
# LABEL 1
# ==========================

st.header(
    "Input Data (500 Sample)"
)

st.dataframe(
    input_df,
    use_container_width=True,
    height=400
)

# ==========================
# LABEL 2
# ==========================

st.header(
    "Prediction Result"
)

st.dataframe(
    result_df,
    use_container_width=True,
    height=400
)

# ==========================
# SUMMARY
# ==========================

attack = (
    result_df["prediction"]
    ==
    "Attack"
).sum()

normal = (
    result_df["prediction"]
    ==
    "Normal"
).sum()

col1, col2 = st.columns(2)

col1.metric(
    "Attack",
    attack
)

col2.metric(
    "Normal",
    normal
)
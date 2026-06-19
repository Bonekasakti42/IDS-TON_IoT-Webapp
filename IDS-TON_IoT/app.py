import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="IDS TON-IoT",
    layout="wide"
)

st.title("🛡️ Intrusion Detection System (TON-IoT)")

# ==================================================
# LOAD MODEL
# ==================================================

try:
    model = joblib.load(
        "models/anomaly_model (1).pkl"
    )

except Exception as e:

    st.error(
        f"Model tidak ditemukan: {e}"
    )

    st.stop()

# ==================================================
# SAMPLE RANGE
# ==================================================

sample_size = st.selectbox(
    "Sample Range",
    [100, 500, 1000],
    index=1
)

# ==================================================
# TRAINING STATISTICS
# ==================================================

st.subheader(
    "📊 Training Statistics"
)

stats_df = pd.DataFrame({

    "Feature":[
        "duration",
        "src_bytes",
        "dst_bytes",
        "src_ip_bytes",
        "dst_ip_bytes"
    ],

    "Mean":[
        7.854521,
        341297.7,
        304782.5,
        745.43194,
        1121.93852
    ],

    "Std":[
        590.575304,
        17041360,
        15753010,
        19906.24796,
        19633.98622
    ],

    "Q1 (25%)":[
        0,
        0,
        0,
        48,
        0
    ],

    "Median (50%)":[
        0.000164,
        0,
        0,
        82,
        40
    ],

    "Q3 (75%)":[
        0.049943,
        130,
        89,
        415,
        134
    ]

})

st.dataframe(
    stats_df,
    use_container_width=True
)

st.divider()

# ==================================================
# GENERATE SIMULATION DATA
# ==================================================

start_time = datetime.strptime(
    "16:52",
    "%H:%M"
)

times = [

    (
        start_time +
        timedelta(minutes=i)
    ).strftime("%H:%M")

    for i in range(sample_size)

]

input_df = pd.DataFrame({

    "time": times,

    "duration": np.random.uniform(
        0,
        0.049943,
        sample_size
    ),

    "src_bytes": np.random.uniform(
        0,
        130,
        sample_size
    ),

    "dst_bytes": np.random.uniform(
        0,
        89,
        sample_size
    ),

    "src_ip_bytes": np.random.uniform(
        48,
        415,
        sample_size
    ),

    "dst_ip_bytes": np.random.uniform(
        0,
        134,
        sample_size
    )

})

# ==================================================
# ATTACK INJECTION
# ==================================================

attack_index = np.random.choice(
    sample_size,
    int(sample_size * 0.10),
    replace=False
)

input_df.loc[
    attack_index,
    "src_bytes"
] *= np.random.randint(
    20,
    100
)

input_df.loc[
    attack_index,
    "dst_bytes"
] *= np.random.randint(
    20,
    100
)

input_df.loc[
    attack_index,
    "src_ip_bytes"
] *= np.random.randint(
    5,
    20
)

input_df.loc[
    attack_index,
    "dst_ip_bytes"
] *= np.random.randint(
    5,
    20
)

# ==================================================
# LABEL 1
# INPUT DATA
# ==================================================

st.subheader(
    f"📡 Simulation Data ({sample_size} Samples)"
)

st.dataframe(
    input_df,
    height=350,
    use_container_width=True
)

# ==================================================
# DETECTION
# ==================================================

if st.button(
    "🚀 Run Detection"
):

    X = input_df[

        [
            "duration",
            "src_bytes",
            "dst_bytes",
            "src_ip_bytes",
            "dst_ip_bytes"
        ]

    ]

    prediction = model.predict(X)

    result_df = pd.DataFrame({

        "time":
        input_df["time"],

        "prediction":
        np.where(
            prediction == -1,
            "🚨 Attack",
            "✅ Normal"
        )

    })

    # ==============================================
    # SUMMARY
    # ==============================================

    attack_count = (
        result_df["prediction"]
        ==
        "🚨 Attack"
    ).sum()

    normal_count = (
        result_df["prediction"]
        ==
        "✅ Normal"
    ).sum()

    attack_rate = (
        attack_count /
        sample_size
    ) * 100

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "🚨 Attack",
        attack_count
    )

    col2.metric(
        "✅ Normal",
        normal_count
    )

    col3.metric(
        "📊 Attack Rate",
        f"{attack_rate:.2f}%"
    )

    st.divider()

    # ==============================================
    # ALERT
    # ==============================================

    if attack_count > 0:

        st.error(
            f"🚨 {attack_count} ATTACK DETECTED"
        )

    else:

        st.success(
            "✅ No Attack Detected"
        )

    # ==============================================
    # LABEL 2
    # PREDICTION RESULT
    # ==============================================

    st.subheader(
        "🚨 Prediction Result"
    )

    st.dataframe(
        result_df,
        height=350,
        use_container_width=True
    )

    st.divider()

    # ==============================================
    # TRAFFIC TREND
    # ==============================================

    st.subheader(
        "📈 Traffic Trend"
    )

    trend_df = pd.DataFrame({

        "time":
        input_df["time"],

        "traffic":
        (
            input_df["src_bytes"]
            +
            input_df["dst_bytes"]
        )

    })

    st.line_chart(
        trend_df.set_index(
            "time"
        )
    )

    st.divider()

    # ==============================================
    # ATTACK TIMELINE
    # ==============================================

    st.subheader(
        "🕒 Attack Timeline"
    )

    attack_df = result_df[
        result_df["prediction"]
        ==
        "🚨 Attack"
    ]

    st.dataframe(
        attack_df,
        use_container_width=True
    )

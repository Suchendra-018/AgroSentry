"""
==========================================================
File: session_history_service.py
Project: AgroSentry

Description:
    Per-session prediction history for the Streamlit app.
    Stores history in st.session_state, which Streamlit keeps
    private and separate per browser session, instead of the
    single shared outputs/history.csv used by history_service.py
    (which every visitor would otherwise be able to see).
==========================================================
"""

from datetime import datetime

import pandas as pd
import streamlit as st


HISTORY_COLUMNS = [
    "Timestamp",
    "Image Name",
    "Crop",
    "Disease",
    "Confidence",
    "Prediction Type",
    "Status",
]

SESSION_KEY = "session_prediction_history"


def _ensure_initialized():
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = []


def save_prediction(
    image_name,
    crop,
    disease,
    confidence,
    prediction_type="Disease Detection",
    status="Success",
):
    _ensure_initialized()

    st.session_state[SESSION_KEY].append(
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Image Name": image_name,
            "Crop": crop,
            "Disease": disease,
            "Confidence": round(float(confidence), 2),
            "Prediction Type": prediction_type,
            "Status": status,
        }
    )


def get_history_dataframe():
    _ensure_initialized()

    if not st.session_state[SESSION_KEY]:
        return pd.DataFrame(columns=HISTORY_COLUMNS)

    return pd.DataFrame(st.session_state[SESSION_KEY])


def get_statistics():
    history = get_history_dataframe()

    if history.empty:
        return {
            "total_predictions": 0,
            "healthy_predictions": 0,
            "diseased_predictions": 0,
            "average_confidence": 0,
        }

    healthy = history[
        history["Disease"].str.contains("healthy", case=False, na=False)
    ]

    return {
        "total_predictions": len(history),
        "healthy_predictions": len(healthy),
        "diseased_predictions": len(history) - len(healthy),
        "average_confidence": round(history["Confidence"].mean(), 2),
    }


def clear_history():
    st.session_state[SESSION_KEY] = []

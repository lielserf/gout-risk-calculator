import streamlit as st
import pickle
import numpy as np

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Gout Risk Calculator",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============ CUSTOM STYLES ============
st.markdown(
    """
    <style>
    body {
        background-color: #f9fdf9;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton button {
        background-color: #00a88f;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        border: none;
    }
    .stButton button:hover {
        background-color: #008d77;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============ TITLE & INTRO ============
st.markdown("<h1 style='color:#00a88f;text-align:center;'>Gout Risk Calculator</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align:center; font-size:16px;'>
    Please enter the patient’s details below to estimate the probability of developing a gout flare.
    </p>
    """,
    unsafe_allow_html=True
)

# ============ INPUT FORM ============
with st.form("gout_form"):
    serum_urate = st.slider(
        "Serum urate level (mg/dL)", 
        6.8, 20.0, 8.0, step=0.1
    )
    age = st.slider(
        "Age (years)", 
        14, 100, 20, step=1
    )

    hyperlipidemia = st.select_slider(
        "Hyperlipidemia", 
        options=["No", "Yes"], 
        value="No"
    )
    nsaids = st.select_slider(
        "Non-Steroidal Anti-Inflammatory Drugs (NSAIDs) use", 
        options=["No", "Yes"], 
        value="No"
    )
    diuretics = st.select_slider(
        "Diuretics use", 
        options=["No", "Yes"], 
        value="No"
    )

    submit = st.form_submit_button("Predict Risk")

# ============ PREDICTION ============
if submit:
    with open("pickle_model.pkl", "rb") as f:
        model = pickle.load(f)

    X = np.array([[
        serum_urate,
        age,
        1 if hyperlipidemia == "Yes" else 0,
        1 if nsaids == "Yes" else 0,
        1 if diuretics == "Yes" else 0
    ]])

    # Probabilities (if model supports predict_proba)
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0][1]
        st.success(f"Estimated probability of developing a gout flare: **{prob:.2%}**")
    else:
        pred = model.predict(X)[0]
        st.success(f"Predicted outcome: {pred}")

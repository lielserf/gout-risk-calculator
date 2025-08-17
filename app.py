import streamlit as st
import pickle
import numpy as np


# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Gout Risk Calculator - Clalit Health Services",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============ CUSTOM STYLES ============
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        direction: ltr;
    }
    
    /* רקע כללי */
    .stApp {
        background: linear-gradient(135deg, 
            #f0f8ff 0%,     /* Alice Blue */
            #e6f3ff 25%,    /* Light Blue */
            #f0fff4 50%,    /* Honeydew */
            #f5fffa 75%,    /* Mint Cream */
            #f0f8ff 100%);  /* Alice Blue */
        min-height: 100vh;
    }
    
    /* קונטיינר ראשי */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem auto;
        max-width: 800px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* כותרת */
    .main-title {
        background: linear-gradient(135deg, #1e88e5, #26c6da, #43a047);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* כותרת משנה */
    .subtitle {
        text-align: center;
        color: #455a64;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* לוגו קופת חולים */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .logo {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #1976d2, #26c6da);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
    }
    
    /* פורם */
    .stForm {
        background: rgba(245, 251, 255, 0.7);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(33, 150, 243, 0.1);
        margin: 1rem 0;
    }
    
    /* תוויות */
    .stSlider > label {
        color: #37474f !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* הסתרת checkbox */
    .stCheckbox {
        display: none;
    }
    
    /* סליידרים */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #e3f2fd, #e0f2f1) !important;
    }
    
    .stSlider .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #1976d2, #43a047) !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3) !important;
    }
    
    /* כפתור */
    .stButton button {
        background: linear-gradient(135deg, #1976d2 0%, #26c6da 50%, #43a047 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 6px 20px rgba(25, 118, 210, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(25, 118, 210, 0.4) !important;
    }
    
    /* תוצאה */
    .result-container {
        background: linear-gradient(135deg, rgba(232, 245, 233, 0.8), rgba(227, 242, 253, 0.8));
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(67, 160, 71, 0.2);
        text-align: center;
    }
    
    .result-title {
        color: #2e7d32;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .result-percentage {
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
        background: linear-gradient(135deg, #1976d2, #43a047);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* פס סיכון */
    .risk-bar-container {
        margin: 1.5rem 0;
        background: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 10px;
    }
    
    .risk-bar {
        height: 35px;
        border-radius: 20px;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .risk-label {
        font-weight: 500;
        color: #455a64;
        margin-bottom: 0.5rem;
    }
    
    /* הודעת אזהרה */
    .disclaimer {
        background: rgba(255, 249, 196, 0.8);
        border: 1px solid rgba(255, 193, 7, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 2rem;
        text-align: center;
        color: #f57c00;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* התאמה למובייל */
    @media (max-width: 768px) {
        .main-container {
            margin: 0.5rem;
            padding: 1.5rem;
        }
        
        .main-title {
            font-size: 2.2rem;
        }
        
        .result-percentage {
            font-size: 2.5rem;
        }
    }
    
    /* Toggle Switch */
    .toggle-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 10px;
        border: 1px solid rgba(33, 150, 243, 0.1);
    }
    
    .toggle-label {
        font-weight: 600;
        color: #37474f;
        font-size: 1rem;
        flex: 1;
    }
    
    .toggle-help {
        font-size: 0.85rem;
        color: #78909c;
        margin-top: 0.25rem;
    }
    
    .toggle-switch {
        position: relative;
        width: 50px;
        height: 26px;
        margin-left: 1rem;
    }
    
    .toggle-switch input[type="checkbox"] {
        opacity: 0;
        width: 0;
        height: 0;
    }
    
    .toggle-slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: #cfd8dc;
        border-radius: 26px;
        transition: all 0.3s ease;
        border: 1px solid #b0bec5;
    }
    
    .toggle-slider:before {
        position: absolute;
        content: "";
        height: 20px;
        width: 20px;
        left: 3px;
        top: 2px;
        background: white;
        border-radius: 50%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .toggle-switch input:checked + .toggle-slider {
        background: #42a5f5;
        border-color: #1976d2;
    }
    
    .toggle-switch input:checked + .toggle-slider:before {
        transform: translateX(24px);
    }
    
    .toggle-switch:hover .toggle-slider {
        box-shadow: 0 0 8px rgba(66, 165, 245, 0.3);
    }
    
    .toggle-switch input:focus + .toggle-slider {
        box-shadow: 0 0 0 2px rgba(66, 165, 245, 0.5);
    }

    /* נגישות */
    .stSlider:focus-within {
        outline: 2px solid #1976d2;
        outline-offset: 2px;
        border-radius: 8px;
    }
    
    .toggle-switch input:focus + .toggle-slider {
        outline: 2px solid #1976d2;
        outline-offset: 2px;
    }
    
    .stButton button:focus {
        outline: 3px solid rgba(25, 118, 210, 0.5) !important;
        outline-offset: 2px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============ HEADER ============
st.markdown(
    """
    <div class="main-container">
        <div class="logo-container">
            <div class="logo">
                🏥 Clalit Health Services
            </div>
        </div>
        
        <h1 class="main-title">Gout Risk Calculator</h1>
        
        <p class="subtitle">
            Please enter the patient's details to estimate the probability of developing a gout flare
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============ INPUT FORM ============
with st.form("gout_form", clear_on_submit=False):
    st.markdown("### 📋 Patient Details")
    
    serum_urate = st.slider(
        "Serum urate level (mg/dL)", 
        min_value=6.8, 
        max_value=20.0, 
        value=8.0, 
        step=0.1,
        help="Normal range: 3.5-7.2 mg/dL"
    )
    
    age = st.slider(
        "Age (years)", 
        min_value=14, 
        max_value=100, 
        value=50, 
        step=1
    )
    
    st.markdown("---")
    st.markdown("**Medical Conditions and Medications:**")
    
    # Toggle switches
    hyperlipidemia = st.checkbox("", key="hyperlipidemia", value=False)
    st.markdown(f"""
    <div class="toggle-container">
        <div>
            <div class="toggle-label">Hyperlipidemia</div>
            <div class="toggle-help">High levels of fats in the blood</div>
        </div>
        <label class="toggle-switch">
            <input type="checkbox" {'checked' if hyperlipidemia else ''} disabled>
            <span class="toggle-slider"></span>
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    nsaids = st.checkbox("", key="nsaids", value=False)
    st.markdown(f"""
    <div class="toggle-container">
        <div>
            <div class="toggle-label">NSAIDs Use</div>
            <div class="toggle-help">Non-Steroidal Anti-Inflammatory Drugs</div>
        </div>
        <label class="toggle-switch">
            <input type="checkbox" {'checked' if nsaids else ''} disabled>
            <span class="toggle-slider"></span>
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    diuretics = st.checkbox("", key="diuretics", value=False)
    st.markdown(f"""
    <div class="toggle-container">
        <div>
            <div class="toggle-label">Diuretics Use</div>
            <div class="toggle-help">Medications that remove excess fluid from the body</div>
        </div>
        <label class="toggle-switch">
            <input type="checkbox" {'checked' if diuretics else ''} disabled>
            <span class="toggle-slider"></span>
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    submit = st.form_submit_button("🔬 Calculate Risk", use_container_width=True)

# ============ PREDICTION ============
if submit:
    try:
        with open("pickle_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # המרת ערכים
        hyperlipidemia_val = 1 if hyperlipidemia else 0
        nsaids_val = 1 if nsaids else 0
        diuretics_val = 1 if diuretics else 0
        
        X = np.array([[
            serum_urate,
            age,
            hyperlipidemia_val,
            nsaids_val,
            diuretics_val
        ]])
        
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X)[0][1]
            percent = float(prob * 100)
            
            # קביעת צבע וטקסט לפי רמת סיכון
            if percent < 25:
                color = "linear-gradient(135deg, #64b5f6, #81c784)"
                risk_text = "Low Risk"
                text_color = "#1565c0"
            elif percent < 50:
                color = "linear-gradient(135deg, #42a5f5, #66bb6a)"
                risk_text = "Low-Moderate Risk"
                text_color = "#0d47a1"
            elif percent < 75:
                color = "linear-gradient(135deg, #2196f3, #1976d2)"
                risk_text = "Moderate-High Risk"
                text_color = "#0d47a1"
            else:
                color = "linear-gradient(135deg, #1976d2, #0d47a1)"
                risk_text = "High Risk"
                text_color = "#0d47a1"
            
            # הצגת התוצאה
            st.markdown(
                f"""
                <div class="result-container">
                    <div class="result-title">Risk Assessment Result</div>
                    <div class="result-percentage">{percent:.1f}%</div>
                    
                    <div class="risk-bar-container">
                        <div class="risk-label">Risk Level: <strong style="color: {text_color};">{risk_text}</strong></div>
                        <div class="risk-bar" style="background: linear-gradient(to right, {color} {percent}%, #e0e0e0 {percent}%);"></div>
                    </div>
                    
                    <div style="color: #455a64; font-size: 0.95rem; line-height: 1.5;">
                        Probability of gout flare based on the given parameters
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            pred = model.predict(X)[0]
            st.success(f"Predicted outcome: {pred}")
            
    except FileNotFoundError:
        st.error("❌ Model file not found. Please ensure 'model.pkl' exists in the same directory.")
    except Exception as e:
        st.error(f"❌ Calculation error: {str(e)}")

# ============ DISCLAIMER ============
st.markdown(
    """
    <div class="disclaimer">
        ⚠️ <strong>Important Notice:</strong> 
        This tool is intended for assistance only and is not a substitute for professional medical advice. 
        Please consult with a physician before making treatment decisions.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

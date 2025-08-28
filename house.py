import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image
import matplotlib.pyplot as plt

# Load model
model = joblib.load("model\lightgbm_model.pkl")

# Page Config
st.set_page_config(page_title="House Price Estimator", layout="wide")

# Init session state
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# Transparent modern nav style
st.markdown("""
    <style>
    .nav-wrapper {
        display: flex;
        justify-content: left;
        gap: 30px;
        margin-top: -20px;
        margin-bottom: 10px;
    }

    .nav-wrapper button {
        all: unset;
        cursor: pointer;
        font-size: 16px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 8px;
        color: #ffffff;
        transition: background 0.3s ease, color 0.3s ease;
    }

    .nav-wrapper button:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #f0f0f0;
    }
    </style>
    <div class="nav-wrapper">
        <form action="" method="get">
            <button name="nav" value="🏠 Home">🏠 Home</button>
            <button name="nav" value="📊 Predict">📊 Predict</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Use new query param method
params = st.query_params
if "nav" in params:
    st.session_state.page = params["nav"]

page = st.session_state.page


# Load Banner
banner = Image.open("data\image.jpg")  # replace with your house image

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 3em;
        font-weight: 700;
        color: #333;
    }
    .sub-title {
        font-size: 1.2em;
        color: #666;
        margin-bottom: 30px;
    }
    .cta-button {
        background-color: #ff7f00;
        color: white;
        font-size: 1.2em;
        padding: 0.5em 2em;
        border: none;
        border-radius: 10px;
    }
    .rounded-img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)


if page == "🏠 Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
            <style>
                .fancy-title {
                    font-family: 'Playfair Display', serif;
                    font-size: 3.8em;
                    color: #ff6600;
                    margin-top: 80px;
                }
            </style>
            <div class="fancy-title">Want to Know Your Home's Worth?</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@600&display=swap" rel="stylesheet">
        <div style='
            font-family: "Playfair Display", sans-serif;
            font-size: 27px;
            color: white;
            font-weight: 600;
            margin-bottom: 30px;
        '>
            Get accurate price predictions based on city, area, and features.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image(banner)

    st.markdown("---")

    st.markdown("### 🔍 How It Works")
    st.write("""
    1. Fill out your home details.
    2. We analyze your inputs using our AI model.
    3. Get the predicted price instantly!
    """)

elif page == "📊 Predict":
    st.markdown('<div id="predict-section"></div>', unsafe_allow_html=True)
    st.title("📊 Predict Your House Price")

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Area (in SqFt)", min_value=100, max_value=10000, value=1200)
        bedrooms = st.number_input("Bedrooms", 1, 10, 3)
        gas = st.selectbox("Gas Connection", [0, 1])
        ac = st.selectbox("Air Conditioning", [0, 1])
        pool = st.selectbox("Swimming Pool", [0, 1])
        backup = st.selectbox("Power Backup", [0, 1])

    with col2:
        clubhouse = st.selectbox("Club House", [0, 1])
        playarea = st.selectbox("Children's Play Area", [0, 1])
        security = st.selectbox("24X7 Security", [0, 1])
        parking = st.selectbox("Car Parking", [0, 1])
        city = st.selectbox("City", ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'])
        location = st.text_input("Location", "Andheri")

    if st.button("💰 Estimate Price"):
        bedroom_to_area = bedrooms / area
        security_parking = security * parking
        area_bin = pd.cut([area], bins=5, labels=['Small', 'Medium', 'Large', 'XL', 'XXL'])[0]

        input_df = pd.DataFrame({
            'Area': [area],
            'No. of Bedrooms': [bedrooms],
            'Price_per_SqFt': [0],  # placeholder
            'Bedroom_to_Area_Ratio': [bedroom_to_area],
            'Gasconnection': [gas],
            'AC': [ac],
            'SwimmingPool': [pool],
            'PowerBackup': [backup],
            'ClubHouse': [clubhouse],
            "Children'splayarea": [playarea],
            '24X7Security': [security],
            'CarParking': [parking],
            'Security_And_Parking': [security_parking],
            'Location': [location],
            'City': [city],
            'Area_Bins': [area_bin]
        })

        prediction = model.predict(input_df)[0]
        st.success(f"🏠 Estimated Price: ₹{prediction:.2f} Lakhs")
        st.balloons()

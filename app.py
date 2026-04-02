import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# ---------- CUSTOM STYLING ----------
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
    }
    .stMetric label {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1 style='text-align: center;'>🌦️ Weather Data Analysis Dashboard</h1>", unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📂 Upload Weather Dataset", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df = df.dropna()

    # ---------- SIDEBAR FILTERS ----------
    st.sidebar.header("🔍 Filters")

    country = st.sidebar.selectbox("Select Country", df["country"].unique())
    filtered_df = df[df["country"] == country]

    location = st.sidebar.selectbox("Select Location", filtered_df["location_name"].unique())
    filtered_df = filtered_df[filtered_df["location_name"] == location]

    # ---------- METRICS ----------
    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Avg Temp (°C)", f"{filtered_df['temperature_celsius'].mean():.2f}")
    col2.metric("🌧️ Max Rainfall (mm)", f"{filtered_df['precip_mm'].max():.2f}")
    col3.metric("💧 Avg Humidity (%)", f"{filtered_df['humidity'].mean():.2f}")

    st.markdown("---")

    # ---------- DATA PREVIEW ----------
    with st.expander("📊 View Dataset"):
        st.dataframe(filtered_df)

    # ---------- GRAPHS ----------
    col4, col5 = st.columns(2)

    # Temperature graph
    with col4:
        st.subheader("🌡️ Temperature Trend")
        fig1, ax1 = plt.subplots()
        ax1.plot(filtered_df["temperature_celsius"], marker='o')
        ax1.set_title("Temperature")
        ax1.set_xlabel("Records")
        ax1.set_ylabel("°C")
        st.pyplot(fig1)

    # Rainfall graph
    with col5:
        st.subheader("🌧️ Rainfall Trend")
        fig2, ax2 = plt.subplots()
        ax2.plot(filtered_df["precip_mm"], marker='o')
        ax2.set_title("Rainfall")
        ax2.set_xlabel("Records")
        ax2.set_ylabel("mm")
        st.pyplot(fig2)

    # ---------- HUMIDITY ----------
    st.subheader("💧 Humidity Trend")
    fig3, ax3 = plt.subplots()
    ax3.plot(filtered_df["humidity"], marker='o')
    ax3.set_title("Humidity")
    ax3.set_xlabel("Records")
    ax3.set_ylabel("%")
    st.pyplot(fig3)

else:
    st.info("👆 Upload a dataset to start analysis")
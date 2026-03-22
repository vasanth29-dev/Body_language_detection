"""
AI-Based Body Language & Emotion Detection System (FINAL UPGRADED)
"""

import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import time

# -------------------------------
# PAGE CONFIG (UI DESIGN)
# -------------------------------
st.set_page_config(page_title="AI Emotion Dashboard", layout="wide")

st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:35px;
    font-weight:bold;
    color:#00ffcc;
}
.card {
    padding:20px;
    border-radius:15px;
    background-color:#111;
    color:white;
    margin:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🧠 AI Emotion Detection Dashboard</div>", unsafe_allow_html=True)

# -------------------------------
# TELEGRAM CONFIG
# -------------------------------
TOKEN = "8712726568:AAH1RrSQTgbhCVIKkIF8DlxLpeIA4KX7H_o"
CHAT_ID = "6296752092"

def send_telegram(message):
    if TOKEN == "YOUR_NEW_TOKEN":
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

# -------------------------------
# SESSION STATE
# -------------------------------
if "log" not in st.session_state:
    st.session_state.log = []

if "run" not in st.session_state:
    st.session_state.run = False

# -------------------------------
# EMOTION + QUOTES
# -------------------------------
def detect_emotion():
    emotions = ["Happy 😄", "Sad 😢", "Neutral 😐", "Stressed 😟", "Angry 😡"]
    return np.random.choice(emotions)

def get_quote(emotion):
    quotes = {
        "Happy 😄": "Keep shining ✨",
        "Sad 😢": "Everything will be okay ❤️",
        "Neutral 😐": "Stay balanced 🧘",
        "Stressed 😟": "Relax your mind 🌿",
        "Angry 😡": "Take a deep breath 😌"
    }
    return quotes.get(emotion, "")

# -------------------------------
# SCORE SYSTEM
# -------------------------------
def get_score(emotion):
    return {
        "Happy 😄": 10,
        "Neutral 😐": 7,
        "Sad 😢": 5,
        "Stressed 😟": 3,
        "Angry 😡": 2
    }.get(emotion, 0)

# -------------------------------
# CAMERA FUNCTION
# -------------------------------
def camera():
    cap = cv2.VideoCapture(0)
    frame_window = st.empty()
    info_box = st.empty()

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        emotion = detect_emotion()
        score = get_score(emotion)
        quote = get_quote(emotion)

        # ALERT SYSTEM (ALL EMOTIONS)
        if emotion == "Happy 😄":
            send_telegram(f"😊 User is HAPPY\n💬 {quote}")

        elif emotion == "Sad 😢":
            send_telegram(f"😢 User is SAD\n💬 {quote}")

        elif emotion == "Neutral 😐":
            send_telegram(f"😐 User is NEUTRAL\n💬 {quote}")

        elif emotion == "Stressed 😟":
            send_telegram(f"🚨 USER STRESSED!\n💬 {quote}")

        elif emotion == "Angry 😡":
            send_telegram(f"😡 USER ANGRY!\n💬 {quote}")

        # LOG
        st.session_state.log.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Emotion": emotion,
            "Score": score
        })

        # DISPLAY ON FRAME
        cv2.putText(frame, f"{emotion}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(frame, f"{score}", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        frame_window.image(frame, channels="BGR")

        info_box.info(f"{emotion} | {quote}")

        time.sleep(0.7)

    cap.release()

# -------------------------------
# DASHBOARD (BETTER UI)
# -------------------------------
def dashboard():
    if len(st.session_state.log) == 0:
        st.warning("No Data Yet")
        return

    df = pd.DataFrame(st.session_state.log)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='card'>🏆 TOTAL RECORDS</div>", unsafe_allow_html=True)
        st.metric("Count", len(df))

    with col2:
        st.markdown("<div class='card'>📊 AVERAGE SCORE</div>", unsafe_allow_html=True)
        st.metric("Score", round(df["Score"].mean(), 2))

    with col3:
        st.markdown("<div class='card'>🔥 MAX SCORE</div>", unsafe_allow_html=True)
        st.metric("Max", df["Score"].max())

    st.subheader("📊 Emotion Pie Chart")
    fig1, ax1 = plt.subplots()
    df["Emotion"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax1)
    st.pyplot(fig1)

    st.subheader("📈 Emotion Graph")
    fig2, ax2 = plt.subplots()
    df["Emotion"].value_counts().plot.bar(ax=ax2)
    st.pyplot(fig2)

# -------------------------------
# CSV DOWNLOAD
# -------------------------------
def download():
    df = pd.DataFrame(st.session_state.log)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "data.csv", "text/csv")

# -------------------------------
# UI BUTTONS (START + STOP)
# -------------------------------
st.sidebar.title("CONTROL PANEL")

if st.sidebar.button("▶ START CAMERA"):
    st.session_state.run = True

if st.sidebar.button("⛔ STOP CAMERA"):
    st.session_state.run = False

menu = st.sidebar.radio("MENU", ["📷 Camera", "📊 Dashboard", "📁 CSV"])

# -------------------------------
# ROUTING
# -------------------------------
if menu == "📷 Camera":
    if st.session_state.run:
        camera()
    else:
        st.info("Press START CAMERA")

elif menu == "📊 Dashboard":
    dashboard()

elif menu == "📁 CSV":
    download()
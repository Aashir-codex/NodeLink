import streamlit as st
import pyrebase
import time
from datetime import datetime

# Firebase Configuration (Yahan apni sahi details daalein)
config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "nodelink-app.firebaseapp.com",
    "databaseURL": "https://nodelink-app-default-rtdb.firebaseio.com",
    "projectId": "nodelink-app",
    "storageBucket": "nodelink-app.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Page Configuration
st.set_page_config(page_title="Node Link", page_icon="🟢", layout="centered")

# CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    .header-banner { background-color: #008069; color: white; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; border-radius: 0px 0px 10px 10px; margin-bottom: 20px; }
    .chat-bubble-sender { background-color: #d9fdd3; padding: 10px; border-radius: 10px 0 10px 10px; margin: 8px 0; float: right; clear: both; max-width: 75%; }
    .chat-bubble-receiver { background-color: #ffffff; padding: 10px; border-radius: 0 10px 10px 10px; margin: 8px 0; float: left; clear: both; max-width: 75%; }
    </style>
""", unsafe_allow_html=True)

# Login Session
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="header-banner">Node Link Authentication</div>', unsafe_allow_html=True)
    phone = st.text_input("Phone Number")
    if st.button("Request OTP"): st.success("OTP '123456' sent!")
    otp = st.text_input("OTP Code", type="password")
    if st.button("Verify"):
        if otp == "123456":
            st.session_state.logged_in = True
            st.session_state.phone = phone
            st.rerun()
else:
    st.markdown('<div class="header-banner">🟢 Node Link</div>', unsafe_allow_html=True)
    
    # Database se messages fetch karein
    messages = db.child("messages").get().val()
    
    chat_container = st.container()
    with chat_container:
        if messages:
            for m_id in messages:
                m = messages[m_id]
                style = "chat-bubble-sender" if m["sender"] == st.session_state.phone else "chat-bubble-receiver"
                st.markdown(f'<div class="{style}">{m["text"]}</div>', unsafe_allow_html=True)

    user_message = st.chat_input("Type a message...")
    if user_message:
        # Firebase mein save karein
        db.child("messages").push({
            "sender": st.session_state.phone,
            "text": user_message,
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

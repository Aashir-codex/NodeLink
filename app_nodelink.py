import streamlit as st
import time
from datetime import datetime

# Page Configuration for Node Link
st.set_page_config(page_title="Node Link", page_icon="🔗", layout="centered")

# Custom CSS styling to mimic a premium chat application theme
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    
    /* Premium Green Header Banner */
    .header-banner {
        background-color: #008069;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border-radius: 0px 0px 10px 10px;
        margin-bottom: 20px;
    }
    
    /* Elegant Chat Speech Bubbles */
    .chat-bubble-sender {
        background-color: #d9fdd3;
        padding: 10px 15px;
        border-radius: 10px 0px 10px 10px;
        margin: 8px 0px;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0px 1px 1px rgba(0,0,0,0.1);
    }
    .chat-bubble-receiver {
        background-color: #ffffff;
        padding: 10px 15px;
        border-radius: 0px 10px 10px 10px;
        margin: 8px 0px;
        max-width: 75%;
        float: left;
        clear: both;
        box-shadow: 0px 1px 1px rgba(0,0,0,0.1);
    }
    .time-stamp {
        font-size: 10px;
        color: #667781;
        text-align: right;
        margin-top: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# ─── SESSION STATE MANAGEMENT ────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "phone_number" not in st.session_state:
    st.session_state.phone_number = ""
if "messages" not in st.session_state:
    # Clean, generic welcome message data
    st.session_state.messages = [
        {"sender": "System Bot", "text": "Welcome to Node Link! Start chatting securely.", "time": "12:00 PM"},
        {"sender": "You", "text": "Awesome, the interface looks incredibly clean!", "time": "12:01 PM"}
    ]

# ─── SCREEN 1: OTP PHONE LOGIN SCREEN ─────────────────────────────────
if not st.session_state.logged_in:
    st.markdown('<div class="header-banner">Node Link Authentication</div>', unsafe_allow_html=True)
    st.subheader("Welcome to Node Link")
    st.write("Enter your mobile phone number to log into your account securely.")
    
    phone = st.text_input("Phone Number", placeholder="+92 300 0000000")
    
    if st.button("Request OTP Verification Code"):
        if len(phone) >= 10:
            st.session_state.phone_number = phone
            st.success("Verification Code '123456' generated for test session access!")
        else:
            st.error("Please enter a valid phone number setup format.")
            
    otp = st.text_input("Enter 6-Digit OTP Code", type="password", placeholder="**")
    
    if st.button("Verify & Open Node Link"):
        if otp == "123456":
            st.session_state.logged_in = True
            st.success("Access authorized!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Invalid Code. Use '123456' for instant access.")

# ─── SCREEN 2: MAIN MULTI-TAB MESSENGER INTERFACE ──────────────────────
else:
    st.markdown('<div class="header-banner">🔗  Node Link</div>', unsafe_allow_html=True)
    
    # Interface core Navigation tabs
    tab_chats, tab_updates, tab_calls, tab_settings = st.tabs([
        "💬 Chats", "🟢 Updates", "📞 Calls", "⚙️ Settings"
    ])
    
    # --- CLEAN MESSAGES STREAM TAB ---
    with tab_chats:
        st.caption(f"Connected Line: {st.session_state.phone_number}")
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                if msg["sender"] == "You":
                    st.markdown(f'<div class="chat-bubble-sender">{msg["text"]}<div class="time-stamp">{msg["time"]} ✔️✔️</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-receiver"><b>{msg["sender"]}:</b><br>{msg["text"]}<div class="time-stamp">{msg["time"]}</div></div>', unsafe_allow_html=True)
        
        st.write("")
        
        # Real-time message entry box
        user_message = st.chat_input("Type a message to link...")
        if user_message:
            now = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({"sender": "You", "text": user_message, "time": now})
            st.rerun()
            
    # --- NEUTRAL STATUS UPDATES TAB ---
    with tab_updates:
        st.subheader("Status Updates")
        st.write("✨ *My Status*")
        st.caption("Share a live snapshot update with contacts")
        st.divider()
        st.write("💬 *Recent Contact Statuses*")
        st.info("User 1 • 25 minutes ago")
        st.info("User 2 • 3 hours ago")
        st.info("User 3 • Yesterday")

    # --- GENERIC CALL LOG TAB ---
    with tab_calls:
        st.subheader("Call Activity Log")
        st.text("📞 User 1 (Incoming Audio) — Today, 7:55 PM")
        st.text("📹 User 2 (Outgoing Video) — Yesterday, 11:36 AM")
        st.text("📞 User 3 (Missed Audio Call) — June 25, 3:56 AM")

    # --- PERSONAL INTERFACE SETTINGS TAB ---
    with tab_settings:
        st.subheader("Profile Customization")
        st.text_input("Profile Display Username", value="Node Link User")
        st.text_area("Profile Tagline Status", value="Available on Node Link Network 🚀")
        
        st.divider()
        if st.button("Secure Logout From Application"):
            st.session_state.logged_in = False

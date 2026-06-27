import streamlit as st
import pyrebase
import time

# Page Responsive Configuration
st.set_page_config(page_title="NodeLink", page_icon="🔗", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ECE5DD; }
    .chat-bubble-user { background-color: #DCF8C6; padding: 12px; border-radius: 12px; margin: 8px; text-align: right; color: black; }
    .chat-bubble-friend { background-color: #FFFFFF; padding: 12px; border-radius: 12px; margin: 8px; text-align: left; color: black; }
    </style>
""", unsafe_allow_html=True)

# Firebase Configuration
config = {
    "apiKey": "AIzaSyD-YourActualKeyHere123",
    "authDomain": "nodelink-app.firebaseapp.com",
    "databaseURL": "https://nodelink-app-default-rtdb.firebaseio.com",
    "projectId": "nodelink-app",
    "storageBucket": "nodelink-app.appspot.com",
}

@st.cache_resource
def init_firebase():
    return pyrebase.initialize_app(config)

firebase = init_firebase()
db = firebase.database()

# ====== DIRECT MAIN PAGE (LOGIN REMOVED) ======
st.title("🔗 NodeLink Hub")
st.write("Welcome! Aap direct chat hub mein hain.")
st.write("---")

# User ID ko manual set karein (Kyunki login hata diya hai)
user_email = "default_user" 
user_node = "default_user"

# Chat Logic
new_friend = st.text_input("Naye Dost ka naam/email:")
if st.button("➕ Add Friend"):
    db.child("users").child(user_node).child("contacts").push(new_friend)
    st.success("Dost add ho gaya!")

contacts_data = db.child("users").child(user_node).child("contacts").get().val()

if contacts_data:
    friends_list = list(contacts_data.values())
    selected_friend = st.selectbox("🎯 Chat kiske sath karni hai?", friends_list)
    
    msg_text = st.text_input("Type message...")
    if st.button("Send 🚀"):
        payload = {"sender": user_email, "text": msg_text, "time": time.strftime('%I:%M %p')}
        db.child("private_chats").child("room_general").push(payload)
        st.rerun()

    # Messages Display
    private_messages = db.child("private_chats").child("room_general").get().val()
    if private_messages:
        for m_id in private_messages:
            m = private_messages[m_id]
            st.markdown(f"<div class='chat-bubble-user'>{m['text']}</div>", unsafe_allow_html=True)

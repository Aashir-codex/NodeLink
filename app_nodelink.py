import streamlit as st
import pyrebase

# --- 1. CONFIGURATION & INITIALIZATION ---
# Hardcoded configuration (Directly inserted)
firebase_config = {
    "apiKey": st.secrets["AIzaSyCHNL6hYcvQjfhh3LqZ8wX0uayvPa0vGYg"],
    "authDomain": st.secrets["nodelink-2824.firebaseapp.com"],
    "databaseURL": st.secrets["https://nodelink-app-default-rtdb.firebaseio.com"],
    "projectId": st.secrets["nodelink-2824"],
    "storageBucket":st.secrets["nodelink-2824.firebasestorage.app"]
}

# Initialize Database
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# --- 2. AUTHENTICATION COMPONENT ---
def render_login():
    st.markdown("###  Node Link Authentication")
    phone = st.text_input("Mobile Number")
    otp = st.text_input("OTP Code", type="password")
    if st.button("Login"):
        if otp == "123456": # Development test code
            st.session_state.logged_in = True
            st.session_state.user = phone
            st.rerun()
        else:
            st.error("Invalid OTP")

# --- 3. CHAT COMPONENT ---
def render_chat(room_id):
    st.markdown(f"### 💬 Room: {room_id}")
    
    # Fetch messages from Firebase
    msgs = db.child("rooms").child(room_id).get().val()
    
    if msgs:
        for m in msgs.values():
            st.chat_message(m["sender"]).write(m["text"])
            
    # Input field
    if prompt := st.chat_input("Type a message..."):
        db.child("rooms").child(room_id).push({
            "sender": st.session_state.user, 
            "text": prompt
        })
        st.rerun()

# --- 4. SETTINGS COMPONENT ---
def render_settings():
    st.subheader("⚙️ Profile Settings")
    st.write(f"Account: {st.session_state.user}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 5. MAIN ORCHESTRATOR (ENTRY POINT) ---
def main():
    st.set_page_config(page_title="Node Link", layout="centered")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        render_login()
    else:
        menu = st.sidebar.radio("Menu", ["Chats", "Settings"])
        
        if menu == "Chats":
            # --- Yahan change karein ---
            st.sidebar.subheader("Private Chat")
            target_user = st.sidebar.text_input("Friend's Phone Number")
            
            if target_user:
                # Private ID banayein
                participants = sorted([st.session_state.user, target_user])
                room_id = f"priv_{participants[0]}_{participants[1]}"
                
                # Ab yahan aapka purana render_chat function call hoga
                render_chat(room_id) 
            else:
                st.info("Enter a phone number to start a private chat.")
        
        else:
            render_settings()

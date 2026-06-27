import streamlit as st
import pyrebase
import time

# Page Responsive Configuration (Mobile + PC friendly)
st.set_page_config(page_title="FocusChat Pro", page_icon="💬", layout="centered")

# WhatsApp Light Green and Attractive Styling
st.markdown("""
    <style>
    .stApp { background-color: #ECE5DD; }
    .chat-bubble-user { background-color: #DCF8C6; padding: 12px; border-radius: 12px; margin: 8px; text-align: right; color: black; box-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
    .chat-bubble-friend { background-color: #FFFFFF; padding: 12px; border-radius: 12px; margin: 8px; text-align: left; color: black; box-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #128C7E !important; color: white !important; border-radius: 8px; }
    .stButton>button:hover { background-color: #075E54 !important; }
    </style>
""", unsafe_view_html=True)

# ====== GOOGLE FIREBASE CONFIGURATION (100% FREE) ======
config = {
    "apiKey": "AIzaSyD-YourActualKeyHere123",
    "authDomain": " nodelink-app.firebaseapp.com",
    "databaseURL": "https://nodelink-app-default-rtdb.firebaseio.com",
    "projectId": "nodelink-app",
    "storageBucket":  "nodelink-app.appspot.com",
}

@st.cache_resource
def init_firebase():
    return pyrebase.initialize_app(config)

firebase = init_firebase()
auth = firebase.auth()
db = firebase.database()

# App State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ====== SCREEN 1: UNIVERSAL LOGIN PORTAL ======
if not st.session_state.logged_in:
    st.title("🕊️ FocusChat Universal Login")
    st.subheader("Sign Up ya Log In karein (Apne Mobile ya PC se)")
    
    email = st.text_input("Email Address / Username:")
    password = st.text_input("Password (Kam se kam 6 characters):", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In", use_container_width=True):
            try:
                auth.sign_in_with_email_and_password(email, password)
                st.session_state.user_email = email
                st.session_state.user_node = email.replace(".", "_")
                st.session_state.logged_in = True
                st.rerun()
            except:
                st.error("Ghalat Email ya Password! Pehle Account Banayein.")
    with col2:
        if st.button("Create New Account", use_container_width=True):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("🎉 Account kamyabi se ban gaya! Ab Log In dabayein.")
            except:
                st.error("Account nahi ban saka. Email sahi likhein ya Password thoda bada rakhein.")

# ====== SCREEN 2: WHATSAPP PRIVATE CHAT HUB ======
else:
    # Top Action Bar
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("💬 FocusChat Hub")
    with col_logout:
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
    st.write(f"Logged in as: **{st.session_state.user_email}**")
    st.write("---")
    
    # 500 CONTACTS MANAGEMENT ENGINE
    contacts_data = db.child("users").child(st.session_state.user_node).child("contacts").get().val()
    current_count = len(contacts_data) if contacts_data else 0
    
    # Live Visual Counter (Upgraded to 500 Max)
    st.metric(label="👥 Aapke Kul Dost (Contacts Limit)", value=f"{current_count} / 500")
    
    # Add New Friend Section
    new_friend = st.text_input("Naye Dost Ka Email Likh Kar Add Karein:")
    if st.button("➕ Add Friend to List"):
        if current_count >= 500:
            st.error("🚨 500 Contacts ki limit poori ho gayi hai! Kisi purane dost ko delete karein.")
        elif new_friend == st.session_state.user_email:
            st.warning("Aap khud ko add nahi kar sakte!")
        elif new_friend:
            f_node = new_friend.replace(".", "_")
            # Save friend connection to Cloud DB
            db.child("users").child(st.session_state.user_node).child("contacts").child(f_node).set(new_friend)
            st.success(f"🎉 {new_friend} aapki list mein add ho gaya!")
            time.sleep(1)
            st.rerun()

    st.write("---")

    # PRIVATE CHAT SELECTION & ENGINE
    if contacts_data:
        # Dropdown list doston ko select karne ke liye (WhatsApp Chat List ki tarah)
        friends_list = list(contacts_data.values())
        selected_friend = st.selectbox("🎯 Kiske sath chat karni hai? (Select Friend):", friends_list)
        
        # Trash/Delete button to free up space (500 counter manager)
        friend_node_to_del = selected_friend.replace(".", "_")
        if st.button("🗑️ Delete This Contact"):
            db.child("users").child(st.session_state.user_node).child("contacts").child(friend_node_to_del).remove()
            st.success("Contact delete ho gaya, counter update ho jayega!")
            time.sleep(1)
            st.rerun()
            
        st.write(f"### 🔒 Private Room with: {selected_friend.split('@')[0]}")
        
        # Unique Room ID Generation (Alphabetically sorted to match both users)
        friend_clean_node = selected_friend.replace(".", "_")
        room_nodes = sorted([st.session_state.user_node, friend_clean_node])
        chat_room_id = f"room_{room_nodes[0]}_{room_nodes[1]}"
        
        # Fetch and Display Real-time Private Messages
        private_messages = db.child("private_chats").child(chat_room_id).get().val()
        
        chat_container = st.container()
        with chat_container:
            if private_messages:
                for m_id in private_messages:
                    m = private_messages[m_id]
                    if m['sender'] == st.session_state.user_email:
                        st.markdown(f"<div class='chat-bubble-user'><b>You ({m['time']}):</b><br>{m['text']}</div>", unsafe_view_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-friend'><b>{m['sender'].split('@')[0]} ({m['time']}):</b><br>{m['text']}</div>", unsafe_view_html=True)
            else:
                st.info("Abhi tak koi purani chat nahi hai. Pehla message bhejiye!")

        # Message Input & Send Mechanism
        msg_text = st.text_input("Type your message here...", key="private_msg_input")
        if st.button("Send Secure Message 🚀"):
            if msg_text.strip() != "":
                payload = {
                    "sender": st.session_state.user_email,
                    "text": msg_text,
                    "time": time.strftime('%I:%M %p')
                }
                db.child("private_chats").child(chat_room_id).push(payload)
                st.rerun()
    else:
        st.info("Aapki contact list khali hai. Upar email daal kar apne doston ko add karein (Max 500)!")

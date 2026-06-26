import streamlit as st
import pyrebase

config = {
    "apiKey": "AIzaSyCHNL6hYcvQjfhh3LqZ8wX0uayvPa0vGYg",
    "authDomain": "nodelink-2824.firebaseapp.com",
    "databaseURL": "https://nodelink-2824-default-rtdb.firebaseio.com/",
    "projectId": "nodelink-2824",
    "storageBucket": "nodelink-2824.firebasestorage.app",
    "messagingSenderId": "37706221130",
    "appId": "1:37706221130:web:446738beb2b0b40eaa08b3"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

st.title("🔗 NodeLink Chat")
name = st.text_input("Apna Naam Likhein:")
message = st.text_input("Paigham Likhein:")

if st.button("Send"):
    data = {"name": name, "message": message}
    db.child("messages").push(data)
    st.success("Message Sent!")

st.subheader("Messages:")
try:
    all_messages = db.child("messages").get()
    for msg in all_messages.each():
        m = msg.val()
        st.write(f"**{m['name']}**: {m['message']}")
except:
    st.write("Abhi koi message nahi hai.")
st.subheader("Connecting Hearts, Sharing Happiness")

import requests
import streamlit as st
import os

FLASK_HOST = os.environ['FLASK_HOST']
FLASK_HOST_PORT = os.environ['FLASK_HOST_PORT']

st.title("Chat using RAG")

gen_url = "http://" + FLASK_HOST + ":" + FLASK_HOST_PORT + "/generate"

if "messages" not in st.session_state:
    st.session_state.messages = []

def display_message(message_content):
    if msg_item := message_content.get('text'):
        st.write(msg_item)
    if msg_item := message_content.get('image_path'):
        st.image(msg_item)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        display_message(message.get('content'))

col1, col2 = st.columns([1, 3])

with col1:
    output_type = st.selectbox(
        "Respond with",
        ("Text", "Image")
    )

with col2:
    

if prompt := st.chat_input("What is up?"):
    user_msg = {"role": "user", "content": {"text": prompt, "image_path": None}}
    st.session_state.messages.append(user_msg)
    # print("DEBUG: type(prompt): " + str(type(prompt)))
    request_urlencoded = {'question': user_msg.get('content').get('text')}
    with st.chat_message("user"):
        display_message(user_msg.get('content'))

    # with st.spinner("Generating results..."):
    response = requests.post(gen_url, data=request_urlencoded)
    response_obj = response.json()
    assistant_msg = {"role": "assistant", "content": {"text": response_obj.get('text', None), "image_path": response_obj.get('image_path', None)}}
    st.session_state.messages.append(assistant_msg)
    with st.chat_message("assistant"):
        display_message(assistant_msg.get('content'))

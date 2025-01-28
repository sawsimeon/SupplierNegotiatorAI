import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI





# Load environment variables from .env file
load_dotenv()

try:
    api_key = os.getenv("API_KEY")
except:
    api_key = os.getenv("API_KEY")


client = OpenAI(api_key=api_key)


st.title("Supplier Negotiation Chatbot")

# Initialize the session state for conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize the session state for input filed
if 'input' not in st.session_state:
    st.session_state.input = ""

def get_openai_response(prompt):
    response = client.completions.create(model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    max_tokens=500,
    n=1,
    stop=None,
    temperature=0.7)
    return response.choices[0].text.strip()

st.write("This chatbot is designed to help you negotiate with suppliers. Ask it for tips, strategies, or even practice negotiating with it.")

# User input
user_input = st.text_input("You: ", st.session_state.input, key="input_field")

if st.button("Send"):
    if user_input:
        prompt = f"You are a negotiation expert. Assist the user in negotiating with suppliers. User input: {user_input}"
        response = get_openai_response(prompt)

        # Append user input and bot response to the conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Clear the input field by setting its value to an empty string
        st.session_state.input = ""
        st.rerun()

# Display the conversation history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Supplier Negotiation Chatbot Valter AB LLM Supplier Negotiation:** {message['content']}")

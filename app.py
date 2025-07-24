import openai
import streamlit as st
from dotenv import load_dotenv
import os
import yaml
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("prompts/personalities.yaml","r") as f:
    personalities = yaml.safe_load(f)

st.set_page_config(page_title="PersonaBot",page_icon="🧠")
st.title("🧠 PersonaBot - Chat with Different Personalities")

persona = st.selectbox("Choose a Persona", list(personalities.keys()))
user_input = st.text_input("You:",key="input")

if persona == "custom":
    custom_prompt = st.text_area("Enter your custom personality prompt:")
else:
    custom_prompt = personalities[persona]['prompt']

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Send"):
    prompt = f"{custom_prompt}\nUser: {user_input}\nAI:"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # or gpt-4 if you have access
    messages=[
        {"role": "system", "content": custom_prompt},
        {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=150
    )
    reply = response['choices'][0]['message']['content'].strip()
st.session_state.chat_history.append((user_input,reply))

# Display chat history

for user_msg, bot_msg in st.session_state.chat_history[::-1]:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**{personalities[persona]['name']}**: {bot_msg}")


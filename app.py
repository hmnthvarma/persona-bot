import streamlit as st
import os
import yaml
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load personality prompts
with open("prompts/personalities.yaml", "r") as f:
    personalities = yaml.safe_load(f)

# Streamlit page settings
st.set_page_config(page_title="PersonaBot 🤖", page_icon="🧠")
st.title("🧠 PersonaBot - Switch Personalities While You Chat")

# UI - Persona selection
persona = st.selectbox("Choose a Persona", list(personalities.keys()))
user_input = st.text_input("You:", key="user_input")

# Get system prompt
if persona == "custom":
    custom_prompt = st.text_area("Enter your custom personality prompt:")
else:
    custom_prompt = personalities[persona]["prompt"]

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# On Send button click
if st.button("Send") and user_input.strip():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.chat_history.append((user_input, reply))
    except Exception as e:
        st.error(f"Error: {e}")

# Display chat history
st.markdown("---")
for user_msg, bot_msg in st.session_state.chat_history[::-1]:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**{personalities[persona]['name']}**: {bot_msg}")

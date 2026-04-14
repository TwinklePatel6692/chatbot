import streamlit as st
import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.messages import AIMessage, SystemMessage, HumanMessage
api_key = st.secrets["MISTRAL_API_KEY"]
# Load API keys from .env
load_dotenv()

# --- Page Setup ---
st.set_page_config(page_title="Intelligent Bot", page_icon="🧠")
st.title("🧠 Intelligent Chat")
st.markdown("---")

# --- Initialize Model ---
# Using cache_resource so the model doesn't reload every time you type
@st.cache_resource
def get_model():
    return ChatMistralAI(
        model="mistral-small-latest", # Recommended stable version
        temperature=0.9
    )

model = get_model()

# --- Initialize Session State (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are intelligent")
    ]

# --- Display Chat History ---
for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        continue  # Hide the system prompt from the UI
    
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# --- Chat Input & Logic ---
if prompt := st.chat_input("Type your message here..."):
    
    # 1. Add and show user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and show AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.invoke(st.session_state.messages)
                st.markdown(response.content)
                # 3. Save AI response to memory
                st.session_state.messages.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"Error: {e}")

# Option to clear chat
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = [SystemMessage(content="You are intelligent")]
    st.rerun()

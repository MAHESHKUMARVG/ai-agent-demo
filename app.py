import streamlit as st
import requests

st.set_page_config(page_title="🤖 AI Agent Demo", layout="centered")
st.title("🤖 Free AI Agent Demo")
st.write("Built with Streamlit + Hugging Face Inference API — runs 100% in the cloud!")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def generate_text(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]["generated_text"]

# Chat interface
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("💬 Ask me anything:", placeholder="e.g. Explain what AI is...")

if st.button("Generate"):
    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            result = generate_text(user_input)
        st.session_state.history.append((user_input, result))

# Display chat
for q, a in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 Agent:** {a}")

import streamlit as st
import requests

st.set_page_config(page_title="🤖 AI Agent Demo", layout="centered")
st.title("🤖 Free AI Agent Demo")
st.write("Built with Streamlit + Hugging Face Router API — 100% cloud hosted!")

# -----------------------------
# Hugging Face Router API Setup
# -----------------------------

API_URL = "https://router.huggingface.co/v1/completions"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}",
    "Content-Type": "application/json"
}

# -----------------------------
# Text Generation Function
# -----------------------------

def generate_text(prompt):
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 256
    }

    raw = requests.post(API_URL, headers=headers, json=payload)

    # If HuggingFace returns non-JSON (e.g., "Not Found")
    try:
        data = raw.json()
    except:
        return f"⚠️ HF API returned non-JSON response:\n\n{raw.text}"

    # If HF returns an error JSON
    if "error" in data:
        return f"⚠️ HF API Error: {data['error']}"

    # Expected OpenAI-like response format:
    # choices[0].text
    try:
        return data["choices"][0]["text"]
    except:
        return f"⚠️ Unexpected API response:\n\n{data}"

# -----------------------------
# Chat UI
# -----------------------------

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("💬 Ask me anything:", placeholder="e.g. Explain what AI is...")

if st.button("Generate"):
    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            result = generate_text(user_input)
        st.session_state.history.append((user_input, result))

# -----------------------------
# Chat History Display
# -----------------------------

for q, a in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 Agent:** {a}")

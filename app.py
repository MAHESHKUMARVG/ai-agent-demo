import streamlit as st
import requests

st.set_page_config(page_title="🤖 AI Agent Demo", layout="centered")
st.title("🤖 Free AI Agent Demo")
st.write("Built with Streamlit + Hugging Face Inference API — runs 100% in the cloud!")

API_URL = "https://router.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Wait-For-Model": "true"
}

def generate_text(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}

    # Get raw response first to debug decode errors
    raw = requests.post(API_URL, headers=headers, json=payload)

    # If response cannot be parsed as JSON:
    try:
        response = raw.json()
    except:
        return f"⚠️ HF API returned non-JSON response:\n\n{raw.text}"

    # HF error handling
    if "error" in response:
        return f"⚠️ HF API Error: {response['error']}"

    # Router-style dict response
    if isinstance(response, dict) and "generated_text" in response:
        return response["generated_text"]

    # Old list response
    if isinstance(response, list) and "generated_text" in response[0]:
        return response[0]["generated_text"]

    return f"⚠️ Unexpected API response:\n{response}"

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

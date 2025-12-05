import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="🤖 AI Agent Demo", layout="centered")
st.title("🤖 Free AI Agent Demo")
st.write("Built with Streamlit + Hugging Face — 100% free to run!")

# Load model (cached so it doesn’t reload every time)
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        device_map="auto"
    )

agent = load_model()

# Chat interface
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("💬 Ask me anything:", placeholder="e.g. Explain what AI is...")

if st.button("Generate"):
    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            result = agent(user_input, max_new_tokens=200, temperature=0.7)[0]["generated_text"]
        st.session_state.history.append((user_input, result))

# Display chat
for q, a in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 Agent:** {a}")

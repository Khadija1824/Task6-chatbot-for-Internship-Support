import streamlit as st
from utils.chatbot_engine import InternshipChatbot

# Page Configuration
st.set_page_config(
    page_title="Intern Support Assistant",
    page_icon="🤖",
    layout="centered"
)

# App Header
st.title("🤖 Intern Support Assistant")
st.markdown("Your virtual companion for company policies, workflows, and instant support.")
st.markdown("---")

# Initialize chatbot engine (cached)
@st.cache_resource
def load_bot():
    return InternshipChatbot()

with st.spinner("Loading knowledge base..."):
    bot = load_bot()

# Sidebar: Quick Guide & Controls
with st.sidebar:
    st.header("📌 Quick Guide")
    st.markdown("Ask questions about:")
    st.markdown("- Weekly progress reports")
    st.markdown("- IT & laptop troubleshooting")
    st.markdown("- Leave & absence policies")
    st.markdown("- Stipend processing")
    
    st.markdown("---")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I help you with your internship journey today?"}
        ]
        st.rerun()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you with your internship journey today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling
if user_input := st.chat_input("Type your question here..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text, source, confidence = bot.get_response(user_input)
            
            # Format display response
            if source != "None":
                full_reply = f"{response_text}\n\n*Source: {source} (Confidence: {confidence}%)*"
            else:
                full_reply = response_text
                
            st.markdown(full_reply)
            
    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_reply})
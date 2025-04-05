import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
import time
import uuid

# Load environment variables
load_dotenv()

# Configure LangSmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Enhanced Q&A Chatbot With Ollama"

# Page configuration
st.set_page_config(
    page_title="AI Assistant - Powered by Ollama",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
:root {
    --text-color: #FFFFFF;
    --background-color: #0E1117;
    --secondary-background: #262730;
    --accent-color: #4B56D2;
    --border-color: #555;
    --user-message-bg: #2E3856;
    --assistant-message-bg: #3A3F51;
    --model-info-bg: #3A3F51;
    --model-info-border: #4B56D2;
}
.main {
    background-color: var(--background-color);
    color: var(--text-color);
}
.stTextInput > div > div > input {
    padding: 12px 15px;
    border-radius: 15px;
    border: 1px solid var(--border-color);
    background-color: var(--secondary-background);
    color: var(--text-color);
}
.chat-message {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    color: var(--text-color);
}
.chat-message.user {
    background-color: var(--user-message-bg);
    border-left: 5px solid var(--accent-color);
}
.chat-message.assistant {
    background-color: var(--assistant-message-bg);
    border-left: 5px solid #718096;
}
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}
.chat-message .message {
    flex-grow: 1;
}
.stButton button {
    border-radius: 15px;
    padding: 5px 15px;
    font-weight: 500;
    background-color: var(--secondary-background);
    color: var(--text-color);
    border: 1px solid var(--border-color);
}
.stButton button:hover {
    border-color: var(--accent-color);
}
.sidebar .stButton button {
    width: 100%;
}
.model-info {
    padding: 12px;
    background-color: var(--model-info-bg);
    border-radius: 10px;
    margin-top: 15px;
    border: 1px solid var(--model-info-border);
    color: var(--text-color);
}
.model-name {
    color: var(--accent-color);
    font-weight: bold;
    margin-bottom: 5px;
}
footer {
    text-align: center;
    padding: 10px;
    font-size: 12px;
    color: #999;
    margin-top: 30px;
}
hr {
    border-color: var(--border-color);
    margin: 20px 0;
}
.stExpander {
    border: 1px solid var(--border-color);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Model details
MODEL_INFO = {
    "gemma2:2b": "Google's Gemma 2B - Lightweight model good for simple tasks",
    "mistral": "Mistral - Well-balanced language model with good reasoning capabilities",
    "llama2": "Meta's LLaMA 2 - General purpose language model",
    "phi3:mini": "Microsoft's Phi-3 Mini - Compact but powerful model",
    "llama3.2": "Meta's LLaMA 3.2 - Latest generation with enhanced capabilities"
}

# Session initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Prompt templates
PROMPT_TEMPLATES = {
    "Default": "You are a helpful assistant. Please respond to the user queries.\n\nQuestion: {question}",
    "Professional": "You are a professional consultant with expertise in various fields. Please provide detailed, well-structured, and accurate information.\n\nQuestion: {question}",
    "Creative": "You are a creative assistant with a flair for imaginative responses. Feel free to think outside the box while being helpful.\n\nQuestion: {question}",
    "Concise": "You are a concise assistant. Provide brief, clear answers without unnecessary details.\n\nQuestion: {question}"
}

# Response generation
def generate_response(question, model, temperature, max_tokens, prompt_style):
    with st.spinner("Thinking..."):
        try:
            prompt_template = PROMPT_TEMPLATES[prompt_style]
            prompt = ChatPromptTemplate.from_messages([
                ("system", prompt_template.split("\n\nQuestion:")[0]),
                ("user", f"Question: {question}")
            ])
            llm = Ollama(model=model, temperature=temperature, num_predict=max_tokens)
            chain = prompt | llm | StrOutputParser()
            start = time.time()
            response = chain.invoke({'question': question})
            end = time.time()
            return response, round(end - start, 2)
        except Exception as e:
            return f"Error: {str(e)}", 0

# Chat message display
def display_chat_message(message, is_user):
    avatar = "👤" if is_user else "🤖"
    role = "user" if is_user else "assistant"
    st.markdown(f"""
    <div class="chat-message {role}">
        <div class="avatar">{avatar}</div>
        <div class="message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

# Process user message and get response
def process_user_message(user_question, model, temperature, max_tokens, prompt_style):
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    response, duration = generate_response(user_question, model, temperature, max_tokens, prompt_style)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    return duration

# Main function
def main():
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        model = st.radio("Select Model:", list(MODEL_INFO.keys()), format_func=lambda x: x.capitalize())
        st.markdown(f"""
        <div class="model-info">
            <div class="model-name">{model.upper()}</div>
            <div>{MODEL_INFO[model]}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
            max_tokens = st.slider("Max Tokens", 50, 1000, 250, 50)
            prompt_style = st.selectbox("Prompt Style", list(PROMPT_TEMPLATES.keys()))

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_id = str(uuid.uuid4())
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("👨‍💻 **Powered by Ollama**")
        st.caption("Using LangChain for orchestration")

    # Main content
    st.title("🤖 AI Assistant")
    st.subheader("Your personal AI-powered chat assistant")

    # Show history
    for msg in st.session_state.messages:
        display_chat_message(msg["content"], msg["role"] == "user")

    # Chat input
    if user_input := st.chat_input("Ask me anything...", key="chat_input"):
        # Display user message
        display_chat_message(user_input, True)
        
        # Generate and display response
        duration = process_user_message(user_input, model, temperature, max_tokens, prompt_style)
        display_chat_message(st.session_state.messages[-1]["content"], False)
        st.caption(f"Response generated in {duration} seconds")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <footer>
        <p>Conversation ID: {st.session_state.conversation_id}</p>
        <p>Built with Streamlit and LangChain</p>
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
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

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stTextInput > div > div > input {
        padding: 12px 15px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
    }
    .chat-message {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #e6f3ff;
        border-left: 5px solid #2b6cb0;
    }
    .chat-message.assistant {
        background-color: #f0f0f0;
        border-left: 5px solid #718096;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 10px;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .stButton button {
        border-radius: 15px;
        padding: 5px 15px;
        font-weight: 500;
    }
    .sidebar .stButton button {
        width: 100%;
    }
    .model-info {
        padding: 10px;
        border-radius: 10px;
        margin-top: 15px;
        color: #ffffff; /* Text color for dark mode */
        background-color: #2b6cb0; /* Background color for dark mode */
        border: 1px solid #ffffff;
    }
    footer {
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Define the models and their descriptions
MODEL_INFO = {
    "gemma2:2b": "Google's Gemma 2B - Lightweight model good for simple tasks",
    "mistral": "Mistral - Well-balanced language model with good reasoning capabilities",
    "llama2": "Meta's LLaMA 2 - General purpose language model",
    "phi3:mini": "Microsoft's Phi-3 Mini - Compact but powerful model",
    "llama3.2": "Meta's LLaMA 3.2 - Latest generation with enhanced capabilities"
}

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Custom prompt templates
PROMPT_TEMPLATES = {
    "Default": "You are a helpful assistant. Please respond to the user queries.\n\nQuestion: {question}",
    "Professional": "You are a professional consultant with expertise in various fields. Please provide detailed, well-structured, and accurate information.\n\nQuestion: {question}",
    "Creative": "You are a creative assistant with a flair for imaginative responses. Feel free to think outside the box while being helpful.\n\nQuestion: {question}",
    "Concise": "You are a concise assistant. Provide brief, clear answers without unnecessary details.\n\nQuestion: {question}"
}

# Function to generate response
def generate_response(question, model, temperature, max_tokens, prompt_style):
    with st.spinner("Thinking..."):
        try:
            # Create the prompt template based on selected style
            prompt_template = PROMPT_TEMPLATES[prompt_style]
            prompt = ChatPromptTemplate.from_messages([
                ("system", prompt_template.split("\n\nQuestion:")[0]),
                ("user", f"Question: {question}")
            ])
            
            # Initialize the LLM
            llm = Ollama(model=model, temperature=temperature, num_predict=max_tokens)
            output_parser = StrOutputParser()
            
            # Create and invoke the chain
            chain = prompt | llm | output_parser
            
            # Track start time for response generation
            start_time = time.time()
            answer = chain.invoke({'question': question})
            end_time = time.time()
            
            # Return the answer and the time it took to generate
            return answer, round(end_time - start_time, 2)
        except Exception as e:
            return f"Error: {str(e)}", 0

def display_chat_message(message, is_user):
    avatar = "👤" if is_user else "🤖"
    role = "user" if is_user else "assistant"
    
    st.markdown(f"""
    <div class="chat-message {role}">
        <div class="avatar">{avatar}</div>
        <div class="message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

# Main application layout
def main():
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Model selection with radio buttons for better UX
        model = st.radio(
            "Select Model:",
            list(MODEL_INFO.keys()),
            format_func=lambda x: x.capitalize()
        )
        
        # Display model information
        st.markdown(f"""
        <div class="model-info">
            <strong>{model.upper()}</strong><br>
            {MODEL_INFO[model]}
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced settings in an expander
        with st.expander("Advanced Settings"):
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1,
                                  help="Higher values make output more random, lower values more deterministic")
            max_tokens = st.slider("Max Tokens", min_value=50, max_value=1000, value=250, step=50,
                                 help="Maximum number of tokens in the response")
            prompt_style = st.selectbox("Prompt Style", list(PROMPT_TEMPLATES.keys()), 
                                      help="Select the personality and style of the AI assistant")
        
        # Add a clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_id = str(uuid.uuid4())
            st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("👨‍💻 **Powered by Ollama**")
        st.caption("Using LangChain for orchestration")

    # Main content area
    st.title("🤖 AI Assistant")
    st.subheader("Your personal AI-powered chat assistant")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["content"], message["role"] == "user")
    
    # Chat input area
    user_input = st.text_input("Ask me anything:", key="user_input", placeholder="Type your question here...")
    
    # Handle user input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        display_chat_message(user_input, True)
        
        # Generate and display AI response
        response, response_time = generate_response(
            user_input, 
            model, 
            temperature, 
            max_tokens,
            prompt_style
        )
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display AI response
        display_chat_message(response, False)
        
        # Display response metrics
        st.caption(f"Response generated in {response_time} seconds")
        
        # Clear the input field
        st.experimental_rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <footer>
        <p>Conversation ID: {}</p>
        <p>Built with Streamlit and LangChain</p>
    </footer>
    """.format(st.session_state.conversation_id), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# Ollama AI Assistant Chatbot 🤖

A sleek, locally-running AI chatbot built with Streamlit, LangChain, and Ollama. This application provides an intuitive interface to interact with various open-source language models running on your local machine.

## ✨ Features

- **Local LLM Integration**: Run AI models locally through Ollama with no API costs
- **Multiple Model Options**:
  - gemma2:2b: Google's lightweight model for simple tasks
  - mistral: Well-balanced language model with good reasoning capabilities
  - llama2: Meta's general purpose language model
  - phi3:mini: Microsoft's compact but powerful model
  - llama3.2: Meta's latest generation with enhanced capabilities

- **Customizable Settings**:
  - Adjust temperature to control response randomness
  - Set max tokens for response length
  - Select from various prompt styles: Default, Professional, Creative, and Concise

- **Clean User Interface**:
  - Modern chat message styling
  - Responsive design
  - Helpful tooltips and informational displays

- **Additional Features**:
  - LangSmith integration for tracking and debugging
  - Conversation session management
  - Response timing metrics

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed on your system
- Downloaded models via Ollama for local use

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ollama-ai-assistant.git
cd ollama-ai-assistant
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root (optional for LangChain tracking):
```
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

4. Make sure Ollama is running on your system:
```bash
ollama serve
```

5. Pull the models you want to use:
```bash
ollama pull gemma2:2b
ollama pull mistral
ollama pull llama2
ollama pull phi3:mini
ollama pull llama3.2
```

### Running the Application

```bash
streamlit run app.py
```

Navigate to the URL provided by Streamlit (typically http://localhost:8501) to interact with the chatbot.

## 📋 Usage Guide

1. Select your preferred model from the sidebar
2. Adjust advanced settings as needed:
   - Higher temperature for more creative responses
   - Lower temperature for more deterministic outputs
   - Set token limit based on the length of response you prefer
   - Choose a prompt style that matches your interaction needs
3. Type your question in the input field and press Enter
4. View the AI's response in the chat window
5. Use the "Clear Chat" button to start a new conversation

## 🔧 Customization

### Adding New Models

To add new LLM models, first pull them with Ollama:

```bash
ollama pull your-new-model
```

Then update the `MODEL_INFO` dictionary in the script:

```python
MODEL_INFO = {
    "your-new-model": "Description of the new model",
    # ... existing models
}
```

### Creating Custom Prompt Templates

Add new prompt styles by updating the `PROMPT_TEMPLATES` dictionary:

```python
PROMPT_TEMPLATES = {
    "Technical": "You are a technical assistant specialized in explaining complex concepts clearly...",
    # ... existing templates
}
```

## ⚡ Performance Notes

- Performance depends on your hardware specifications
- Larger models require more RAM and may run slower on less powerful machines
- For best experience on lower-end hardware, use smaller models like gemma2:2b or phi3:mini

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- File upload support for document Q&A
- Voice input/output capabilities
- Chat history export feature
- Custom styling options
- Multi-modal model support
- GPU acceleration configuration

---

Built with ❤️ using Streamlit, LangChain and Ollama

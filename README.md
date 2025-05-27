
# 🌞 Summer of AI Chatbot

A comprehensive **RAG (Retrieval-Augmented Generation)** chatbot built for the **Swecha Summer of AI Internship** program. This intelligent assistant helps interns access program information, apply for leaves, and reach emergency contacts through a modern, user-friendly interface.

---

## 🌟 Features

- 💬 **Intelligent Q&A**: Chatbot powered by Google Gemini with RAG to answer internship-related queries
- 📝 **Leave Application**: Submit leave requests with optional document uploads
- 🚨 **Emergency Contacts**: Quick access to key contacts during the internship
- 🌍 **Multi-location Support**: Venue details across Telangana
- ❓ **FAQ Section**: Instantly answers common questions

---

## 🏗️ Architecture

- **Frontend**: Streamlit-based chat interface
- **Backend**: Python implementation of RAG using Google Gemini
- **Vector Search**: FAISS for fast, accurate retrieval
- **Embeddings**: Sentence Transformers for encoding
- **Knowledge Base**: Text-based program info (`info.txt`)

---

## 🚀 Quick Start

### 🔧 Prerequisites

Install required packages:

```bash
pip install streamlit streamlit-chat google-generativeai faiss-cpu sentence-transformers numpy pandas
```

### ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Vighneshwarkuru/Summer-Of-AI-chatbot.git
   cd Summer-Of-AI-chatbot
   ```

2. **Set your API Key**  
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace `"Your_API_Key"` in `main.py` with your actual key

3. **Knowledge Base**  
   - Ensure `info.txt` contains valid internship information

4. **Launch the Chatbot**  
   ```bash
   streamlit run interface.py
   ```

5. **Access the Interface**  
   Open `http://localhost:8501` in your browser

---

## 📁 Project Structure

```
Summer-Of-AI-chatbot/
├── README.md             # Project documentation
├── main.py               # Core RAG logic
├── interface.py          # Streamlit-based frontend
├── info.txt              # Knowledge base
├── rag_system.log        # Backend logs
└── .git/                 # Git tracking
```

---

## ⚙️ Configuration

### 🔍 RAG System Parameters

| Parameter        | Value                         |
|------------------|-------------------------------|
| Embedding Model  | `all-MiniLM-L6-v2`            |
| LLM              | `gemini-1.5-flash`            |
| Top-k Retrieval  | 3 relevant chunks             |
| Cache Size       | 100 queries                   |

### 💻 Streamlit Settings

- Wide layout for better readability
- Session-persistent chat history
- Form validation for leave requests
- Clear and helpful error messages

---

## 🛠️ Technical Details

### 🧠 RAG Workflow

- Use SentenceTransformer to embed internship data
- Index using FAISS for quick vector search
- Query Google Gemini LLM with retrieved context
- Cache results using LRU for speed

### ⚠️ Error Handling

- Detailed logging in `rag_system.log` and `interface.log`
- Graceful handling of API errors and missing info
- Persistent state management for user experience

---

## 💡 Usage Examples

### 🤖 Chat

- "What is the internship duration?"
- "Can I attend online only?"
- "Where is the Warangal venue?"
- "How do I apply for leave?"

### 📝 Leave Application

- Input intern ID and leave type
- Pick date range and reason
- Optional upload of medical or personal document
- One-click validated submission

---

## 📝 Logging

| File              | Purpose                          |
|------------------|----------------------------------|
| `rag_system.log`  | Logs all backend RAG operations |
| `interface.log`   | Logs user interactions/forms     |

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push and open a Pull Request

---

## 📄 License

This chatbot is a part of the Swecha Summer of AI program. Please follow program guidelines for appropriate usage.

---

## 🆘 Support

- Use the **FAQ** section in the chatbot
- Reach out to your program coordinator
- Refer to the `info.txt` knowledge base

---

> **Built with ❤️ for the Summer of AI Internship**  
> Empowering students to build impactful AI solutions for the Telugu language and beyond.

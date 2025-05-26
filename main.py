# main.py
import google.generativeai as genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from functools import lru_cache
import logging

class RAGSystem:
    def _init_(self, knowledge_file="info.txt"):
        logging.basicConfig(
            filename='rag_system.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Initializing RAG system...")

        try:
            genai.configure(api_key="Your_API_Key")  # 🔐 Replace with your actual Gemini API key
            self.llm = genai.GenerativeModel("models/gemini-1.5-flash")
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            self.chunks = self._load_knowledge(knowledge_file)
            self.index = self._create_index()
            logging.info("RAG system initialized successfully.")
        except Exception as e:
            logging.error(f"Initialization failed: {str(e)}")
            raise

    def _load_knowledge(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
        logging.info(f"Loaded {len(chunks)} knowledge chunks")
        return chunks

    def _create_index(self):
        embeddings = self.embedder.encode(self.chunks, convert_to_numpy=True)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        logging.info("FAISS index created.")
        return index

    @lru_cache(maxsize=100)
    def query(self, question, k=3):
        try:
            logging.info(f"Processing query: {question}")
            query_embedding = self.embedder.encode([question])[0]
            _, indices = self.index.search(np.array([query_embedding]), k)
            retrieved_chunks = [self.chunks[i] for i in indices[0]]
            context = "\n\n".join(retrieved_chunks)
            prompt = self._build_prompt(question, context)
            response = self.llm.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Query failed: {str(e)}")
            return "Sorry, I encountered an error while processing your query."

    def _build_prompt(self, question, context):
        return f"""You are a helpful assistant for open-source contribution interns. 
Based on the following context, answer the question concisely and helpfully.
If the information isn't in the context, say you don't know and suggest contacting the program administrator.

Context:
{context}

Question: {question}

Answer:"""

# Global instance for import
rag_system = RAGSystem()

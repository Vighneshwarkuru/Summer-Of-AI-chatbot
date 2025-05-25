import google.generativeai as genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


genai.configure(api_key="AIzaSyDjluzJLeucnG6qrOoWv2I3OfiE5RAGq4I")

model = genai.GenerativeModel("models/gemini-1.5-flash")


with open("yourfile.txt", "r", encoding="utf-8") as f:
    text = f.read()


chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]

embedder = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embedder.encode(chunks, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)


query = input("Enter your question: ")
query_embedding = embedder.encode([query])[0]

k = 3  
_, indices = index.search(np.array([query_embedding]), k)

retrieved_chunks = [chunks[i] for i in indices[0]]

context = "\n\n".join(retrieved_chunks)
prompt = f"You are a 24/7 help assistant chatbot, Based on the following context, answer the question polietly:\n\n{context}\n\nQuestion: {query}"

response = model.generate_content(prompt)
print(response.text)
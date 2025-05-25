import google.generativeai as genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
genai.configure(api_key="AIzaSyDjluzJLeucnG6qrOoWv2I3OfiE5RAGq4I")

model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- STEP 1: Load and split text file ---
with open("yourfile.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Simple chunking by paragraph (customize as needed)
chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]

# --- STEP 2: Embed the chunks ---
# Gemini API does not expose embeddings yet (as of early 2024).
# Use an external model like sentence-transformers or OpenAI for embeddings:
embedder = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embedder.encode(chunks, convert_to_numpy=True)

# --- STEP 3: Create FAISS index ---
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# --- STEP 4: Handle a query ---
query = input("Enter your question: ")
query_embedding = embedder.encode([query])[0]

k = 3  # number of top results
_, indices = index.search(np.array([query_embedding]), k)

retrieved_chunks = [chunks[i] for i in indices[0]]

# --- STEP 5: Pass to Gemini ---
context = "\n\n".join(retrieved_chunks)
prompt = f"Based on the following context, answer the question:\n\n{context}\n\nQuestion: {query}"

response = model.generate_content(prompt)
print(response.text)
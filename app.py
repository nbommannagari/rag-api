import os
from fastapi import FastAPI
import chromadb

# Mock LLM mode for CI testing
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

if not USE_MOCK_LLM:
    import ollama


app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")
# ollama_client = ollama.Client(host="http://host.docker.internal:11434")


@app.post("/query")
def query(q: str): # Question arrives to your API
    # Chroma searches through your knowledge base to find text that matches the question's meaning
    # n_results=1 means it will return the most relevant document
    results = collection.query(query_texts=[q], n_results=1) 

    # If there is a document that matches the question, it will be stored in the context variable. If not, it will be an empty string.
    context = results["documents"][0][0] if results["documents"] else ""

    if USE_MOCK_LLM:
        # In mock mode, return the retrieved context directly
        return {"answer": context}

    # In production mode, use Ollama
    # The question and the matching text are sent together to tinyllama, which creates an answer
    ollama_client = ollama.Client(host="http://host.docker.internal:11434")

    answer = ollama.generate(
    # answer = ollama_client.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
    )
    # The answer is returned to the user
    return {"answer": answer["response"]}

@app.post("/add")
def add_knowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    # Accepts a text parameter (the content to add)
    try:
        # Generate a unique ID for the new document using uuid
        import uuid
        doc_id = str(uuid.uuid4())
        
        # Add the text to Chroma collection with the doc_id (UUID)
        collection.add(documents=[text], ids=[doc_id])
        
        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

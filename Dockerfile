# Tells Docker to start with a pre-built image that has Python 3.11 installed. This is the foundation everything else builds on.
FROM python:3.11-slim
# Sets the working directory inside the container to /app
WORKDIR /app
# Installs curl and removes the package list to keep the image clean.
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Copies your application files from your computer into the container. These files become part of the image.
COPY app.py embed_docs.py ./
COPY docs ./docs
# Execute commands during build time. RUN installs packages and pre-computes embeddings, so they're baked into the image.
RUN pip install fastapi uvicorn chromadb ollama
# Pre-computes embeddings for your knowledge base and saves them in Chroma.
RUN python embed_docs.py 
# Opens port 8000 to allow external traffic to reach your application.  This is the port your server will listen on.
EXPOSE 8000 
# Tells Docker what command to run when the container starts. This starts the FastAPI server and makes it accessible at http://localhost:8000.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

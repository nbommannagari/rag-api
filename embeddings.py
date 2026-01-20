import chromadb

# - Creates a Chroma client that stores data permanently in a new ./db folder on your computer. 
# The PersistentClient means the data will be saved to disk, so it persists even after you close the program.
client = chromadb.PersistentClient(path="./db")

# Gets an existing collection named "docs" or creates a new one if it doesn't exist. A collection is like a folder that holds your documents and their embeddings.
# You can have multiple collections for different types of documents.
collection = client.get_or_create_collection("docs")

# Opens the k8s.txt file in read mode. The with statement automatically closes the file when done, which is a best practice in Python.
with open("k8s.txt", "r") as f:
    text = f.read() # Reads all the content from the file and stores it in the text variable.

# Adds the text to the collection with the ID "k8s".
# Chroma automatically converts the text into embeddings (numerical representations) when you add it. 
# The ids parameter gives each document a unique identifier so you can reference it later.
collection.add(documents=[text], ids=["k8s"]) 

print("Embedding stored in Chroma")


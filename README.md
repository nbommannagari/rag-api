
### Run container
docker run -p 8000:8000 rag-app

* docker run - Creates and starts a new container from an image
* -p 8000:8000 - Maps port 8000 on your host (your computer) to port 8000 in the container. This is called port mapping - it makes the container's port 8000 accessible from your computer.
* rag-app - The name of the image to run (the one we built earlier)


#### Issues faced:

``` 'File "/usr/local/lib/python3.11/site-packages/ollama/_client.py", line 135, in _request_raw
    raise ConnectionError(CONNECTION_ERROR_MESSAGE) from None
ConnectionError: Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download'```


Fix: Add below in app.py

```ollama_client = ollama.Client(host="http://host.docker.internal:11434")```

##### Also add the below ollama_client.generate instead of ollama. Now that we've created a client with the correct host address, we need to use that client to make API calls. The client knows where to find Ollama on your computer!

answer = ollama_client.generate(
    model="tinyllama",
    prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
)

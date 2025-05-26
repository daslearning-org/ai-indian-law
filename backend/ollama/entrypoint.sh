#!/bin/bash

# Start Ollama server in the background
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama server to be active..."

# Wait for Ollama to be ready (you can customize the health check)
# This loop waits until `ollama list` returns something, indicating the server is up
while ! ollama list > /dev/null 2>&1; do
    sleep 1
done

echo "Ollama server is active. Pulling models..."

# Pull your desired LLMs
ollama pull llama3.2
ollama pull mxbai-embed-large

echo "Models pulled. Keeping Ollama server running..."

# Wait for the background Ollama server process to finish (it won't, as it's a long-running service)
wait $OLLAMA_PID
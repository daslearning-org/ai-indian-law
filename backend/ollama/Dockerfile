# Use the official Ollama base image
FROM ollama/ollama:latest

# Set environment variables (optional, but good for reproducibility)
# OLLAMA_MODELS=/root/.ollama/models is the default location, but can be overridden
ENV OLLAMA_MODELS=/root/.ollama/models

# Create a directory to store models (if not using the default volume mount)
# RUN mkdir -p ${OLLAMA_MODELS}

# Copy an entrypoint script to handle Ollama startup and model pulling
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose Ollama's default port
EXPOSE 11434

# Use the entrypoint script as the container's entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command to run Ollama server
CMD ["ollama", "serve"]
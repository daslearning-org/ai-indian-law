# Update Ollama Configs
Advance level tasks

## Make Ollama listens from any host in the network
```bash
sudo systemctl edit ollama.service
# add below lines
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"

# restart services
sudo systemctl daemon-reload
sudo systemctl restart ollama

# start serving
export OLLAMA_HOST="0.0.0.0:11434"
ollama serve & # Or whatever command you use to start Ollama
```

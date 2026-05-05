#!/bin/bash
PROJECT_DIR="/Users/leefanghui/Desktop/ContentedBot"
cd "$PROJECT_DIR"

if ! curl -sf http://localhost:11434 > /dev/null 2>&1; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
fi

open http://localhost:8501
streamlit run app.py --server.port 8501 --server.headless true

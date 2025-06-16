# Week 4: Flask, RAG and MCP Learning

This week covers Flask web development, RAG and Message Control Protocol (MCP) implementation. Contains three main parts:

## 1. Flask Tutorial App (`flask/`)

Simple trivia app built during the Flask tutorial.

```bash
cd flask
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py
```

## 2. MCP and RAG Implementation (`scripts/`)

### MCP Server
```bash
cd scripts
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python mcp_server_example.py
```

### MCP Client
```bash
# In a new terminal, with the same venv
python mcp_client_example.py
```

### RAG Example
```bash
# In the same venv
python rag.py
```

## 3. HmmSpeak Flask App (`hmmspeak-flask/`)

Final task: Converting the HmmSpeak app to a Flask web application.

```bash
cd hmmspeak-flask
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python run.py
```

## Project Structure

```
week4/
├── flask/              # Flask tutorial app
├── scripts/           # MCP and RAG examples
│   ├── mcp_server.py
│   ├── mcp_client.py
│   └── rag_example.py
├── hmmspeak-flask/    # Final Flask app
└── requirements.txt   # Common requirements
```

## Note

Each component has its own virtual environment and requirements. Make sure to activate the correct environment for each part.
# CineBot

CineBot is a conversational AI assistant that provides context-aware movie recommendations. It uses Retrieval-Augmented Generation (RAG) to fetch movie data from the TMDB API, indexes it locally via ChromaDB, and generates responses using a Hugging Face LLM. It features a Query Condenser to maintain conversational memory without degrading vector search accuracy.

## Features
* Automated Setup Wizard: Configures API keys and builds the local database on first launch via a Streamlit UI.
* Context-Aware Memory: Uses `InMemoryChatMessageHistory` and LLM-based query rewriting to handle follow-up questions accurately.
* Local Vector Database: Semantic search powered by ChromaDB.
* Package Architecture: Structured using the `src/` layout for maintainable imports.

## Prerequisites
* Python 3.12+
* Hugging Face API Token
* TMDB Read Access Token

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/Karthik-005/CineBot.git](https://github.com/Karthik-005/CineBot.git)
cd CineBot
```

2. Create and activate a virtual environment:
uv venv
source .venv/bin/activate

3. Install dependencies in editable mode:
uv pip install -e .

4. Run the application:
streamlit run main.py

## Explanation of initialization process

1. When the main.py file is run for the first time, it checks for the existance of required API keys and data. If these requirements are not met then the UI prompts the user to enter TMDB read access token and hugging face API key. Once these details are entered, they are entered into a .env file in the project root.

2. After the user enters the required info the data will be fetced through TMDB API and preprocessed. Each row in the preprocessed data will be converted into a document object and inserted into a vector database (ChromaDB). With this the required setup is complete.

3. Once the setup is complete the UI will change into a chat interface where the user can ask movie related queries.


## Project Structure
 .
├── config.yaml
├── main.py
├── notebooks
│   └── MovieMate.ipynb
├── project_brief.pdf
├── pyproject.toml
├── README.md
├── src
│   ├── cinebot
│       ├── complete_setup.py
│       ├── config.py
│       ├── database.py
│       ├── engine.py
│       ├── ingestion.py
│       ├── __init__.py
│       ├── prompts.py
│           
└── uv.lock

## Project Structure Explanation



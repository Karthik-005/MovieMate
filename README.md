# MovieMate

MovieMate is a conversational AI assistant that provides context-aware movie recommendations. It uses Retrieval-Augmented Generation (RAG) to fetch movie data from the TMDB API, indexes it locally via ChromaDB, and generates responses using a Hugging Face LLM. It features a Query Condenser to maintain conversational memory without degrading vector search accuracy.

## Prerequisites

* Python 3.12+
* Hugging Face API Token
* TMDB Read Access Token

Note: 
The following permissions must enabled for hugging face token:

* Read access to contents of all repos under your personal namespace
* Read access to contents of all public gated repos you can access
* Make calls to Inference Providers
 
## Installation

1. Clone the repository:
```bash
git clone [https://github.com/Karthik-005/MovieMate](https://github.com/Karthik-005/MovieMate)
cd MovieMate
```

2. Create and activate a virtual environment:

Option A: Using standard pip
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```
Option B: Using uv
```bash
uv sync
```
3. Install dependencies in editable mode:
```bash
pip install -e .
```
4. Run the application:
```bash
streamlit run main.py
```

## Explanation of initialization process

1. When the main.py file is run for the first time, it checks for the existance of required API keys and data. If these requirements are not met then the UI prompts the user to enter TMDB read access token and hugging face API key. Once these details are entered, they are entered into a .env file in the project root.

2. After the user enters the required info the data will be fetced through TMDB API and preprocessed. Each row in the preprocessed data will be converted into a document object and inserted into a vector database (ChromaDB). With this the required setup is complete.

3. Once the setup is complete the UI will change into a chat interface where the user can ask movie related queries.

## Data Preprocessing

The following preprocessing steps are applied on the collected data:

1. Removal of duplicate rows 

2. Combining all the text columns into one single column ("combined_text"). This column contains textual info like Plot of the movie, names of the directors, genres in the movie, names of actors/actresses involved in the movie. This column is going to be used for semantic search in the vector database.

3. Normalization of case in all the textual columns.
 
## Project Structure

```bash
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
```

## Project Structure Explanation



## Limitations

1. The model performs a vector DB search for every query (even the queries that only require chat history) this takes unnecessary amount of time.

2. The chatbot is good at answering semantic queries (ex: "Suggest some action movies...") but it cannot handle queries with very specific details (ex: "suggest movies released in 2021 and have a duration above 100 min"). This is probably because the plot of each movie in the provided context takes most of the space, as a result the other specific details like duration, year of release are diluted in the embedding vectors.  
	
3. 

# MovieMate

MovieMate is a conversational AI assistant that provides context-aware movie recommendations. It uses Retrieval-Augmented Generation (RAG) to fetch movie data from the TMDB API, indexes it locally via ChromaDB, and generates responses using a Hugging Face LLM. It has a Query Condenser to maintain conversational memory without degrading vector search accuracy.

## Prerequisites

* Python 3.12+
* Hugging Face API Token
* TMDB Read Access Token

Note: 
1. The following permissions must enabled for hugging face token:

* Read access to contents of all repos under your personal namespace
* Read access to contents of all public gated repos you can access
* Make calls to Inference Providers

2. If you encounter a connection error during the initial setup or data fetching process, it is likely because your network is unable to reach the TMDB servers (TMDB is blocked by some ISPs in certain regions). If this happens, you may need to use a VPN to successfully download the initial dataset.

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/Karthik-005/MovieMate.git](https://github.com/Karthik-005/MovieMate.git)
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

1. Removal of duplicate rows.

2. Combining all the text columns into one single column ("combined_text"). This column contains textual info like Plot of the movie, names of the directors, genres in the movie, names of actors/actresses involved in the movie. This column is going to be used for semantic search in the vector database.

3. Normalization of case in all the textual columns.
 
## Project Structure

```bash
 .
├── config.yaml
├── main.py
├── notebooks
│   └── MovieMate.ipynb
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

1. config.yaml: Contains all the configurations (like paths of different files, names/repo ids of the models used etc..)

2. main.py: This is the entry point of this project, it contains the streamlit UI and handles the initial setup logic.

3. notebooks/MovieMate.ipynb: This file is used for data exploration and EDA.

4. pyproject.toml / uv.lock: Project metadata and dependency management files utilized by pip or uv to ensure reproducible 		environments.

5. cinebot: This is the package that contains all the backend code. (This module needs to be installed in editable mode as mentioned in the instructions)

6. complete_setup: This is the data pipeline of the project, it calls the functions to fetch data, preprocess the data, create documents and build the vector database.

7. config.py: Fetches all the configurations from config.yaml file and creates a settings object that can be used by all the backend code.

8. ingestion.py: Fetches the movie data, preprocesses it and creates objects to be inserted into the vector database. 

9. database.py: Creates vector database from the documents created in ingestion.py. 

10. prompts.py: Defines System prompt, Human prompt template and condenser prompt. This file finally creates two templates, one for the final prompt sent to the LLM and other for the formatting each document fetched (through similarity search) to be provided as context to the LLM. 

11. engine.py: This file takes care of augmenting the query with relevant data and sending the final prompt to the LLM.

## Limitations

1. The model performs a vector DB search for every query (even the queries that only require chat history) this takes unnecessary amount of time.

2. The chatbot is good at answering semantic queries (ex: "Suggest some action movies...") but it cannot handle queries with very specific details (ex: "suggest movies released in 2021 and have a duration above 100 min"). This is probably because the plot of each movie in the provided context takes most of the space, as a result the other specific details like duration, year of release are diluted in the embedding vectors.  

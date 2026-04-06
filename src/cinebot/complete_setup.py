from cinebot import ingestion, database
from cinebot.config import settings
from dotenv import load_dotenv, set_key, dotenv_values
import os

def complete_setup():
	# API keys and tokens
	env_path = settings.ROOT_DIR / '.env'
	
	if not load_dotenv():
		print("Creating .env file....")
		env_path.touch()
	
	config = dotenv_values(env_path)
	if "HF_TOKEN" not in config:
		hf_token = input("Enter your Hugging face token: ").strip()
		set_key(env_path, "HF_TOKEN", hf_token)
		
	if "TMDB_READ_ACCESS" not in config:
		tmdb_read_access = input("Enter your TMDB read access key: ")
		set_key(env_path, "TMDB_READ_ACCESS", tmdb_read_access).strip()
	
	# data pipeline
	base_url = settings.BASE_URL
	raw_data_path = settings.RAW_DATA_PATH
	preprocessed_data_path = settings.PREPROCESSED_DATA_PATH
	
	df = ingestion.fetch_movie_data(base_url, raw_data_path)	
	df = ingestion.preprocess_data(df, preprocessed_data_path)
	docs = ingestion.create_docs(df)
	vector_db = database.initiate_vector_db(docs)
	
	
		
				
		


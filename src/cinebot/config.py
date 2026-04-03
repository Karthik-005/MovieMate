from pathlib import Path
from dotenv import load_dotenv
import yaml
import os


class Settings():
	def __init__(self):
	
		# Locate the root dir.
		self.ROOT_DIR = Path(__file__).parents[2].resolve()
		
		# Load the environmental variables.
		if not load_dotenv(self.ROOT_DIR / '.env'):
			raise FileNotFoundError('Couldn\'t find the .env file')
		
		# API Keys		
		self.TMDB_API_KEY = os.getenv('TMDB_API_KEY')
		self.TMDB_READ_ACCESS = os.getenv('TMDB_READ_ACCESS')
		self.HF_TOKEN = os.getenv('HF_TOKEN')
		
		if not (self.TMDB_API_KEY and self.TMDB_READ_ACCESS and self.HF_TOKEN):
			raise ValueError("Couldn't load all the environmental variables")
		
		# Load config.yaml file
		with open(self.ROOT_DIR / "config.yaml", "r") as f:
			config = yaml.safe_load(f)
		
		# Data
		self.RAW_DATA_PATH = self.ROOT_DIR / config['data']['raw_data_path']
		self.PREPROCESSED_DATA_PATH = self.ROOT_DIR / config['data']['preprocessed_data_path']
		self.VECTOR_DB = {'path': self.ROOT_DIR / config['data']['vector_db']['path'],
						  'collection_name': config['data']['vector_db']['collection_name']}
		
		# TMDB API
		self.BASE_URL = config['api']['base_url']
		self.DISCOVER_ENDPOINT = config['api']['discover_endpoint']
		self.CREDITS_ENDPOINT = config['api']['credits_endpoint']
		self.MOVIE_DETAILS_ENDPOINT = config['api']['movie_details_endpoint']
		self.MOVIE_QUERY_PARAMS = {'vote_count_gte': config['api']['movie_query_parameters']['vote_count_gte'], 
								   'sort_by': config['api']['movie_query_parameters']['sort_by']}

		# Hugging face
		self.EMBEDDING_MODEL = config['hugging_face']['embedding_model']
		self.LLM = config['hugging_face']['llm']
		
		# LLM
		self.LLM_CONFIG = {
			'repo_id':self.LLM,
			'task':"text-generation",
			'temperature':0.8,
			'top_p':0.9,
			'max_new_tokens':512,
			'huggingfacehub_api_token':self.HF_TOKEN,
			'provider':'auto'
		}
		
settings = Settings()

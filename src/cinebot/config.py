from pathlib import Path
from dotenv import load_dotenv
import yaml
import os

load_dotenv()
class Settings():
	def __init__(self):
		HF_TOKEN = os.getenv('HF_TOKEN')
		# Locate the root dir.
		self.ROOT_DIR = Path(__file__).parents[2].resolve()
		
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
			'huggingfacehub_api_token':HF_TOKEN,
			'provider':'auto'
		}
		
settings = Settings()

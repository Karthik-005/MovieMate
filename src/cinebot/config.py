from pathlib import Path
from dotenv import load_dotenv
import yaml
import os

class Settings():
	def __init__(self):
	
		# Locate the root dir.
		self.ROOT_DIR = Path(__file__).parents[2]
	
		# Load the environmental variables.
		try:
			load_dotenv()
			self.TMDB_API_KEY = os.getenv('TMDB_API_KEY')
			self.TMDB_READ_ACCESS = os.getenv('TMDB_READ_ACCESS')
			self.HF_TOKEN = os.getenv('HF_TOKEN')
			
		except Exception as e:
			print("Couldn't load all the environmental variables")
			print(f"Error : {e}")
		
		
		
		# Load config.yaml file
		with open(ROOT_DIR / "config.yaml", "r") as f:
			config = yaml.safe_load(f)
		
		# Data
		self.RAW_DATA_PATH = self.ROOT_DIR / config['data']['raw_date_path']
		self.PREPROCESSED_DATA_PATH = self.ROOT_DIR / config['data']['preprocessed_data_path']
		self.VECTOR_DB = {'path': self.ROOT_DIR / config['data']['vector_db']['path'],
						  'collection_name': config['data']['vector_db']['collection_name']}
		
		# API
		self.BASE_URL = config['api']['base_url']
		self.DISCOVER_ENDPOINT = config['api']['discover_endpoint']
		self.CREDITS_ENDPOINT = config['api']['credits_endpoint']
		self.MOVIE_DETAILS_ENDPOINT = config['api']['movie_details_endpoint']
		self.MOVIE_QUERY_PARAMS = {'vote_count_gte': config['api']['movie_query_parameters']['vote_count_gte'], 
								   'sort_by': config['api']['movie_query_parameters']['sort_by']}

		# Hugging face
		self.EMBEDDING_MODEL = config['hugging_face']['embedding_model']

settings = Settings()

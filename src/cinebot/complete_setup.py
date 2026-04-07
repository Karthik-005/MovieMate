from cinebot import ingestion, database
from cinebot.config import settings 
def complete_setup(read_access, hf_token):
	# data pipeline
	base_url = settings.BASE_URL
	raw_data_path = settings.RAW_DATA_PATH
	preprocessed_data_path = settings.PREPROCESSED_DATA_PATH
	
	df = ingestion.fetch_movie_data(base_url, raw_data_path, read_access)	
	df = ingestion.preprocess_data(df, preprocessed_data_path)
	docs = ingestion.create_docs(df)
	vector_db = database.initiate_vector_db(docs)
	
	
		
				
		


import os
from langchain_chroma import Chroma
from pathlib import Path
from tqdm.auto import tqdm
from cinebot.config import settings
from cinebot.ingestion import create_docs, fetch_movie_data, preprocess_data
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import time

def initiate_vector_db(docs):
	
	# Load the embedding model
	model_name = settings.EMBEDDING_MODEL
	embedding_model = HuggingFaceEndpointEmbeddings(model=model_name,
	                                        huggingfacehub_api_token=settings.HF_TOKEN)
    
    
	vector_db_path = settings.VECTOR_DB['path']
    
    # If the vector database is already created just connect to it. 
	if os.path.exists(vector_db_path):
		print("Connect to the existing vectorDB...")
		vector_db = Chroma(
            embedding_function=embedding_model,
            persist_directory=str(vector_db_path),
            collection_name=settings.VECTOR_DB['collection_name']
        )    
		
		# Check if the vectorDB folder doesn't contain any data.
		if vector_db._collection.count() == 0:
			print("The database is empty, adding the documents to the database..")
			
			for i in tqdm(range(0, len(docs), 10), desc="Adding docs one batch at a time"):
				vector_db.add_documents(docs[i:i+10])
			
    # Create a new vector database and ingest all the docs into it.
	else:    
		print("Creating a new vectorDB....")
		vector_db = Chroma(
            embedding_function=embedding_model,
            persist_directory=str(vector_db_path),
            collection_name=settings.VECTOR_DB['collection_name']
        )
        
		for i in tqdm(range(0, len(docs), 10), desc="Adding docs one batch at a time"):
			batch = docs[i:i+10]
			
			# Make mulitple attempts if the first attempt at the API call fails.
			for attempt in range(3):
				try:
					vector_db.add_documents(batch)
					break
					
				except Exception as e:
					if attempt < 2:
						print(f"Failed to upload the batch {(i+11)//10}, retrying in 5 secs")        			
						time.sleep(5)
        				
					else:
						raise RuntimeError(f"Batch failed permanently : {e}")
        				
	return vector_db

if __name__ == "__main__":
	raw_data_path = settings.RAW_DATA_PATH
	pre_data_path = settings.PREPROCESSED_DATA_PATH
	base_url = settings.BASE_URL
	
	df = fetch_movie_data(base_url, raw_data_path)
	df = preprocess_data(df, pre_data_path)
	docs = create_docs(df)
	
	initiate_vector_db(docs)

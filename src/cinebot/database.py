import os
from langchain_chroma import Chroma

def initiate_vector_db(embedding_model, vector_db_path, docs):

    # If the vector database is already created just connect to it. 
    if os.path.exists(vector_db_path):
        print("Connect to the existing vectorDB...")
        vector_db = Chroma(
            embedding_function=embedding_model,
            persist_directory=vector_db_path,
            collection_name='movies'
        )    
		
		# Check if the vectorDB folder contains data
		if vector_db._collection.count() == 0:
			print("The database is empty, adding the documents to the database..")
			vector_db = Chroma.from_documents(
				embedding= embedding_model, 
				documents=docs,
				collection_name='movies',
				persist_directory=vector_db_path
			)
			
    # Create a new vector database and ingest all the docs into it.
    else:    
        print("Creating a new vectorDB....")
        vector_db = Chroma.from_documents(
            documents=docs,
            embedding=embedding_model,
            persist_directory=vector_db_path,
            collection_name='movies'
        )
        
    return vector_db

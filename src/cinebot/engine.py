from langchain_core.prompts import format_document
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_chroma import Chroma
from cinebot.config import settings
from cinebot.prompts import CHAT_TEMPLATE, DOC_TEMPLATE 
from langchain_huggingface import HuggingFaceEndpointEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
class Chatbot():
	def __init__(self, top_k):
		self.top_k = top_k
		load_dotenv()
		
		# Connect to the vector DB.
		hf_token = os.getenv('HF_TOKEN')
		vector_db_path = settings.VECTOR_DB['path']
		embedding_model_name = settings.EMBEDDING_MODEL
		embedding_model = HuggingFaceEndpointEmbeddings(model=embedding_model_name,
													huggingfacehub_api_token=hf_token)
		collection_name = settings.VECTOR_DB['collection_name']
				
		self.vector_db = Chroma(embedding_function=embedding_model,
						   	   persist_directory=vector_db_path,
						   	   collection_name=collection_name)
		
		# Connect to the LLM.
		llm_repo_id = settings.LLM
		llm_config = settings.LLM_CONFIG
		llm = HuggingFaceEndpoint(**llm_config)
	
		# Initiate chat and chat history.
		self.history = InMemoryChatMessageHistory()
		self.chat = ChatHuggingFace(llm=llm, verbose=True)
		
	def retrieve(self, query):

		# Similarity search to get tok_k similar movies.
		docs = self.vector_db.similarity_search(query=query,
											  k=self.top_k)
											  
		return docs
		
	def create_prompt(self, docs, query):
		
		# Format the retrieved documents to create the final prompt for the LLM.
		formatted_docs = [format_document(doc, DOC_TEMPLATE) for doc in docs]
		context = "\n\n".join(formatted_docs)
	
		prompt = CHAT_TEMPLATE.invoke({
			"context":context,
			"query":query,
			"chat_history":self.history.messages
		})
	
		return prompt
	
	def ask(self, query):
		docs = self.retrieve(query)
		prompt = self.create_prompt(docs, query)
		chat = self.chat
		
		result = chat.invoke(prompt)
		self.history.add_user_message(query)
		self.history.add_ai_message(result.content)
		
		return result.content


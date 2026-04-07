import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv, set_key, dotenv_values
from cinebot.engine import Chatbot
from cinebot.complete_setup import complete_setup

env_path = Path(__file__).parent / '.env'

# This is make sure the Vector_db building process is not interrupted if the user interacts in between the process. 
if "building_db" not in st.session_state:
	st.session_state['building_db'] = False

# Check whether .env file exists or not.
if not env_path.exists():
    env_path.touch()
    
# Load environmental variables into the RAM.
load_dotenv(env_path)
config = dotenv_values(env_path)


db_exists = Path("./data/vector_db").exists()

# If any of the API keys or the vector_db doesn't exist prompt the user to enter the details.
if not config.get("TMDB_READ_ACCESS") or not config.get("HF_TOKEN") or not db_exists:
	st.title("Setup")

    
	with st.form(key='set_form'):
		read_access = st.text_input("Enter your TMDB Read Access Token", type="password")
		hf_token = st.text_input("Enter your Hugging Face Token", type="password")
        
		submit = st.form_submit_button("Submit")
    
	if submit:
		if read_access and hf_token:
			set_key(str(env_path), "TMDB_READ_ACCESS", read_access)
			set_key(str(env_path), "HF_TOKEN", hf_token)

			with st.status("Fetching movies' data and building vectordatabase, This might take some time", expanded=True):
				st.session_state['building_db'] = True
				complete_setup(read_access, hf_token)
				st.session_state['building_db'] = False
            	
			st.success("Setup complete! Initializing chat...")
			st.rerun() 
		else:
			st.error("Please provide both tokens.")
    
	st.stop()
	
# Store chat history in session state.
if 'message_history' not in st.session_state:
	st.session_state.message_history = []

# Store the bot in the session state so that for every message a new bot is not created.
if 'bot' not in st.session_state:
	st.session_state.bot = Chatbot(5)
	
# Write all the previous messages.
for msg in st.session_state.message_history:
	with st.chat_message(msg['role']):
		st.write(msg['content'])
	
# User input
inp = st.chat_input("Type here")

# Append user input and bot's output to message_history and also write them on the canvas.
if inp:
	st.session_state.message_history.append({'role':'user', 'content':inp})
	with st.chat_message('user'):
		st.write(inp)
	
	out = st.session_state.bot.ask(inp)
	
	st.session_state.message_history.append({'role':'assistant', 'content':out})	
	with st.chat_message('assistant'):
		st.write(out)
	
	

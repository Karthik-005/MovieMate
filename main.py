from cinebot.engine import Chatbot
import streamlit as st

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
	
	

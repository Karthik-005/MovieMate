from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder

SYSTEM_MESSAGE = "You are a movie expert and your job is to suggest movies based on the context. If the context is not sufficient then do not hallucinate, just apologize for not having enough information. Do not mention anything related to the context section in your response. You might get queries related to the previous queries, use only your previous responses in chat history to answer these queries" 

HUMAN_MESSAGE = """Answer the given query using only the following context,

Context:
{context}

Query: {query}
"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone search query. Do not answer the question, just reformulate it.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone query:"""
)

CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
	("system", SYSTEM_MESSAGE),
	MessagesPlaceholder(variable_name="chat_history"),
	("human", HUMAN_MESSAGE)
])

DOC_TEMPLATE = PromptTemplate.from_template("""Title: {Title} \n Release year: {Year_of_release} \n
                                                   Directors: {Directors} \nCast: {Cast} \nRating: {Rating} \nGenres: {genres}\n Plot: {Plot}""")

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpfully assistant"),
    MessagesPlaceholder(variable_name="history"),
    ("human","{input}")
])

llm = OllamaLLM(model="llama3")

chain = prompt | llm

session_store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

config = {"configurable": {"session_id": "demo-session"}}

# Interactions
response1 = conversational_chain.invoke({"input": "Hello, my name is Wesley. how are you?"}, config=config)
print("Assistant: ", response1)
print("-"*30)

response2 = conversational_chain.invoke({"input": "Can you repeat my name?"}, config=config)
print("Assistant: ", response2)
print("-"*30)

response3 = conversational_chain.invoke({"input": "Can you repeat my name in a motivation phrase?"}, config=config)
print("Assistant: ", response3)
print("-"*30)
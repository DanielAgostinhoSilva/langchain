from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


system = ("system", "you are an assistant that answers question in a {style} style")
user = ("user", "{question}")

chat_prompt = ChatPromptTemplate([system, user])

messages = chat_prompt.format_messages(style="funny", question="Who is Alan Turing?")

for msg in messages:
    print(f"{msg.type}: {msg.content}")

model = OllamaLLM(model="llama3")
result = model.invoke(messages)
print(result)
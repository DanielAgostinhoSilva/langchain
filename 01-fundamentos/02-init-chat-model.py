from langchain.chat_models import init_chat_model
from langchain.propts import

chat = init_chat_model(model="llama3",  model_provider="ollama")
answer_chat = chat.invoke("Hello World")
print(answer_chat.content)


template = PromptTemplate(
    input_
)
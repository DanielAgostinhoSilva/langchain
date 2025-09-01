from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


question_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a joke with my name"
)

model = OllamaLLM(model="llama3")

chain = question_template | model

result = chain.invoke({"name", "Daniel"})

print(result)
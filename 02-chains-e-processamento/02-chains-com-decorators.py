from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.runnables import chain
from langchain_ollama import OllamaLLM


@chain
def square(input_dict:dict) -> dict:
    x = input_dict["x"]
    return {"square_result": x * x}

question_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a joke with my name"
)

question_template2 = PromptTemplate(
    input_variables=["square_result"],
    template="Tell me about the numer {square_result}"
)

model = OllamaLLM(model="llama3")

chain = square | question_template2 | model

result = chain.invoke({"x":10})

print(result)
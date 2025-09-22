from langchain.tools import tool
from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import re


@tool("calculator")
def calculator(expression: str) -> str:
    """Evaluate a simple mathematical expression and return the result as a string.
    Use ONLY for simple math expressions (digits, spaces, and + - * / ( ) .)."""
    if not re.fullmatch(r"[\d+\-*/().\s]+", expression):
        return "Error: calculator only accepts simple math expressions."
    try:
        result = eval(expression)  # cuidado: apenas para exemplo didático
    except Exception as e:
        return f"Error: {e}"
    return str(result)


@tool("web_search_mock")
def web_search_mock(query: str) -> str:
    """Return the capital of a given country if it exists in the mock data."""
    data = {
        "Brazil": "Brasília",
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "United States": "Washington, D.C."

    }
    for country, capital in data.items():
        if country.lower() in query.lower():
            return f"The capital of {country} is {capital}."
    return "I don't know the capital of that country."


llm = OllamaLLM(model="llama3")
tools = [calculator, web_search_mock]

prompt = hub.pull("hwchase17/react")
agent_chain = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent_chain,
    tools=tools,
    verbose=True,
    handle_parsing_errors=(
        "Invalid format. Either provide an Action with Action Input, or a Final Answer only."
    ),
    max_iterations=3,
)

print(agent_executor.invoke({"input": "What is the capital of Iran?"}))
# print(agent_executor.invoke({"input": "How much is 10 + 10?"}))
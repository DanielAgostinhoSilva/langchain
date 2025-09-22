from langchain.tools import tool
from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
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

prompt = PromptTemplate.from_template(
    """
    Answer the following questions as best you can. You have access to the following tools.
    Only use the information you get from the tools, even if you know the answer.
    If the information is not provided by the tools, say you don't know.
    
    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Rules:
    - Use `calculator` ONLY for simple math expressions (digits and + - * / ( ) .). If input is not math, do not use calculator.
    - If an Observation says exactly "I don't know the capital of that country.", then immediately answer:
      Final Answer: I don't know the capital of that country.
      and stop.
    - If you choose an Action, do NOT include Final Answer in the same step.
    - After Action and Action Input, stop and wait for Observation.
    - Never search the internet. Only use the tools provided.
    
    Begin!
    
    Question: {input}
    {agent_scratchpad}
    """
)
agent_chain = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent_chain,
    tools=tools,
    verbose=True,
    handle_parsing_errors=(
        "Invalid format. Either provide an Action with Action Input, or a Final Answer only."
    ),
    max_iterations=4,
)

print(agent_executor.invoke({"input": "What is the capital of Iran?"}))
print(agent_executor.invoke({"input": "How much is 10 + 10?"}))
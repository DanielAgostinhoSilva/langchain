from langchain_ollama import OllamaLLM

# Inicializa o modelo via API local do Ollama
model = OllamaLLM(model="llama3")  # Você pode usar "mistral", "gemma", etc.

# Faz uma pergunta simples
message = model.invoke("Hello World")

print(message)

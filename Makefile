# Makefile para projeto de IA com LangChain + Docker Compose
.PHONY: ai-start ai-stop ai-clean ai-logs

# Comando principal para iniciar o ambiente
ai-start:
	 docker compose up

# Comando para parar os containers
ai-stop:
	 docker compose down

# Comando para remover volumes e limpar tudo
ai-clean:
	 docker compose down -v --remove-orphans

# Comando para visualizar logs
ai-logs:
	 docker compose logs -f
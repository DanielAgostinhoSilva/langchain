# langchain

Este repositório está configurado para utilizar o idioma Português do Brasil (pt-BR) em toda a documentação e nas interações.

## Ollama: Modelos suportados e como instalar (Docker Compose)

Esta seção documenta os modelos suportados pelo Ollama mais comuns no ecossistema e como instalá-los quando você sobe o serviço via `docker-compose` deste projeto.

Observação importante: a lista abaixo foca em modelos populares e amplamente usados. O Ollama suporta muitos outros modelos que podem ser consultados no catálogo oficial: https://ollama.com/library

### Modelos populares e para que servem
- llama3, llama3.1, llama3.2 (Meta Llama 3.x)
  - Propósito: modelos de uso geral (razão, escrita, perguntas e respostas). Variantes 8B/70B variam em capacidade e requisitos de hardware.
- mistral, mixtral
  - Propósito: modelos eficientes para tarefas gerais e de raciocínio leve. Mixtral (MoE) oferece bom custo/desempenho.
- phi3 (Phi-3 / Mini)
  - Propósito: modelo leve, bom para dispositivos com menos recursos e respostas rápidas em tarefas comuns.
- gemma (Google Gemma)
  - Propósito: modelo geral com bom equilíbrio entre qualidade e tamanho, adequado para geração e Q&A.
- codellama, llama3.1:instruct-code (variantes de código)
  - Propósito: assistência em programação, geração e explicação de código.
- neural-chat
  - Propósito: assistente conversacional geral treinado para diálogos úteis.
- qwen, qwen2
  - Propósito: modelos gerais fortes em raciocínio e tarefas multilingues.
- starcoder, deepseek-coder
  - Propósito: focados em código/ferramentas para desenvolvimento de software.

Nota: o nome exato do modelo no Ollama costuma ser o “slug” que você passa para `ollama pull` e para o cliente (por exemplo: `llama3`, `mistral`, `phi3`). Em alguns casos há variantes como `:instruct`, versões com tamanhos (ex.: `7b`, `8b`, `70b`) e quantizações (ex.: `q4_0`). Consulte a página do modelo para detalhes.

### Como o Ollama está configurado neste projeto

Arquivo: `docker-compose.yml`

- Serviço: `ollama`
- Imagem: `ollama/ollama`
- Porta exposta: `11434` (API HTTP)
- Volume persistente: `ollama_data` mapeado em `/root/.ollama` (mantém modelos baixados entre reinícios)
- Política de restart: `unless-stopped`
- Plataforma: `linux/arm64` (compatível com Apple Silicon)

Com isso, ao subir o compose, você terá o servidor do Ollama acessível em `http://localhost:11434`.

### Instalando modelos dentro do container (docker-compose)

Há duas formas principais:

1) Instalar manualmente após subir o serviço
- Suba o serviço:
  - `make ai-start` (ou `docker compose up`)
- Em outro terminal, entre no container:
  - `docker exec -it ollama bash`
- Dentro do container, rode o pull do(s) modelo(s):
  - `ollama pull llama3`
  - `ollama pull mistral`
  - `ollama pull phi3`
- Os modelos serão armazenados no volume `ollama_data` e permanecem disponíveis nos próximos reinícios.

1.1) Instalar via API HTTP (curl)
Se preferir, você pode pedir ao servidor Ollama (porta 11434) para baixar o modelo via API de pull. Exemplos:

- Importante: inclua o header `Content-Type: application/json` para evitar erros de parsing.
- Dica: use `-N` para ver o progresso de streaming sem buffer.

Exemplos de instalação:
- llama3:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"llama3"}'`
- mistral:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"mistral"}'`
- phi3:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"phi3"}'`
- gemma:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"gemma"}'`
- codellama:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"codellama"}'`
- qwen2 (ex.: 7B):
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"qwen2:7b"}'`
- neural-chat:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"neural-chat"}'`
- starcoder:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"starcoder"}'`
- deepseek-coder:
  - `curl -N -H "Content-Type: application/json" http://localhost:11434/api/pull -d '{"name":"deepseek-coder"}'`

Variantes e tags:
- Você pode especificar variantes, tamanhos e quantizações no nome, por exemplo:
  - `llama3:instruct`
  - `llama3:8b`
  - `qwen2:7b-q4_0`

Observação: a API de pull faz streaming em JSON; o servidor precisa estar em execução (`make ai-start`).

2) Pré-carregar modelos automaticamente na subida
Você pode ajustar o serviço no `docker-compose.yml` para executar pulls iniciais. Exemplo (modelo de snippet; adapte conforme sua necessidade):

```
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    platform: linux/arm64
    command: /bin/bash -lc "ollama serve & sleep 5 && ollama pull llama3 && ollama pull mistral && wait"
```

Notas importantes:
- `ollama serve` inicia o servidor; usamos `&` para rodar em segundo plano, aguardamos alguns segundos com `sleep` para garantir que o serviço inicialize e, então, executamos `ollama pull` dos modelos desejados. O `wait` segura o processo principal.
- Ajuste a lista de modelos (`llama3`, `mistral`, `phi3`, etc.) conforme suas necessidades.
- Em ambientes de produção, considere manejar isso via entrypoint dedicado ou scripts de inicialização mais robustos.

### Como usar um modelo neste projeto (LangChain)

O arquivo `main.py` demonstra o uso de um modelo via LangChain (cliente `langchain_ollama`). Abaixo segue um guia de Hello World completo.

#### Exemplo: Hello World com LangChain + Ollama

#### Exemplo: Hello World com init_chat_model (LangChain + Ollama + llama3)

- Script de exemplo neste repo: `01-fundamentos/02-init-chat-model.py`
- Pré‑requisitos: servidor Ollama rodando (`make ai-start`) e modelo instalado (`ollama pull llama3`).

Código mínimo:
```
from langchain.chat_models import init_chat_model
import os

base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
chat = init_chat_model(
    model="llama3",
    provider="ollama",
    config={"base_url": base_url},
)

resposta = chat.invoke("Diga 'Olá, mundo!' em português de forma curta.")
print(resposta.content)
```

Execute:
- `python 01-fundamentos/02-init-chat-model.py`

1) Suba o servidor Ollama via Docker Compose:
- `make ai-start` (ou `docker compose up`)

2) Instale um modelo dentro do container (ex.: llama3):
- `docker exec -it ollama bash`
- Dentro do container, rode: `ollama pull llama3`

3) Código mínimo (conteúdo já similar ao `main.py`):
```
from langchain_ollama import OllamaLLM

# Inicializa o modelo via API local do Ollama
llm = OllamaLLM(model="llama3")  # você pode usar "mistral", "phi3", etc.

# Faz uma pergunta simples (Hello World)
resposta = llm.invoke("Diga 'Olá, mundo!' em português")

print(resposta)
```

4) Execute o script Python localmente:
- Garanta seu ambiente Python ativo e dependências instaladas (veja `requirements.txt`).
- Rode: `python main.py`

Dicas:
- Ajuste o nome do modelo conforme o que você instalou: `llama3`, `mistral`, `phi3`.
- Se você expôs o Ollama em outra URL, você pode definir a variável de ambiente `OLLAMA_BASE_URL` (por padrão é `http://localhost:11434`).

Exemplos práticos de troca de modelo:
- `OllamaLLM(model="llama3")`
- `OllamaLLM(model="mistral")`
- `OllamaLLM(model="phi3")`

Certifique-se de ter o modelo instalado (via `ollama pull ...`) e o serviço rodando (`make ai-start`).

### Requisitos e considerações
- CPU vs GPU: alguns modelos podem usar aceleração; verifique a documentação da imagem `ollama/ollama` para suporte a GPU e variáveis específicas.
- Tamanho de modelos: modelos maiores (ex.: 70B) exigem mais RAM/VRAM; escolha variantes menores para máquinas locais com poucos recursos (ex.: 7B/8B).
- Armazenamento: o volume `ollama_data` mantém os arquivos dos modelos; garanta espaço em disco suficiente.
- Redes/Firewall: a API fica em `11434/tcp` localmente por padrão.

### Referências
- Catálogo de modelos Ollama: https://ollama.com/library
- Documentação geral: https://github.com/ollama/ollama

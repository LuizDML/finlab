# 🧪 FinLab — Seu Laboratório Financeiro com IA

> Projeto desenvolvido como parte da **Especialização em Engenharia de IA** do [Dev Eficiente](https://deveficiente.com.br), seguindo uma abordagem *code along*. As principais diferenças desta versão estão no **deploy em produção com Docker** e nas adaptações e experimentações feitas ao longo do processo.

🌐 **Acesse o projeto online:** [finlab.datamonsters.com.br](https://finlab.datamonsters.com.br)

---

## 🤔 O que é o FinLab?

O FinLab é uma aplicação que permite fazer **perguntas em linguagem natural sobre o mercado financeiro** — especificamente sobre empresas listadas na bolsa americana. Em vez de vasculhar relatórios e notícias manualmente, você simplesmente pergunta e a IA responde com base em fontes confiáveis.

Por baixo dos panos, o projeto usa uma técnica chamada **RAG (Retrieval-Augmented Generation)**, que combina dois mundos:

- 🔍 **Recuperação de informação:** busca os trechos mais relevantes em uma base vetorial (Qdrant)
- 🧠 **Geração com IA:** usa um LLM (via Groq) para responder de forma inteligente, baseado no que foi recuperado

O projeto foi construído como um exercício prático de RAG — minha formação era muito voltada ao **ML clássico**, e essa especialização foi a oportunidade de aprofundar em engenharia de sistemas de IA com LLMs.

---

## 📸 Screenshots

> 💡 *Substitua os espaços abaixo pelas imagens correspondentes.*

### Interface principal
<img width="856" height="461" alt="image" src="https://github.com/user-attachments/assets/95f877df-fbed-47dd-ab4b-92672b3252d0" />


### Exemplo de resposta (modo RAG)
<img width="906" height="601" alt="image" src="https://github.com/user-attachments/assets/867d957e-2dfc-4938-ae20-6489754609c4" />


### Exemplo de resposta (modo Agente)
<img width="820" height="478" alt="image" src="https://github.com/user-attachments/assets/4804290c-599d-4d36-ba5b-e553f8a51af8" />
<img width="795" height="542" alt="image" src="https://github.com/user-attachments/assets/56746d69-d62c-46d8-8af5-5daa7dab314a" />


### Collections no Qdrant
<img width="1173" height="296" alt="image" src="https://github.com/user-attachments/assets/13c3e261-3d09-4221-9bbe-4e7c51f82d77" />


### Estrutura dos vetores no Qdrant
<img width="1164" height="662" alt="image" src="https://github.com/user-attachments/assets/402ca872-2d0e-4069-a547-39493ee85bf2" />


## 🏗️ Como o projeto está organizado

```
finlab/
├── backend/
│   ├── ingestion/          # Scripts para popular a base vetorial
│   │   ├── create-collection.py    # Cria as collections no Qdrant
│   │   ├── create_indexes.py       # Cria os índices das collections
│   │   ├── ingestion.py            # Ingestão de dados da SEC (relatórios oficiais)
│   │   └── news_ingestion.py       # Ingestão de notícias via Yahoo Finance
│   └── main.py             # API FastAPI com os endpoints principais
├── frontend/               # Interface web (Next.js/TypeScript)
└── docker-compose.yml      # Configuração para rodar tudo com Docker
```

---

## ⚙️ Como funciona por dentro

### 1. 📥 Ingestão de dados

Antes de qualquer pergunta ser respondida, é preciso popular a base de conhecimento. Dois tipos de dados são utilizados:

- **Documentos da SEC** — relatórios oficiais de empresas americanas (10-K, 10-Q etc.)
- **Notícias financeiras** — coletadas via Yahoo Finance

Esses textos são divididos em trechos menores (*chunks*), transformados em vetores numéricos (*embeddings*) e armazenados no **Qdrant**, um banco de dados vetorial. Cada chunk vira um "ponto" na base, com seu vetor e metadados associados (empresa, data, fonte etc.).

### 2. 🔍 Busca Semântica (`POST /search`)

Quando você faz uma pergunta, ela também é transformada em vetor e uma busca por similaridade é feita no Qdrant. Os trechos mais parecidos semanticamente com a pergunta são retornados — mesmo que não compartilhem as mesmas palavras exatas.

### 3. 🤖 RAG — Geração com contexto (`POST /rag`)

Os trechos recuperados são passados como **contexto** para o LLM (via Groq API). O modelo então gera uma resposta coerente e fundamentada, sem precisar "adivinhar" — ele responde com base no que foi encontrado na base.

### 4. 🕵️ Agente (`POST /agent`)

No modo agente, o LLM tem acesso a ferramentas e pode **decidir autonomamente** quais buscas fazer antes de responder. É o modo mais poderoso: em vez de uma única busca, o agente pode encadear múltiplas consultas e raciocinar sobre elas antes de gerar a resposta final.

---

## 🔄 Diagrama de Fluxo

```
Usuário faz uma pergunta
        │
        ▼
  Pergunta vira vetor (embedding)
        │
        ▼
  Busca semântica no Qdrant
  (collections: SEC + News)
        │
        ▼
  Trechos mais relevantes são recuperados
        │
        ├──── /rag ──────▶ LLM recebe contexto e gera resposta
        │
        └──── /agent ────▶ LLM decide quais buscas fazer → gera resposta
```

---

## 🛠️ Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| **API** | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| **LLM** | [Groq API](https://groq.com/) |
| **Banco vetorial** | [Qdrant](https://qdrant.tech/) |
| **Dados financeiros** | SEC (EDGAR) + Yahoo Finance |
| **Deploy** | Docker / Docker Compose |
| **Frontend** | Next.js + TypeScript |
| **Gerenciador de deps** | [uv](https://docs.astral.sh/uv/) |

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) instalado
- Docker e Docker Compose
- Conta no [Qdrant Cloud](https://cloud.qdrant.io/) (ou instância local)
- Chave de API do [Groq](https://console.groq.com/)

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/LuizDML/finlab.git
cd finlab
```

**2. Instale as dependências do backend**
```bash
cd backend
uv sync
```

**3. Configure as variáveis de ambiente**

Crie um arquivo `.env` dentro da pasta `backend/` com o seguinte conteúdo:
```env
QDRANT_URL=https://sua-instancia.qdrant.io
QDRANT_API_KEY=sua_chave_aqui
GROQ_API_KEY=sua_chave_aqui
```

**4. Crie as collections e índices no Qdrant**
```bash
python ingestion/create-collection.py
python ingestion/create_indexes.py
```

**5. Faça a ingestão dos dados**
```bash
python ingestion/ingestion.py        # Dados da SEC
python ingestion/news_ingestion.py   # Notícias do Yahoo Finance
```

> ⚠️ Este passo pode demorar um pouco dependendo do volume de dados. Futuramente será automatizado.

**6. Suba a API**
```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

---

## 🐳 Rodando com Docker

```bash
docker compose up --build
```

Isso sobe tanto o backend quanto o frontend de uma vez.

---

## 📡 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/search` | Busca semântica pura — retorna os chunks mais relevantes |
| `POST` | `/rag` | Busca + geração: retorna uma resposta em linguagem natural com base nos documentos |
| `POST` | `/agent` | Modo agente: o LLM decide autonomamente as buscas e raciocina antes de responder |

> No frontend, os endpoints `/rag` e `/agent` são os utilizados. O modo agente é ativado marcando uma checkbox na interface.

---

## 💡 O que aprendi com esse projeto

Minha formação era muito voltada ao **ML clássico** (modelos supervisionados, feature engineering, etc.). Essa especialização foi minha porta de entrada para o universo de **LLMs e sistemas RAG** — uma área com desafios bem diferentes:

- Como estruturar e segmentar documentos para busca eficiente
- Como criar embeddings e armazenar vetores no Qdrant
- Como orquestrar LLMs com contexto externo
- Como pensar em agentes que tomam decisões autonomamente
- Como colocar tudo isso em produção de forma reproduzível com Docker

---

## 📚 Créditos

Projeto desenvolvido como exercício da **Especialização em Engenharia de IA** do [Dev Eficiente](https://deveficiente.com.br), em formato *code along*. As principais contribuições originais desta versão são o **deploy em produção com Docker** e as adaptações feitas durante o processo de aprendizado.

---

## 📬 Contato

Feito por [Luiz Almeida](https://github.com/LuizDML) — sinta-se à vontade para abrir uma issue ou entrar em contato!

# 🚀 NASA Space Apps Challenge - RAG System

Sistema de RAG desenvolvido para a competição NASA Space Apps Challenge, utilizando embeddings e LLMs para responder perguntas de cientistas e pesquisadores sobre artigos científicos.

## Sobre o Projeto

Este projeto implementa um sistema RAG completo que extrai documentos e converte em Markdown, cria embeddings vetoriais e utiliza um agente inteligente com LangGraph para responder perguntas de forma contextualizada. O sistema avalia a relevância dos documentos recuperados e reescreve perguntas quando necessário para melhorar a qualidade das respostas.

## Tecnologias Utilizadas

- **LangChain** - Framework para construção de aplicações com LLMs
- **LangGraph** - Orquestração de fluxos de agentes
- **FAISS** - Banco de dados vetorial para busca de similaridade
- **HuggingFace Embeddings** - Modelo de embeddings `sentence-transformers/all-MiniLM-L6-v2`
- **Google Gemini 2.5 Flash** - LLM para geração de respostas
- **Streamlit** - Interface web interativa
- **FastAPI** - API REST

##  Arquitetura

O projeto está dividido em três componentes principais:

### 1. Pipeline de Processamento de Documentos
- Leitura de arquivos Markdown
- Divisão por headers (H1-H4)
- Geração de embeddings
- Armazenamento em FAISS

### 2. Agente RAG Inteligente
O agente implementa um fluxo com as seguintes etapas:
- **Generate Query**: Prepara a consulta e aciona ferramentas
- **Retrieve**: Busca documentos relevantes no banco vetorial
- **Grade Documents**: Avalia se os documentos são relevantes
- **Rewrite Question**: Reformula a pergunta se necessário
- **Generate Answer**: Gera resposta contextualizada

### 3. Interface e API
- Interface web em Streamlit
- API REST para integração

### Configuração
1. Crie um arquivo `.env` com sua chave da API do Google:
```
GOOGLE_API_KEY=sua_chave_aqui
```

### Processamento dos Documentos
```bash
python process_documents.py
```

### Executar a Interface Web
```bash
streamlit run app.py
```

### Executar a API
```bash
uvicorn api:app --reload
```

## Funcionalidades

- ✅ Processamento automático de documentos Markdown
- ✅ Busca semântica com embeddings
- ✅ Avaliação de relevância de documentos
- ✅ Reescrita inteligente de perguntas
- ✅ Geração de respostas contextualizadas
- ✅ Interface web interativa
- ✅ API REST para integração

## 🏆 NASA Space Apps Challenge

Este projeto foi desenvolvido como solução para a NASA Space Apps Challenge, demonstrando como técnicas modernas de IA podem ser aplicadas para facilitar o acesso e compreensão de documentação técnica e científica.


---

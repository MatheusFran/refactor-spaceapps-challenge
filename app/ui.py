import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Configuração da página
st.set_page_config(
    page_title="NASA BioScience Explorer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configurações da API")
    api_url = st.text_input(
        "URL da API",
        value="https://api.nasa.gov/bioscience/search",
        help="Endpoint da API que retorna os dados dos experimentos"
    )
    api_key = st.text_input(
        "Chave da API (opcional)",
        type="password",
        help="Se a API requer autenticação"
    )
    st.markdown("---")
    st.header("📊 Filtros")
    show_charts = st.checkbox("Mostrar Gráficos", value=True)
    max_articles = st.slider("Máximo de Artigos", 1, 20, 10)

# --- Área principal ---
query = st.text_input(
    "🔍 Digite sua pergunta sobre bioexperimentos espaciais:",
    placeholder="Ex: Como a microgravidade afeta o crescimento de plantas?",
    key="search_query"
)

search_button = st.button("🚀 Pesquisar", use_container_width=True, type="primary")

def fetch_data(query_text, api_endpoint, api_key_value=None):
    """Faz requisição POST para a API"""
    try:
        headers = {'Content-Type': 'application/json'}
        if api_key_value:
            headers['Authorization'] = f'Bearer {api_key_value}'
        payload = {'query': query_text}
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao conectar com a API: {str(e)}")
        return None

# --- Processar busca ---
if search_button and query:
    with st.spinner('🔄 Analisando publicações da NASA...'):
        data = fetch_data(query, api_url, api_key)
        if data is None:
            st.warning("⚠️ Usando dados de demonstração")
            # Simular JSON de teste
            data = {
                "abstract": "Encontrados 3 artigos relevantes sobre microgravidade e crescimento celular.",
                "graph_datas": {
                    "experiments_timeline": {"2023": 1, "2024": 2},
                    "subject_distribution": {"Plant Biology": 1, "Human Health": 1, "Microbiology": 1},
                    "relevance_scores": [
                        {"title": "Effects of Microgravity...", "score": 0.95},
                        {"title": "Bone Density Loss...", "score": 0.88},
                        {"title": "Microbial Behavior...", "score": 0.82}
                    ]
                },
                "documents": [
                    {
                        "title": "Effects of Microgravity on Plant Growth",
                        "authors": "Smith, J., Johnson, A.",
                        "date": "2024-03-15",
                        "summary": "This study examines how microgravity affects plant cell development.",
                        "url": "https://ntrs.nasa.gov/20240001234.pdf",
                        "keywords": ["microgravity", "plants", "cell growth"],
                        "relevance": "95%"
                    },
                    # ... mais artigos
                ]
            }

        # --- Resumo ---
        st.markdown("## 📊 Resumo dos Resultados")
        st.info(data.get("abstract", "Nenhum resumo disponível"))

        # --- Métricas ---
        graph_data = data.get("graph_datas", {})
        documents = data.get("documents", [])[:max_articles]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Artigos", len(documents))
        with col2:
            if graph_data.get("relevance_scores"):
                avg_relevance = sum(d["score"] for d in graph_data["relevance_scores"]) / len(graph_data["relevance_scores"])
                st.metric("Relevância Média", f"{avg_relevance*100:.1f}%")
        with col3:
            if graph_data.get("subject_distribution"):
                st.metric("Áreas de Pesquisa", len(graph_data["subject_distribution"]))

        st.markdown("---")

        # --- Gráficos ---
        if show_charts:
            chart_col1, chart_col2 = st.columns(2)

            # Timeline
            if "experiments_timeline" in graph_data:
                st.markdown("### Experimentos por Ano")
                timeline_data = graph_data["experiments_timeline"]
                fig_timeline = go.Figure(data=[go.Bar(
                    x=list(timeline_data.keys()),
                    y=list(timeline_data.values()),
                    marker_color='rgba(77, 166, 255, 0.8)',
                    text=list(timeline_data.values()),
                    textposition='auto'
                )])
                fig_timeline.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0', xaxis_title="Ano", yaxis_title="Número de Experimentos", height=300)
                chart_col1.plotly_chart(fig_timeline, use_container_width=True)

            # Relevância
            if "relevance_scores" in graph_data:
                st.markdown("### Score de Relevância")
                rel_data = graph_data["relevance_scores"]
                fig_rel = go.Figure(data=[go.Bar(
                    y=[item["title"] for item in rel_data],
                    x=[item["score"]*100 for item in rel_data],
                    orientation='h',
                    marker_color='rgba(0, 204, 102, 0.8)',
                    text=[f"{item['score']*100:.1f}%" for item in rel_data],
                    textposition='auto'
                )])
                fig_rel.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0', xaxis_title="Relevância (%)", height=300, xaxis_range=[0,100])
                chart_col1.plotly_chart(fig_rel, use_container_width=True)

            # Distribuição por área
            if "subject_distribution" in graph_data:
                st.markdown("### Distribuição por Área")
                subject_data = graph_data["subject_distribution"]
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(subject_data.keys()),
                    values=list(subject_data.values()),
                    marker=dict(colors=['rgba(77, 166, 255, 0.8)', 'rgba(0, 204, 102, 0.8)','rgba(255, 159, 64, 0.8)'])
                )])
                fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0', height=300, showlegend=True)
                chart_col2.plotly_chart(fig_pie, use_container_width=True)

        # --- Artigos ---
        st.markdown("## 📚 Artigos Relevantes")
        if documents:
            for idx, article in enumerate(documents, 1):
                st.markdown(f"""
                    <div class="article-card">
                        <h3 style="color: #4da6ff; margin-bottom: 10px;">{idx}. {article['title']}</h3>
                        <p style="color: #888; font-size: 0.9em; margin-bottom: 10px;">
                            👥 {article['authors']} | 📅 {article['date']} | 
                            <span style="background: linear-gradient(135deg, #00cc66, #00994d); 
                                         color: white; padding: 3px 10px; border-radius: 15px; 
                                         font-weight: bold;">
                                Relevância: {article['relevance']}
                            </span>
                        </p>
                        <p style="color: #d0d0d0; line-height: 1.6; margin-bottom: 10px;">
                            {article['summary']}
                        </p>
                        <p>{' '.join(f'<span class="keyword-tag">{kw}</span>' for kw in article.get('keywords', []))}</p>
                        <a href="{article['url']}" target="_blank">🔗 Acessar Artigo Completo →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum artigo encontrado para esta consulta.")

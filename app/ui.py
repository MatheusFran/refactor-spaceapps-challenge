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

# CSS customizado para design moderno
st.markdown("""
<style>
    /* Estilo geral */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }

    /* Header personalizado */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .header-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .header-subtitle {
        color: #a8b2d1;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }

    /* Cards de artigos */
    .article-card {
        background: linear-gradient(135deg, rgba(30, 60, 114, 0.4) 0%, rgba(42, 82, 152, 0.3) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(100, 150, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .article-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(100, 150, 255, 0.4);
    }

    .article-card h3 {
        color: #64b5f6;
        margin-bottom: 10px;
        font-size: 1.4rem;
    }

    .article-card a {
        color: #81c784;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }

    .article-card a:hover {
        color: #a5d6a7;
    }

    /* Tags de keywords */
    .keyword-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px 5px 5px 0;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Métricas customizadas */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        text-align: center;
    }

    /* Botão de busca */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1f3a 0%, #0a0e27 100%);
    }

    /* Info box */
    .stAlert {
        background: linear-gradient(135deg, rgba(100, 150, 255, 0.15) 0%, rgba(100, 200, 255, 0.15) 100%);
        border: 1px solid rgba(100, 150, 255, 0.3);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header-container">
    <div class="header-title">🚀 NASA BioScience Explorer</div>
    <div class="header-subtitle">Explore experimentos espaciais e pesquisas de biociência da NASA</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configurações")

    api_url = st.text_input(
        "URL da API",
        value="http://localhost:8000/query",
        help="Endpoint da API local"
    )

    st.markdown("---")
    st.header("📊 Opções de Visualização")
    show_charts = st.checkbox("Mostrar Gráficos", value=True)
    max_articles = st.slider("Máximo de Artigos", 1, 50, 10)

    st.markdown("---")
    st.markdown("### 💡 Dicas de Busca")
    st.markdown("""
    - Seja específico na sua pergunta
    - Use termos científicos quando possível
    - Experimente diferentes formulações
    """)

# --- Área principal ---
query = st.text_input(
    "🔍 Digite sua pergunta sobre bioexperimentos espaciais:",
    placeholder="Ex: Como a microgravidade afeta o crescimento de plantas?",
    key="search_query"
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    search_button = st.button("🚀 Pesquisar", use_container_width=True, type="primary")


def fetch_data(query_text, api_endpoint):
    """Faz requisição POST para a API local"""
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {'question': query_text}
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Erro: Não foi possível conectar com a API local. Verifique se o servidor está rodando em http://localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Erro: A requisição demorou muito tempo. Tente novamente.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao conectar com a API: {str(e)}")
        return None


# --- Processar busca ---
if search_button and query:
    with st.spinner('🔄 Analisando publicações da NASA...'):
        data = fetch_data(query, api_url)

        if data is None:
            st.warning("⚠️ Usando dados de demonstração")
            # Simular JSON de teste
            data = {
                "abstract": "Encontrados 3 artigos relevantes sobre microgravidade e crescimento celular.",
                "graph_datas": {
                    "experiments_timeline": {"2020": 3, "2021": 5, "2022": 7, "2023": 4, "2024": 6},
                    "subject_distribution": {"Plant Biology": 8, "Human Health": 10, "Microbiology": 7},
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
                    {
                        "title": "Bone Density Loss in Extended Space Missions",
                        "authors": "Williams, R., Davis, K.",
                        "date": "2024-01-20",
                        "summary": "Analysis of bone density changes in astronauts during long-duration missions.",
                        "url": "https://ntrs.nasa.gov/20240001235.pdf",
                        "keywords": ["bone density", "astronauts", "health"],
                        "relevance": "88%"
                    },
                    {
                        "title": "Microbial Behavior in Space Environments",
                        "authors": "Chen, L., Martinez, S.",
                        "date": "2023-11-10",
                        "summary": "Study of bacterial growth patterns and antibiotic resistance in microgravity.",
                        "url": "https://ntrs.nasa.gov/20230005678.pdf",
                        "keywords": ["microbiology", "bacteria", "resistance"],
                        "relevance": "82%"
                    }
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
            st.metric("📚 Total de Artigos", len(documents), delta=None)
        with col2:
            if graph_data.get("relevance_scores"):
                avg_relevance = sum(d["score"] for d in graph_data["relevance_scores"]) / len(
                    graph_data["relevance_scores"])
                st.metric("⭐ Relevância Média", f"{avg_relevance * 100:.1f}%", delta=None)
            else:
                st.metric("⭐ Relevância Média", "N/A")
        with col3:
            if graph_data.get("subject_distribution"):
                st.metric("🔬 Áreas de Pesquisa", len(graph_data["subject_distribution"]), delta=None)
            else:
                st.metric("🔬 Áreas de Pesquisa", "N/A")

        st.markdown("---")

        # --- Gráficos ---
        if show_charts and graph_data:
            st.markdown("## 📈 Visualizações")

            chart_col1, chart_col2 = st.columns(2)

            # Timeline
            if "experiments_timeline" in graph_data:
                with chart_col1:
                    st.markdown("### 📅 Experimentos por Ano")
                    timeline_data = graph_data["experiments_timeline"]
                    fig_timeline = go.Figure(data=[go.Bar(
                        x=list(timeline_data.keys()),
                        y=list(timeline_data.values()),
                        marker=dict(
                            color=list(timeline_data.values()),
                            colorscale='Viridis',
                            line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                        ),
                        text=list(timeline_data.values()),
                        textposition='auto',
                        hovertemplate='<b>Ano:</b> %{x}<br><b>Experimentos:</b> %{y}<extra></extra>'
                    )])
                    fig_timeline.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0e0e0', size=12),
                        xaxis_title="Ano",
                        yaxis_title="Número de Experimentos",
                        height=350,
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)

            # Distribuição por área
            if "subject_distribution" in graph_data:
                with chart_col2:
                    st.markdown("### 🎯 Distribuição por Área")
                    subject_data = graph_data["subject_distribution"]
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=list(subject_data.keys()),
                        values=list(subject_data.values()),
                        marker=dict(
                            colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'],
                            line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
                        ),
                        textinfo='label+percent',
                        hovertemplate='<b>%{label}</b><br>Artigos: %{value}<br>Percentual: %{percent}<extra></extra>'
                    )])
                    fig_pie.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0e0e0', size=12),
                        height=350,
                        showlegend=True,
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            # Relevância (full width)
            if "relevance_scores" in graph_data:
                st.markdown("### 🎯 Score de Relevância")
                rel_data = graph_data["relevance_scores"]
                fig_rel = go.Figure(data=[go.Bar(
                    y=[item["title"][:50] + "..." if len(item["title"]) > 50 else item["title"] for item in rel_data],
                    x=[item["score"] * 100 for item in rel_data],
                    orientation='h',
                    marker=dict(
                        color=[item["score"] * 100 for item in rel_data],
                        colorscale='Greens',
                        line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                    ),
                    text=[f"{item['score'] * 100:.1f}%" for item in rel_data],
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>Relevância: %{x:.1f}%<extra></extra>'
                )])
                fig_rel.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0', size=11),
                    xaxis_title="Relevância (%)",
                    height=max(300, len(rel_data) * 50),
                    xaxis_range=[0, 100],
                    margin=dict(l=250, r=40, t=40, b=40)
                )
                st.plotly_chart(fig_rel, use_container_width=True)

        st.markdown("---")

        # --- Artigos ---
        st.markdown("## 📚 Artigos Relevantes")
        if documents:
            for idx, article in enumerate(documents, 1):
                st.markdown(f"""
                    <div class="article-card">
                        <h3>{idx}. {article.get('title', 'Sem título')}</h3>
                        <p style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 10px;">
                            👥 {article.get('authors', 'Autores não disponíveis')} | 
                            📅 {article.get('date', 'Data não disponível')} | 
                            <span style="background: linear-gradient(135deg, #00cc66, #00994d); 
                                         color: white; padding: 4px 12px; border-radius: 15px; 
                                         font-weight: bold; font-size: 0.85em;">
                                ⭐ Relevância: {article.get('relevance', 'N/A')}
                            </span>
                        </p>
                        <p style="color: #d0d0d0; line-height: 1.7; margin-bottom: 15px; font-size: 0.95em;">
                            {article.get('summary', 'Resumo não disponível')}
                        </p>
                        <p style="margin-bottom: 15px;">
                            {' '.join(f'<span class="keyword-tag">{kw}</span>' for kw in article.get('keywords', []))}
                        </p>
                        <a href="{article.get('url', '#')}" target="_blank" style="font-size: 0.95em;">
                            🔗 Acessar Artigo Completo →
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("🔍 Nenhum artigo encontrado para esta consulta. Tente reformular sua busca.")

elif search_button and not query:
    st.warning("⚠️ Por favor, digite uma pergunta antes de pesquisar.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🚀 NASA BioScience Explorer | Desenvolvido com Streamlit & Plotly</p>
    <p style="font-size: 0.85em;">Conectado à API local: <code>localhost:8000/query</code></p>
</div>
""", unsafe_allow_html=True)
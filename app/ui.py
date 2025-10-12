import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="NASA BioScience Explorer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    .stTitle {
        color: #4da6ff !important;
        text-align: center;
        font-size: 3em !important;
        text-shadow: 0 0 20px rgba(77, 166, 255, 0.5);
    }
    .stMarkdown h2 {
        color: #4da6ff;
    }
    .stMarkdown h3 {
        color: #66b3ff;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2em;
        color: #4da6ff;
    }
    .article-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4da6ff;
        margin-bottom: 15px;
    }
    .keyword-tag {
        background: rgba(77, 166, 255, 0.2);
        color: #4da6ff;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        display: inline-block;
        margin: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("🚀 NASA BioScience Explorer")
st.markdown(
    "<p style='text-align: center; color: #b0b0b0; font-size: 1.2em;'>Explore décadas de experimentos biológicos espaciais da NASA</p>",
    unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Configurações
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

    st.markdown("---")
    st.info(
        "💡 **Dica:** Digite perguntas como:\n- Como a microgravidade afeta plantas?\n- Efeitos do espaço na saúde humana\n- Experimentos com bactérias na ISS")

# Área principal - Busca
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "🔍 Digite sua pergunta sobre bioexperimentos espaciais:",
        placeholder="Ex: Como a microgravidade afeta o crescimento de plantas?",
        key="search_query"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🚀 Pesquisar", use_container_width=True, type="primary")


# Função para fazer a requisição à API
def fetch_data(query_text, api_endpoint, api_key_value=None):
    """Faz requisição POST para a API"""
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        if api_key_value:
            headers['Authorization'] = f'Bearer {api_key_value}'

        payload = {'query': query_text}

        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao conectar com a API: {str(e)}")
        return None


# Função para gerar dados mock (para demonstração)
def generate_mock_data(query_text):
    """Gera dados simulados quando a API não está disponível"""
    return {
        'summary': f"""Encontrados 3 artigos relevantes sobre "{query_text}".

Os estudos abrangem temas principais como: microgravidade, ISS, crescimento celular, saúde, bactérias.

As pesquisas incluem experimentos realizados principalmente na Estação Espacial Internacional (ISS), 
focando nos efeitos da microgravidade em sistemas biológicos.

Os resultados indicam impactos significativos em crescimento celular, saúde humana e comportamento 
microbiano em ambientes espaciais.""",
        'articles': [
            {
                'title': 'Effects of Microgravity on Plant Growth',
                'authors': 'Smith, J., Johnson, A.',
                'date': '2024-03-15',
                'summary': 'This study examines how microgravity affects plant cell development and growth patterns in space environments. Results show significant changes in root orientation and cell wall formation.',
                'url': 'https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20240001234.pdf',
                'relevance': '95.0%',
                'keywords': ['microgravity', 'plants', 'cell growth', 'ISS']
            },
            {
                'title': 'Bone Density Loss in Long-Duration Spaceflight',
                'authors': 'Williams, R., Chen, L.',
                'date': '2024-01-20',
                'summary': 'Analysis of bone density changes in astronauts during extended missions aboard the International Space Station. Study reveals critical insights for Mars missions.',
                'url': 'https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20240005678.pdf',
                'relevance': '88.0%',
                'keywords': ['bone density', 'astronauts', 'long-duration', 'health']
            },
            {
                'title': 'Microbial Behavior in Space Environments',
                'authors': 'Garcia, M., Patel, S.',
                'date': '2023-11-10',
                'summary': 'Investigation of bacterial growth patterns and antibiotic resistance in microgravity conditions. Important implications for spacecraft hygiene and crew health.',
                'url': 'https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20230009012.pdf',
                'relevance': '82.0%',
                'keywords': ['microbes', 'bacteria', 'space', 'resistance']
            }
        ],
        'charts': {
            'experiments_timeline': {
                '2023': 1,
                '2024': 2
            },
            'subject_distribution': {
                'Plant Biology': 1,
                'Human Health': 1,
                'Microbiology': 1
            },
            'relevance_scores': [
                {'title': 'Effects of Microgravity...', 'score': 0.95},
                {'title': 'Bone Density Loss...', 'score': 0.88},
                {'title': 'Microbial Behavior...', 'score': 0.82}
            ]
        },
        'total_results': 3
    }


# Processar busca
if search_button and query:
    with st.spinner('🔄 Analisando publicações da NASA...'):
        # Tentar buscar dados reais da API
        data = fetch_data(query, api_url, api_key)

        # Se falhar, usar dados mock para demonstração
        if data is None:
            st.warning("⚠️ Usando dados de demonstração (API não disponível)")
            data = generate_mock_data(query)

        if data:
            # Seção de Resumo
            st.markdown("## 📊 Resumo dos Resultados")
            st.info(data.get('summary', 'Nenhum resumo disponível'))

            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Artigos", data.get('total_results', 0))
            with col2:
                if data.get('articles'):
                    avg_relevance = sum(float(a['relevance'].rstrip('%')) for a in data['articles']) / len(
                        data['articles'])
                    st.metric("Relevância Média", f"{avg_relevance:.1f}%")
            with col3:
                if data.get('charts', {}).get('subject_distribution'):
                    st.metric("Áreas de Pesquisa", len(data['charts']['subject_distribution']))

            st.markdown("---")

            # Gráficos
            if show_charts and 'charts' in data:
                st.markdown("## 📈 Visualizações")

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    # Gráfico de Timeline
                    if 'experiments_timeline' in data['charts']:
                        st.markdown("### Experimentos por Ano")
                        timeline_data = data['charts']['experiments_timeline']
                        fig_timeline = go.Figure(data=[
                            go.Bar(
                                x=list(timeline_data.keys()),
                                y=list(timeline_data.values()),
                                marker_color='rgba(77, 166, 255, 0.8)',
                                text=list(timeline_data.values()),
                                textposition='auto'
                            )
                        ])
                        fig_timeline.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#e0e0e0',
                            xaxis_title="Ano",
                            yaxis_title="Número de Experimentos",
                            height=300
                        )
                        st.plotly_chart(fig_timeline, use_container_width=True)

                    # Gráfico de Relevância
                    if 'relevance_scores' in data['charts']:
                        st.markdown("### Score de Relevância")
                        rel_data = data['charts']['relevance_scores']
                        fig_rel = go.Figure(data=[
                            go.Bar(
                                y=[item['title'] for item in rel_data],
                                x=[item['score'] * 100 for item in rel_data],
                                orientation='h',
                                marker_color='rgba(0, 204, 102, 0.8)',
                                text=[f"{item['score'] * 100:.1f}%" for item in rel_data],
                                textposition='auto'
                            )
                        ])
                        fig_rel.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#e0e0e0',
                            xaxis_title="Relevância (%)",
                            height=300,
                            xaxis_range=[0, 100]
                        )
                        st.plotly_chart(fig_rel, use_container_width=True)

                with chart_col2:
                    # Gráfico de Distribuição por Área
                    if 'subject_distribution' in data['charts']:
                        st.markdown("### Distribuição por Área")
                        subject_data = data['charts']['subject_distribution']
                        fig_pie = go.Figure(data=[
                            go.Pie(
                                labels=list(subject_data.keys()),
                                values=list(subject_data.values()),
                                marker=dict(colors=['rgba(77, 166, 255, 0.8)', 'rgba(0, 204, 102, 0.8)',
                                                    'rgba(255, 159, 64, 0.8)'])
                            )
                        ])
                        fig_pie.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#e0e0e0',
                            height=300,
                            showlegend=True
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)

                st.markdown("---")

            # Lista de Artigos
            st.markdown("## 📚 Artigos Relevantes")

            articles = data.get('articles', [])[:max_articles]

            if articles:
                for idx, article in enumerate(articles, 1):
                    with st.container():
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
                        </div>
                        """, unsafe_allow_html=True)

                        # Keywords
                        keywords_html = "".join(
                            [f'<span class="keyword-tag">{kw}</span>' for kw in article.get('keywords', [])])
                        st.markdown(keywords_html, unsafe_allow_html=True)

                        # Link
                        st.markdown(f"[🔗 Acessar Artigo Completo →]({article['url']})")
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.warning("Nenhum artigo encontrado para esta consulta.")

elif search_button and not query:
    st.warning("⚠️ Por favor, digite uma pergunta para pesquisar!")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #888; font-size: 0.9em;'>
    🚀 NASA BioScience Explorer | Desenvolvido para explorar décadas de pesquisa espacial
</p>
""", unsafe_allow_html=True)
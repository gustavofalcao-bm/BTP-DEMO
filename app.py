# app.py v7.0 PREMIUM
# BOMTEMPO ENGENHARIA - Plataforma de Dados, BI e IA
# Versão 7.0 PREMIUM: Visual Sofisticado + Estrutura Completa v6.4

import os
import time
import base64
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ========================================== 
# ÍCONES SVG PREMIUM (LUCIDE)
# ========================================== 
ICONS = {
    'home': '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
    'analytics': '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
    'presentation': '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
    'demo': '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="10 8 16 12 10 16 10 8"></polygon></svg>',
    'chat': '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>',
    'chevron_right': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>',
}

# ========================================== 
# 1. CONFIGURAÇÃO E CSS PREMIUM
# ========================================== 
def set_page_config():
    st.set_page_config(
        page_title="BOMTEMPO | Plataforma de Dados, BI e IA",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def set_theme():
    st.markdown('''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

        :root {
            --btp-green: #0B5B3E;
            --btp-green-dark: #084932;
            --btp-green-light: #0D7050;
            --btp-gold: #C98B2A;
            --btp-gold-light: #E0A63B;
            --btp-gold-soft: #F5D78E;
            --btp-bg: #F9FAFB;
            --btp-text-main: #111827;
            --btp-text-muted: #6B7280;
            --btp-border: #E5E7EB;
            --btp-shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
            --btp-shadow-md: 0 4px 12px rgba(0,0,0,0.08);
            --btp-shadow-lg: 0 12px 32px rgba(0,0,0,0.12);
        }

        body {
            background-color: var(--btp-bg);
            color: var(--btp-text-main);
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            color: var(--btp-green);
            letter-spacing: -0.02em;
        }

        .block-container {
            padding-top: 5rem !important;
            padding-bottom: 3rem;
            max-width: 1600px;
        }

        /* SIDEBAR PREMIUM */
        section[data-testid="stSidebar"] {
            width: 300px !important;
            background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%) !important;
            border-right: 1px solid var(--btp-border);
            box-shadow: 4px 0 20px rgba(0,0,0,0.04);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem !important;
        }

        /* NAVEGAÇÃO COM ÍCONES SVG */
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.875rem 1.25rem;
            margin: 0.25rem 0.75rem;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.95rem;
            color: var(--btp-text-main);
            background: white;
            border: 1px solid var(--btp-border);
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .nav-item:hover {
            transform: translateX(4px);
            background: linear-gradient(135deg, var(--btp-green) 0%, var(--btp-green-light) 100%);
            color: white;
            border-color: var(--btp-green);
            box-shadow: var(--btp-shadow-md);
        }

        .nav-item svg {
            flex-shrink: 0;
            stroke: var(--btp-green);
            transition: stroke 0.3s;
        }

        .nav-item:hover svg {
            stroke: white;
        }

        /* BREADCRUMBS COM ÍCONES */
        .breadcrumbs {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem 0 1.5rem 0;
            margin-bottom: 1.5rem;
            font-size: 0.875rem;
            color: var(--btp-text-muted);
            border-bottom: 1px solid var(--btp-border);
        }

        .breadcrumbs a {
            color: var(--btp-green);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }

        .breadcrumbs a:hover {
            color: var(--btp-gold);
        }

        .breadcrumbs svg {
            opacity: 0.4;
        }

        /* FLIP CARDS PREMIUM 370PX */
        .flip-card {
            background-color: transparent;
            perspective: 1000px;
            height: 370px;
            margin-bottom: 1.5rem;
        }

        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
        }

        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }

        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 16px;
            border: 1.5px solid var(--btp-border);
            box-shadow: var(--btp-shadow-md);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }

        .flip-card-front {
            background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        }

        .flip-card-back {
            background: linear-gradient(135deg, var(--btp-green) 0%, var(--btp-green-light) 50%, var(--btp-gold) 100%);
            color: white;
            transform: rotateY(180deg);
            padding: 2rem 1.5rem 2.5rem 1.5rem;
            justify-content: flex-start;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .flip-card-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .flip-card-title {
            font-size: 1.5rem;
            font-weight: 800;
            font-family: 'Montserrat', sans-serif;
            color: var(--btp-green);
            margin-bottom: 0.5rem;
        }

        .flip-card-back .flip-card-title {
            color: white;
            font-size: 1.3rem;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid rgba(255,255,255,0.4);
            padding-bottom: 0.75rem;
            text-align: center;
            width: 100%;
        }

        .flip-card-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
            width: 100%;
        }

        .flip-card-list li {
            background: rgba(255,255,255,0.18);
            backdrop-filter: blur(10px);
            padding: 0.7rem 1rem;
            border-radius: 10px;
            font-size: 0.9rem;
            text-align: left;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.3s ease-out;
            border: 1px solid rgba(255,255,255,0.1);
        }

        @keyframes slideUpFade {
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .flip-card:hover .flip-card-back .flip-card-list li:nth-child(1) {
            animation: slideUpFade 0.4s 0.1s forwards;
        }

        .flip-card:hover .flip-card-back .flip-card-list li:nth-child(2) {
            animation: slideUpFade 0.4s 0.2s forwards;
        }

        .flip-card:hover .flip-card-back .flip-card-list li:nth-child(3) {
            animation: slideUpFade 0.4s 0.3s forwards;
        }

        .flip-card:hover .flip-card-back .flip-card-list li:nth-child(4) {
            animation: slideUpFade 0.4s 0.4s forwards;
        }

        /* METRIC CARDS PREMIUM */
        .metric-card {
            background: white;
            border-radius: 14px;
            padding: 1.75rem;
            border: 1.5px solid var(--btp-border);
            box-shadow: var(--btp-shadow-md);
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: linear-gradient(180deg, var(--btp-green) 0%, var(--btp-gold) 100%);
            transform: scaleY(0);
            transition: transform 0.3s;
        }

        .metric-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--btp-shadow-lg);
            border-color: var(--btp-green);
        }

        .metric-card:hover::before {
            transform: scaleY(1);
        }

        .metric-value {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            font-size: 2.2rem;
            color: var(--btp-green);
            letter-spacing: -0.03em;
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            font-size: 0.875rem;
            color: var(--btp-text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-change {
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.25rem 0.75rem;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .metric-change.positive {
            background: #DCFCE7;
            color: #166534;
        }

        .metric-change.negative {
            background: #FEE2E2;
            color: #991B1B;
        }

        /* CHAT PREMIUM */
        .chat-bubble {
            max-width: 75%;
            padding: 1.25rem 1.5rem;
            border-radius: 16px;
            line-height: 1.6;
            font-size: 0.95rem;
            margin-bottom: 1rem;
            box-shadow: var(--btp-shadow-sm);
        }

        .chat-user {
            align-self: flex-end;
            background: linear-gradient(135deg, var(--btp-green) 0%, var(--btp-green-light) 100%);
            color: white;
            border-bottom-right-radius: 4px;
            margin-left: auto;
        }

        .chat-ai {
            align-self: flex-start;
            background: white;
            border: 1.5px solid var(--btp-border);
            color: var(--btp-text-main);
            border-bottom-left-radius: 4px;
        }

        /* HERO BANNER */
        .hero-banner {
                
            display: flex;
            flex-direction: column;
            align-items: center;    
            text-align: center;
            padding: 3.5rem 2rem;
            background: linear-gradient(135deg, #f0fdf4 0%, #fff 100%);
            border-radius: 20px;
            border: 1.5px solid #dcfce7;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        }

        .hero-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(11,91,62,0.05) 0%, transparent 70%);
            animation: shimmer 8s infinite linear;
        }

        @keyframes shimmer {
            0% { transform: translate(-50%, -50%); }
            100% { transform: translate(50%, 50%); }
        }

        .hero-title {
            font-size: 2.8rem;
            margin-bottom: 1rem;
            position: relative;
            z-index: 1;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            color: var(--btp-text-muted);
            max-width: 800px;
            margin: 0 auto 2rem auto;
            position: relative;
            z-index: 1;
        }

        .hero-badges {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }

        .hero-badge {
            padding: 0.625rem 1.25rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.95rem;
            box-shadow: var(--btp-shadow-sm);
        }

        /* PROGRESS BAR */
        .progress-container {
            background: #E5E7EB;
            border-radius: 10px;
            height: 10px;
            overflow: hidden;
            margin: 0.5rem 0;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--btp-green) 0%, var(--btp-gold) 100%);
            border-radius: 10px;
            transition: width 0.5s ease;
        }

        /* DOC PREVIEW */
        .doc-preview {
            background: white;
            border: 1.5px solid var(--btp-border);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: var(--btp-shadow-md);
            margin-top: 1rem;
            position: relative;
        }

        .doc-watermark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 4rem;
            color: rgba(0,0,0,0.03);
            font-weight: 900;
            pointer-events: none;
            white-space: nowrap;
        }

        /* GRÁFICOS */
        .plot-container {
            background: white;
            border-radius: 14px;
            border: 1.5px solid var(--btp-border);
            box-shadow: var(--btp-shadow-md);
            padding: 1rem;
        }

        /* EXPANDER */
        .streamlit-expanderHeader {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: var(--btp-green);
        }

        /* BUTTON CUSTOMIZADO */
        .stButton > button {
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            border-radius: 10px;
            transition: all 0.3s;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--btp-shadow-md);
        }
        </style>
    ''', unsafe_allow_html=True)

def init_session_state():
    defaults = {
        "mode": "home",
        "demo_module": "financeiro",
        "chat_history": [],
        "apresentacao_tab": "Diagnóstico",
        "obra_selecionada": "Residencial Atlântico",
        "periodo_meses": 6
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ========================================== 
# 2. DADOS DEMO (12 MESES, 6 OBRAS)
# ========================================== 
@st.cache_data
def get_obras_data():
    return pd.DataFrame([
        {"id": 1, "nome": "Residencial Atlântico", "cidade": "Recife/PE", "status": "Em Andamento", "spi": 1.0, "cpi": 1.02, "progresso": 75, "orcamento": 8500000},
        {"id": 2, "nome": "Hospital Norte", "cidade": "Olinda/PE", "status": "Em Andamento", "spi": 0.88, "cpi": 0.95, "progresso": 65, "orcamento": 12000000},
        {"id": 3, "nome": "Comercial Centro", "cidade": "Recife/PE", "status": "Em Andamento", "spi": 1.05, "cpi": 1.08, "progresso": 82, "orcamento": 6800000},
        {"id": 4, "nome": "Shopping Boa Viagem", "cidade": "Cabo/PE", "status": "Concluída", "spi": 1.0, "cpi": 1.0, "progresso": 100, "orcamento": 9500000},
        {"id": 5, "nome": "Industrial Suape", "cidade": "Ipojuca/PE", "status": "Em Andamento", "spi": 0.92, "cpi": 0.98, "progresso": 58, "orcamento": 10200000},
        {"id": 6, "nome": "Hotel Praia", "cidade": "Porto de Galinhas/PE", "status": "Planejamento", "spi": 0.0, "cpi": 0.0, "progresso": 0, "orcamento": 12000000},
    ])

@st.cache_data
def get_financeiro_data():
    obras = get_obras_data()
    meses = pd.date_range("2025-01-01", periods=12, freq="MS")
    data = []
    np.random.seed(42)
    for _, obra in obras.iterrows():
        if obra['status'] == 'Planejamento':
            continue
        base_receita = obra['orcamento'] / 12
        base_custo = int(base_receita * 0.68)
        for mes in meses:
            variacao = 0.9 + 0.2 * np.random.random()
            data.append({
                "obra": obra['nome'],
                "mes": mes,
                "receita": base_receita * variacao,
                "custo": base_custo * variacao
            })
    df = pd.DataFrame(data)
    df['margem'] = df['receita'] - df['custo']
    return df

@st.cache_data
def get_rh_data():
    obras = get_obras_data()
    data = []
    for _, obra in obras.iterrows():
        if obra['status'] in ['Planejamento']:
            continue
        data.extend([
            {"obra": obra['nome'], "categoria": "Engenheiros", "qtd": np.random.randint(3, 8)},
            {"obra": obra['nome'], "categoria": "Técnicos", "qtd": np.random.randint(8, 15)},
            {"obra": obra['nome'], "categoria": "Operacionais", "qtd": np.random.randint(25, 60)},
        ])
    return pd.DataFrame(data)

# ========================================== 
# 3. COMPONENTES
# ========================================== 
def get_img_base64(img_path):
    if not os.path.exists(img_path):
        return ""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def find_image(candidates):
    for name in candidates:
        if os.path.exists(name):
            return name
    return None

def render_breadcrumbs():
    mode_names = {
        "home": "Página Inicial",
        "apresentacao": "Apresentação",
        "demo": "Demonstração",
        "chat": "Chat IA",
        "analytics": "Analytics"
    }
    current = mode_names.get(st.session_state.mode, "Página Inicial")
    st.markdown(f'<div class="breadcrumbs">{ICONS["home"]} <a href="#" onclick="return false;">Home</a> {ICONS["chevron_right"]} <span>{current}</span></div>', unsafe_allow_html=True)

def sidebar():
    banner_path = find_image(["BTP-BANNER.png", "btp-banner.png", "BTP-IMG.png", "BTP-BANNER.PNG"])
    with st.sidebar:
        if banner_path:
            img_b64 = get_img_base64(banner_path)
            st.markdown(f'<div style="text-align:center; padding: 1.5rem 0 2rem 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));"><img src="data:image/png;base64,{img_b64}" style="max-height: 150px; max-width: 100%;"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center; padding: 1.5rem 0 2rem 0;"><h1 style="color:#0B5B3E; font-family: Montserrat, sans-serif; font-weight: 800;">BOMTEMPO</h1></div>', unsafe_allow_html=True)

        st.markdown('<div style="padding: 0 0.75rem 1.5rem 0.75rem; font-size: 0.8rem; color: #6B7280; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">Navegação Principal</div>', unsafe_allow_html=True)

        menu_options = [
            ("home", "Página Inicial"),
            ("analytics", "Analytics"),
            ("apresentacao", "Apresentação"),
            ("demo", "Demonstração"),
            ("chat", "Chat IA"),
        ]

        for key, label in menu_options:
            if st.button(f"{label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.mode = key
                st.rerun()

        st.markdown("---")
        st.caption("© 2026 BOMTEMPO ENGENHARIA")
        st.caption("v7.0 Premium Edition")

# ========================================== 
# 4. PÁGINAS
# ========================================== 

def render_home():
    render_breadcrumbs()

    banner_path = find_image(["BTP-BANNER.png", "btp-banner.png", "BTP-BANNER.PNG"])
    if banner_path:
        img_b64 = get_img_base64(banner_path)
        st.markdown(f'''
            <div class="hero-banner">
                <img src="data:image/png;base64,{img_b64}" style="max-width: 350px; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));">
                <h1 class="hero-title">Transformação Digital para Engenharia</h1>
                <p class="hero-subtitle">
                    Centralize dados de obras, financeiro e RH em uma única plataforma inteligente. Decisões mais rápidas. Gestão mais eficiente.
                </p>
                <div class="hero-badges">
                    <span class="hero-badge" style="background: #DCFCE7; color: #166534;">✓ +40% Agilidade</span>
                    <span class="hero-badge" style="background: #FEF3C7; color: #92400E;">✓ -25% Custos</span>
                    <span class="hero-badge" style="background: #DBEAFE; color: #1E40AF;">✓ 100% LGPD</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="hero-banner">
                <h1 class="hero-title">Transformação Digital para Engenharia</h1>
                <p class="hero-subtitle">
                    Centralize dados de obras, financeiro e RH em uma única plataforma inteligente. Decisões mais rápidas. Gestão mais eficiente.
                </p>
                <div class="hero-badges">
                    <span class="hero-badge" style="background: #DCFCE7; color: #166534;">✓ +40% Agilidade</span>
                    <span class="hero-badge" style="background: #FEF3C7; color: #92400E;">✓ -25% Custos</span>
                    <span class="hero-badge" style="background: #DBEAFE; color: #1E40AF;">✓ 100% LGPD</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('<h2 style="font-family: Montserrat, sans-serif; font-weight: 800; color: #0B5B3E; margin-bottom: 0.5rem;">Soluções Integradas</h2>', unsafe_allow_html=True)
    st.caption("Passe o mouse nos cards para ver detalhes")

    c1, c2, c3 = st.columns(3)

    flip_cards_data = [
        ("🗄️", "Centralização de Dados", ["Data Lake estruturado", "ERPs integrados", "Dados em tempo real", "Histórico completo"], c1),
        ("📊", "Business Intelligence", ["Dashboards executivos", "KPIs customizados", "Análises preditivas", "Alertas inteligentes"], c2),
        ("🤖", "Inteligência Artificial", ["OCR de documentos", "Chat C-Level", "Previsão de custos", "Detecção de anomalias"], c3),
        ("💰", "ROI Comprovado", ["+15% margem operacional", "-25% custos gestão", "40% mais agilidade", "Payback 8 meses"], c1),
        ("🔐", "Segurança Enterprise", ["Compliance LGPD", "Auditoria completa", "Backup automático", "Criptografia ponta-a-ponta"], c2),
        ("⚡", "Implementação Rápida", ["Go-live em 12 semanas", "Sem disrupção", "Treinamento incluso", "Suporte 24/7"], c3),
    ]

    for icon, title, features, col in flip_cards_data:
        with col:
            features_html = "".join([f"<li>{f}</li>" for f in features])
            st.markdown(f'''
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div class="flip-card-icon">{icon}</div>
                            <div class="flip-card-title">{title}</div>
                            <p style="font-size: 0.875rem; color: #6B7280;">Passe o mouse</p>
                        </div>
                        <div class="flip-card-back">
                            <div class="flip-card-title">{title}</div>
                            <ul class="flip-card-list">
                                {features_html}
                            </ul>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)


def render_analytics():
    render_breadcrumbs()
    st.markdown('<h2 style="font-family: Montserrat, sans-serif; font-weight: 800; color: #0B5B3E;">Analytics Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("Visão consolidada de todas as obras e indicadores-chave")

    obras = get_obras_data()
    fin_data = get_financeiro_data()

    col_filter, col_spacer = st.columns([1, 3])
    with col_filter:
        periodo = st.select_slider("⏱️ Período", options=[3, 6, 12], value=6, format_func=lambda x: f"{x} meses", key="slider_analytics")

    meses_filtro = pd.date_range("2025-01-01", periods=periodo, freq="MS")
    fin_filtrado = fin_data[fin_data['mes'].isin(meses_filtro)]

    st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E; margin-top: 2rem;">Indicadores Gerais</h3>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    obras_ativas = len(obras[obras['status'] == 'Em Andamento'])
    receita_total = fin_filtrado['receita'].sum()
    custo_total = fin_filtrado['custo'].sum()
    margem_media = ((receita_total - custo_total) / receita_total * 100) if receita_total > 0 else 0
    spi_medio = obras[obras['status'] == 'Em Andamento']['spi'].mean()

    with c1:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{obras_ativas}</div>
                <div class="metric-label">Obras Ativas</div>
                <div class="metric-change positive">+1 este mês</div>
            </div>
        ''', unsafe_allow_html=True)

    with c2:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">R$ {receita_total/1e6:.1f}M</div>
                <div class="metric-label">Receita Total</div>
                <div class="metric-change positive">+15%</div>
            </div>
        ''', unsafe_allow_html=True)

    with c3:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{margem_media:.1f}%</div>
                <div class="metric-label">Margem Média</div>
                <div class="metric-change positive">+2.1%</div>
            </div>
        ''', unsafe_allow_html=True)

    with c4:
        change_class = "negative" if spi_medio < 1 else "positive"
        change_text = "-0.04" if spi_medio < 1 else "+0.04"
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{spi_medio:.2f}</div>
                <div class="metric-label">SPI Médio</div>
                <div class="metric-change {change_class}">{change_text}</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Evolução Financeira ({periodo} Meses)</h3>', unsafe_allow_html=True)
        fin_mensal = fin_filtrado.groupby('mes').agg({'receita': 'sum', 'custo': 'sum'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fin_mensal['mes'], 
            y=fin_mensal['receita']/1e6, 
            name="Receita", 
            line=dict(color='#0B5B3E', width=3),
            fill='tonexty',
            fillcolor='rgba(11, 91, 62, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=fin_mensal['mes'], 
            y=fin_mensal['custo']/1e6, 
            name="Custo", 
            line=dict(color='#C98B2A', width=3)
        ))
        fig.update_layout(
            template='plotly_white',
            yaxis_title="R$ (Milhões)",
            height=350,
            hovermode='x unified',
            font=dict(family='Montserrat'),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Top 3 Obras</h3>', unsafe_allow_html=True)
        obras_ranking = obras[obras['status'] == 'Em Andamento'].copy()
        obras_ranking['score'] = obras_ranking['spi'] + obras_ranking['cpi'] / 2
        obras_ranking = obras_ranking.sort_values('score', ascending=False).head(3)

        for i, (_, obra) in enumerate(obras_ranking.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            border_color = '#0B5B3E' if i==1 else '#C98B2A' if i==2 else '#6B7280'
            st.markdown(f'''
                <div style="background: white; padding: 1rem; border-radius: 12px; margin-bottom: 0.75rem; border-left: 4px solid {border_color}; box-shadow: 0 2px 6px rgba(0,0,0,0.06);">
                    <div style="font-size: 1.2rem; font-family: Montserrat, sans-serif; font-weight: 600;">{medal} {obra['nome']}</div>
                    <div style="font-size: 0.875rem; color: #6B7280; margin-top: 0.25rem;">Score: {obra['score']:.2f} • {obra['progresso']}% completo</div>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Heatmap de Performance</h3>', unsafe_allow_html=True)

    heatmap_data = obras[obras['status'] == 'Em Andamento'][['nome', 'spi', 'cpi', 'progresso']].copy()
    heatmap_data['spi_pct'] = heatmap_data['spi'] * 100
    heatmap_data['cpi_pct'] = heatmap_data['cpi'] * 100

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=[heatmap_data['spi_pct'], heatmap_data['cpi_pct'], heatmap_data['progresso']],
        x=heatmap_data['nome'],
        y=['SPI (%)', 'CPI (%)', 'Progresso (%)'],
        colorscale='RdYlGn',
        text=[[f"{v:.0f}%" for v in heatmap_data['spi_pct']],
              [f"{v:.0f}%" for v in heatmap_data['cpi_pct']],
              [f"{v:.0f}%" for v in heatmap_data['progresso']]],
        texttemplate='%{text}',
        textfont={"size": 12, "family": "Montserrat"}
    ))
    fig_heatmap.update_layout(
        template='plotly_white', 
        height=250,
        font=dict(family='Montserrat')
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("---")
    st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Previsão IA - Próximos 3 Meses</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">R$ 14.2M</div>
                <div class="metric-label">Receita Prevista</div>
                <div class="metric-change positive">+13.6%</div>
                <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6B7280;">Tendência de crescimento mantida</div>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">36.8%</div>
                <div class="metric-label">Margem Prevista</div>
                <div class="metric-change positive">+2.4%</div>
                <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6B7280;">Otimização de custos em curso</div>
            </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">2</div>
                <div class="metric-label">Obras Finalizadas</div>
                <div style="margin-top: 1rem; font-size: 0.8rem; color: #6B7280;">Shopping + Comercial Centro</div>
            </div>
        ''', unsafe_allow_html=True)

def render_apresentacao():
    render_breadcrumbs()
    st.markdown('<h2 style="font-family: Montserrat, sans-serif; font-weight: 800; color: #0B5B3E;">Visão Geral da Plataforma</h2>', unsafe_allow_html=True)

    tabs = ["Diagnóstico", "Arquitetura", "Módulos", "Tecnologia", "Roadmap"]
    cols = st.columns(5)

    for i, tab in enumerate(tabs):
        with cols[i]:
            if st.button(tab, key=f"tab_{tab}", use_container_width=True):
                st.session_state.apresentacao_tab = tab
                st.rerun()

    st.markdown("---")
    active_tab = st.session_state.apresentacao_tab

    if active_tab == "Diagnóstico":
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">O Cenário Atual da Construção Civil</h3>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('''
            #### 🚨 Problemas Identificados

            **1. Dados Fragmentados**
            - Planilhas Excel desconectadas
            - ERPs que não conversam entre si
            - Informações duplicadas e conflitantes

            **2. Decisões Atrasadas**
            - Relatórios manuais demoram dias
            - Informação chega tarde para correção
            - Gestores sem visibilidade em tempo real

            **3. Estouro de Orçamento**
            - 68% das obras excedem o budget
            - Média de 15% de custo extra
            - Falta de controle preditivo
            ''')

        with c2:
            st.markdown('''
            #### 💡 Consequências no Negócio

            **Impacto Financeiro**
            - R$ 2.5M perdidos/ano em retrabalho
            - 30% do tempo gasto em buscas
            - Margem operacional reduzida

            **Impacto Operacional**
            - Equipes desmotivadas
            - Clientes insatisfeitos
            - Riscos de compliance (LGPD)
            ''')

            st.info("💡 **Insight:** Sem centralização de dados, você gerencia pelo retrovisor, não pelo GPS.")

        st.markdown("---")
        st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">A Solução: Plataforma Integrada</h4>', unsafe_allow_html=True)

        cols_sol = st.columns(4)
        solucoes = [
            ("🗄️", "Data Lake", "Centraliza todos os dados"),
            ("📊", "BI em Tempo Real", "Dashboards executivos"),
            ("🤖", "IA Preditiva", "Antecipa problemas"),
            ("📱", "Mobile First", "Acesso de qualquer lugar")
        ]

        for i, (icon, titulo, desc) in enumerate(solucoes):
            with cols_sol[i]:
                st.markdown(f'''
                <div style="text-align:center; padding:1.75rem; background:white; border-radius:14px; border: 2px solid #0B5B3E; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <div style="font-size:2.5rem; margin-bottom: 0.75rem;">{icon}</div>
                    <h4 style="font-family: Montserrat, sans-serif; color: #0B5B3E; margin-bottom: 0.5rem;">{titulo}</h4>
                    <p style="font-size:0.875rem; color:#6B7280; margin: 0;">{desc}</p>
                </div>
                ''', unsafe_allow_html=True)

    elif active_tab == "Arquitetura":
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Arquitetura Medalhão (Data Lakehouse)</h3>', unsafe_allow_html=True)

        st.markdown('''
        A plataforma utiliza a **Arquitetura Medalhão**, padrão do setor para Data Lakes modernos, 
        garantindo qualidade, governança e performance.
        ''')

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('''
            <div style="background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); color: white; padding: 2rem; border-radius: 14px; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <h3 style="color: white; font-family: Montserrat, sans-serif;">🥉 Camada Bronze (Raw)</h3>
                <p><strong>Dados Brutos</strong></p>
                <ul style="padding-left: 1.25rem;">
                    <li>ERP SAP Business One</li>
                    <li>Planilhas Excel legadas</li>
                    <li>APIs de fornecedores</li>
                    <li>Sensores IoT de obras</li>
                    <li>E-mails e documentos</li>
                </ul>
                <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
                <p style="font-size: 0.875rem;"><em>Ingestão sem transformação<br>Dados como chegam</em></p>
            </div>
            ''', unsafe_allow_html=True)

        with c2:
            st.markdown('''
            <div style="background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%); color: white; padding: 2rem; border-radius: 14px; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <h3 style="color: white; font-family: Montserrat, sans-serif;">🥈 Camada Prata (Trusted)</h3>
                <p><strong>Dados Limpos</strong></p>
                <ul style="padding-left: 1.25rem;">
                    <li>Validação de tipos</li>
                    <li>Remoção de duplicatas</li>
                    <li>Padronização de campos</li>
                    <li>Enriquecimento com APIs</li>
                    <li>Histórico versionado</li>
                </ul>
                <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
                <p style="font-size: 0.875rem;"><em>Qualidade garantida<br>Fonte confiável para analistas</em></p>
            </div>
            ''', unsafe_allow_html=True)

        with c3:
            st.markdown('''
            <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #333; padding: 2rem; border-radius: 14px; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <h3 style="font-family: Montserrat, sans-serif;">🥇 Camada Ouro (Refined)</h3>
                <p><strong>KPIs Prontos</strong></p>
                <ul style="padding-left: 1.25rem;">
                    <li>Margem de contribuição</li>
                    <li>SPI/CPI por obra</li>
                    <li>Curva ABC de fornecedores</li>
                    <li>Produtividade por equipe</li>
                    <li>Análises preditivas (ML)</li>
                </ul>
                <hr style="border-color: rgba(0,0,0,0.2); margin: 1rem 0;">
                <p style="font-size: 0.875rem;"><em>Consumo direto no Power BI<br>Performance otimizada</em></p>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Fluxo de Dados End-to-End</h4>', unsafe_allow_html=True)
        st.code('''
        [ERPs/APIs/IoT] 
            ↓ (Ingestão Azure Data Factory)
        [🥉 BRONZE: Raw Data Lake] 
            ↓ (Transformação Databricks/PySpark)
        [🥈 PRATA: Delta Tables Validadas] 
            ↓ (Agregação SQL/DAX)
        [🥇 OURO: KPIs & ML Models] 
            ↓ (Visualização)
        [📊 Power BI / Streamlit / Mobile App]
        ''', language="text")

    elif active_tab == "Módulos":
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Módulos da Plataforma</h3>', unsafe_allow_html=True)

        modulos_detalhes = [
            {
                "icon": "💰",
                "nome": "Financeiro & Controladoria",
                "features": [
                    "DRE por obra (mensal/acumulado)",
                    "Fluxo de caixa projetado 12 meses",
                    "Margem de contribuição por cliente",
                    "Análise de desvio orçamentário",
                    "Integração bancária (OFX)"
                ],
                "kpis": ["EBITDA", "Margem Líquida", "ROI", "Payback"]
            },
            {
                "icon": "🏗️",
                "nome": "Produção & Obras",
                "features": [
                    "Curva S (Planejado x Realizado)",
                    "Medição digital de empreiteiros",
                    "Diário de obra georreferenciado",
                    "Controle de apontamento de horas",
                    "Timeline de marcos críticos"
                ],
                "kpis": ["SPI", "CPI", "EAC", "% Físico"]
            },
            {
                "icon": "✅",
                "nome": "Qualidade & Segurança",
                "features": [
                    "FVS - Ficha de Verificação de Serviço",
                    "Registro de não-conformidades",
                    "Análise de causas (Ishikawa/5 Porquês)",
                    "Checklist de segurança NR-18",
                    "Certificações ISO integradas"
                ],
                "kpis": ["Taxa NC", "LTIF", "Retrabalho %"]
            },
            {
                "icon": "📦",
                "nome": "Suprimentos & Logística",
                "features": [
                    "Curva ABC de fornecedores",
                    "Prazo médio de compras (PMC)",
                    "Controle de estoque (Kanban visual)",
                    "Cotação eletrônica (3 orçamentos)",
                    "Rastreamento de entregas (integração transportadora)"
                ],
                "kpis": ["Giro Estoque", "Lead Time", "% On-time"]
            },
            {
                "icon": "👷",
                "nome": "RH & Gestão de Pessoas",
                "features": [
                    "Headcount por obra/função",
                    "Controle de ponto biométrico",
                    "Gestão de treinamentos NR",
                    "Avaliação de desempenho 360°",
                    "Integração eSocial"
                ],
                "kpis": ["Turnover", "Absenteísmo", "Produtividade"]
            },
            {
                "icon": "🤖",
                "nome": "IA & Machine Learning",
                "features": [
                    "OCR de notas fiscais (extração automática)",
                    "Classificação de documentos (NLP)",
                    "Previsão de custos (Regressão)",
                    "Detecção de anomalias (Isolation Forest)",
                    "Chatbot C-Level (RAG com GPT-4)"
                ],
                "kpis": ["Acurácia", "Economia IA", "Tempo economizado"]
            }
        ]

        cols = st.columns(2)
        for i, mod in enumerate(modulos_detalhes):
            with cols[i % 2]:
                with st.expander(f"{mod['icon']} **{mod['nome']}**", expanded=(i < 2)):
                    st.markdown("**Funcionalidades:**")
                    for feat in mod['features']:
                        st.markdown(f"- {feat}")
                    st.markdown(f"**KPIs Principais:** {', '.join(mod['kpis'])}")

    elif active_tab == "Tecnologia":
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Stack Tecnológico Enterprise</h3>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### ☁️ Cloud & Infraestrutura")
            st.markdown('''
            - **Azure** (Data Lake Gen2, Data Factory, Databricks)
            - **AWS** (S3 backup, Lambda edge functions)
            - **Docker** + **Kubernetes** (orquestração containers)
            - **Terraform** (IaC - Infrastructure as Code)
            - **Azure DevOps** (CI/CD pipelines)
            ''')

            st.markdown("#### 🗄️ Dados & Processamento")
            st.markdown('''
            - **SQL Server 2022** (OLTP transacional)
            - **Azure Synapse** (Data Warehouse)
            - **Databricks** (PySpark para Big Data)
            - **Delta Lake** (ACID transactions)
            - **Redis** (cache distribuído)
            ''')

        with c2:
            st.markdown("#### 📊 Analytics & BI")
            st.markdown('''
            - **Power BI Premium** (reports corporativos)
            - **Streamlit** (apps customizados Python)
            - **Plotly/Dash** (dashboards interativos)
            - **Tableau** (análises ad-hoc)
            ''')

            st.markdown("#### 🤖 IA & Automação")
            st.markdown('''
            - **Azure OpenAI** (GPT-4, embeddings)
            - **Scikit-learn / XGBoost** (ML clássico)
            - **LangChain** (RAG e agentes)
            - **N8N / Zapier** (automação workflows)
            - **Python 3.11** (core development)
            ''')

        st.markdown("---")
        st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Métricas de Qualidade</h4>', unsafe_allow_html=True)

        metricas = st.columns(4)
        with metricas[0]:
            st.markdown('''
                <div class="metric-card">
                    <div class="metric-value">Azure</div>
                    <div class="metric-label">Cloud Tier</div>
                    <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6B7280;">Premium 99.9% SLA</div>
                </div>
            ''', unsafe_allow_html=True)
        with metricas[1]:
            st.markdown('''
                <div class="metric-card">
                    <div class="metric-value">SQL</div>
                    <div class="metric-label">Banco</div>
                    <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6B7280;">Enterprise Edition</div>
                </div>
            ''', unsafe_allow_html=True)
        with metricas[2]:
            st.markdown('''
                <div class="metric-card">
                    <div class="metric-value">Power BI</div>
                    <div class="metric-label">BI Tool</div>
                    <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6B7280;">Premium Capacity</div>
                </div>
            ''', unsafe_allow_html=True)
        with metricas[3]:
            st.markdown('''
                <div class="metric-card">
                    <div class="metric-value">GPT-4</div>
                    <div class="metric-label">IA Model</div>
                    <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6B7280;">Azure OpenAI</div>
                </div>
            ''', unsafe_allow_html=True)

    elif active_tab == "Roadmap":
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Roadmap de Implantação (12 Semanas)</h3>', unsafe_allow_html=True)

        st.markdown('''
            <div class="progress-container" style="height: 16px; margin: 1rem 0 0.5rem 0;">
                <div class="progress-bar" style="width: 100%;"></div>
            </div>
        ''', unsafe_allow_html=True)
        st.caption("✅ Cronograma validado com 15+ projetos similares no setor")

        roadmap_fases = [
            {
                "fase": "Fase 1: Discovery & Setup",
                "semanas": "Semanas 1-2",
                "cor": "#0B5B3E",
                "atividades": [
                    "Kick-off e alinhamento de stakeholders",
                    "Mapeamento de processos AS-IS",
                    "Inventário de fontes de dados",
                    "Provisionamento infraestrutura Azure",
                    "Setup DevOps e repositórios Git"
                ],
                "entregavel": "Documento de Arquitetura + Ambiente Dev"
            },
            {
                "fase": "Fase 2: Data Foundation",
                "semanas": "Semanas 3-5",
                "cor": "#C98B2A",
                "atividades": [
                    "Configuração Data Lake (Bronze/Silver/Gold)",
                    "Pipelines de ingestão (ERP → Bronze)",
                    "Transformações iniciais (Bronze → Silver)",
                    "Modelagem dimensional (Silver → Gold)",
                    "Testes de qualidade de dados"
                ],
                "entregavel": "Data Warehouse operacional + 3 dashboards piloto"
            },
            {
                "fase": "Fase 3: BI & Analytics",
                "semanas": "Semanas 6-8",
                "cor": "#10A878",
                "atividades": [
                    "Desenvolvimento dashboards Power BI",
                    "Criação de medidas DAX avançadas",
                    "Integração com Streamlit (apps custom)",
                    "Configuração Row-Level Security",
                    "Treinamento usuários-chave (Power Users)"
                ],
                "entregavel": "15 dashboards + Documentação + Treinamento"
            },
            {
                "fase": "Fase 4: IA & Go-Live",
                "semanas": "Semanas 9-12",
                "cor": "#6366F1",
                "atividades": [
                    "Implementação modelos ML (custos, prazos)",
                    "Deploy chatbot RAG (GPT-4 + embeddings)",
                    "Testes de carga e performance",
                    "Documentação técnica completa",
                    "Go-Live assistido + Suporte 24/7 (30 dias)"
                ],
                "entregavel": "Plataforma em Produção + SLA ativo"
            }
        ]

        for fase_info in roadmap_fases:
            with st.expander(f"**{fase_info['fase']}** ({fase_info['semanas']})", expanded=True):
                st.markdown(f"<div style='border-left: 4px solid {fase_info['cor']}; padding-left: 1.5rem;'>", unsafe_allow_html=True)
                st.markdown("**Atividades:**")
                for ativ in fase_info['atividades']:
                    st.markdown(f"- {ativ}")
                st.success(f"✅ **Entregável:** {fase_info['entregavel']}")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Marcos Críticos</h4>', unsafe_allow_html=True)

        marcos = st.columns(3)
        marcos[0].markdown('''
        **🚀 Kick-off**  
        Semana 1  
        *10/02/2026*
        ''')
        marcos[1].markdown('''
        **🎯 Checkpoint**  
        Semana 6  
        *24/03/2026*
        ''')
        marcos[2].markdown('''
        **✅ Go-Live**  
        Semana 12  
        *05/05/2026*
        ''')


def render_demo():
    render_breadcrumbs()
    st.markdown('<h2 style="font-family: Montserrat, sans-serif; font-weight: 800; color: #0B5B3E;">Demonstração Interativa</h2>', unsafe_allow_html=True)

    obras = get_obras_data()
    fin_data = get_financeiro_data()
    rh_data = get_rh_data()

    cols = st.columns(4)
    modulos = [
        ("financeiro", "💰 Financeiro"),
        ("rh", "👷 RH"),
        ("obras", "🏗️ Obras"),
        ("ia", "🤖 IA")
    ]

    for i, (key, label) in enumerate(modulos):
        with cols[i]:
            if st.button(label, key=f"btn_mod_{key}", use_container_width=True):
                st.session_state.demo_module = key
                st.rerun()

    st.markdown("---")

    if st.session_state.demo_module == "financeiro":
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            obra_sel = st.selectbox("🏗️ Obra", options=obras['nome'].tolist(), key="fin_obra", label_visibility="collapsed")
        with c2:
            periodo = st.select_slider("⏱️ Período", options=[3, 6, 12], value=6, format_func=lambda x: f"{x}m", key="fin_periodo")

        meses_filtro = pd.date_range("2025-01-01", periods=periodo, freq="MS")
        df_obra = fin_data[(fin_data['obra'] == obra_sel) & (fin_data['mes'].isin(meses_filtro))]

        c1, c2, c3, c4 = st.columns(4)
        receita_total = df_obra['receita'].sum()
        custo_total = df_obra['custo'].sum()
        margem_total = receita_total - custo_total
        margem_pct = (margem_total / receita_total * 100) if receita_total > 0 else 0

        with c1:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">R$ {receita_total/1e6:.1f}M</div>
                    <div class="metric-label">Receita</div>
                </div>
            ''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">R$ {custo_total/1e6:.1f}M</div>
                    <div class="metric-label">Custo</div>
                </div>
            ''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">R$ {margem_total/1e6:.1f}M</div>
                    <div class="metric-label">Margem</div>
                </div>
            ''', unsafe_allow_html=True)
        with c4:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{margem_pct:.1f}%</div>
                    <div class="metric-label">Margem %</div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E; margin-top: 2rem;">Evolução Financeira</h4>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_obra['mes'].dt.strftime('%b'), 
            y=df_obra['receita']/1e6, 
            name="Receita", 
            marker_color='#0B5B3E'
        ))
        fig.add_trace(go.Scatter(
            x=df_obra['mes'].dt.strftime('%b'), 
            y=df_obra['custo']/1e6, 
            name="Custo", 
            line=dict(color='#C98B2A', width=3)
        ))
        fig.update_layout(
            template='plotly_white', 
            yaxis_title="R$ (Milhões)", 
            height=350,
            font=dict(family='Montserrat')
        )
        st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.demo_module == "obras":
        c1, c2 = st.columns([1, 3])
        with c1:
            obra_sel = st.selectbox("🏗️ Obra", options=obras['nome'].tolist(), key="obras_obra", label_visibility="collapsed")
            obra_info = obras[obras['nome'] == obra_sel].iloc[0]
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{obra_info['spi']:.2f}</div>
                    <div class="metric-label">SPI</div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="metric-card" style="margin-top: 1rem;">
                    <div class="metric-value">{obra_info['cpi']:.2f}</div>
                    <div class="metric-label">CPI</div>
                </div>
            ''', unsafe_allow_html=True)

        with c2:
            st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Curva S</h4>', unsafe_allow_html=True)
            x = np.linspace(0, 100, 100)
            y_plan = (1 / (1 + np.exp(-0.1 * (x - 50)))) * 100
            y_real = (1 / (1 + np.exp(-0.1 * (x - 55)))) * 100

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_plan, name="Planejado", line=dict(color='#0B5B3E', width=3)))
            fig.add_trace(go.Scatter(
                x=x[:80], 
                y=y_real[:80], 
                name="Realizado", 
                fill='tozeroy',
                fillcolor='rgba(201, 139, 42, 0.2)',
                line=dict(color='#C98B2A', width=3)
            ))
            fig.update_layout(
                template='plotly_white', 
                height=350,
                font=dict(family='Montserrat')
            )
            st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.demo_module == "rh":
        obra_sel = st.selectbox("🏗️ Obra", options=obras[obras['status'] != 'Planejamento']['nome'].tolist(), key="rh_obra")
        df_rh = rh_data[rh_data['obra'] == obra_sel]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Headcount</h4>', unsafe_allow_html=True)
            fig = px.pie(
                df_rh, 
                values='qtd', 
                names='categoria', 
                color_discrete_sequence=['#0B5B3E', '#10A878', '#C98B2A'], 
                hole=0.5
            )
            fig.update_layout(font=dict(family='Montserrat'))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Absenteísmo</h4>', unsafe_allow_html=True)
            df2 = pd.DataFrame({'Semana': [1,2,3,4], 'Taxa': [2.5, 3.1, 1.8, 2.2]})
            fig2 = px.bar(df2, x='Semana', y='Taxa', color_discrete_sequence=['#C98B2A'])
            fig2.update_layout(font=dict(family='Montserrat'))
            st.plotly_chart(fig2, use_container_width=True)

    elif st.session_state.demo_module == "ia":
        st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">IA & Machine Learning</h3>', unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["📄 OCR", "🔍 Anomalias", "📁 Classificação", "🔮 Previsão"])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.info("📄 **NF 4521**\n\nAço Brasil\n\nR$ 45.230")
            with c2:
                st.success("✅ **Extraído:**\n\n12.345.678/0001-90")

        with tab2:
            np.random.seed(42)
            x = np.arange(30)
            y = 100 + np.random.normal(0, 5, 30)
            y[15] = 140
            y[22] = 145
            colors = ['#DC2626' if v > 120 else '#10A878' for v in y]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=10, color=colors)))
            fig.add_hline(y=120, line_dash='dash', line_color='#DC2626', line_width=2)
            fig.update_layout(
                template='plotly_white', 
                height=300,
                font=dict(family='Montserrat')
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            df_docs = pd.DataFrame({'Documento': ['Contrato.pdf', 'Laudo.pdf'], 'Categoria': ['Jurídico', 'Técnico']})
            st.dataframe(df_docs, use_container_width=True, hide_index=True)

        with tab4:
            obras_ml = obras[obras['status'] == 'Em Andamento'][['nome', 'spi']].copy()
            obras_ml['Risco'] = obras_ml['spi'].apply(lambda x: 'Alto' if x < 0.90 else 'Baixo')
            st.dataframe(obras_ml, use_container_width=True, hide_index=True)

def simulate_typing(placeholder):
    with st.empty():
        for text in ["Analisando...", "Processando...", "Gerando..."]:
            placeholder.caption(f"⏳ {text}")
            time.sleep(0.3)
        placeholder.empty()

def generate_pdf_report_rich(buffer):
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFillColorRGB(0.043, 0.357, 0.243)
    c.rect(0, height-100, width, 100, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height-60, "RELATÓRIO DE PERFORMANCE")

    c.setFont("Helvetica", 12)
    c.drawString(50, height-85, f"BOMTEMPO ENGENHARIA | {datetime.now().strftime('%d/%m/%Y')}")

    c.saveState()
    c.translate(width/2, height/2)
    c.rotate(45)
    c.setFont("Helvetica-Bold", 60)
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.drawCentredString(0, 0, "CONFIDENCIAL")
    c.restoreState()

    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "1. RESUMO EXECUTIVO")

    c.setFont("Helvetica", 11)
    y_pos = height - 165
    resumo = [
        "Análise consolidada do portfólio de 6 obras ativas.",
        "Performance financeira com margem média de 34.4%, crescimento de 15% no trimestre.",
        "Identificadas 2 obras com atenção necessária (Hospital Norte e Industrial Suape)."
    ]
    for linha in resumo:
        c.drawString(50, y_pos, linha)
        y_pos -= 20

    c.setFont("Helvetica-Bold", 14)
    y_pos -= 30
    c.drawString(50, y_pos, "2. INDICADORES CONSOLIDADOS (KPIs)")

    y_pos -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y_pos, "Indicador")
    c.drawString(200, y_pos, "Valor")
    c.drawString(300, y_pos, "Meta")
    c.drawString(400, y_pos, "Status")

    y_pos -= 5
    c.line(50, y_pos, 550, y_pos)

    kpis = [
        ("Receita Total", "R$ 12.5M", "R$ 10.8M", "✓ Superou"),
        ("EBITDA", "R$ 3.1M", "R$ 2.8M", "✓ Superou"),
        ("Margem Operacional", "34.4%", "32.0%", "✓ Superou"),
        ("SPI Médio", "0.96", "1.00", "⚠ Atenção"),
        ("Obras Ativas", "5", "5", "✓ Conforme")
    ]

    c.setFont("Helvetica", 10)
    for kpi in kpis:
        y_pos -= 20
        c.drawString(60, y_pos, kpi[0])
        c.drawString(200, y_pos, kpi[1])
        c.drawString(300, y_pos, kpi[2])
        c.drawString(400, y_pos, kpi[3])

    y_pos -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, "3. STATUS DE OBRAS")

    y_pos -= 25
    c.setFont("Helvetica", 10)
    obras_status = [
        "✅ Residencial Atlântico: 75% completo, SPI 1.00 (no prazo)",
        "⚠️ Hospital Norte: 65% completo, SPI 0.88 (atraso crítico - 2 semanas)",
        "✅ Comercial Centro: 82% completo, SPI 1.05 (adiantado)",
        "✅ Shopping Boa Viagem: 100% concluída (dentro do orçamento)",
        "⚠️ Industrial Suape: 58% completo, SPI 0.92 (leve atraso - 5 dias)"
    ]

    for obra in obras_status:
        y_pos -= 18
        c.drawString(60, y_pos, obra)

    y_pos -= 35
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, "4. RECOMENDAÇÕES ESTRATÉGICAS (IA)")

    y_pos -= 25
    c.setFont("Helvetica", 10)
    recomendacoes = [
        "1. Acelerar Hospital Norte com aumento de equipe (+20%) - Investimento: R$ 200k",
        "   ROI esperado: Evitar multa de R$ 450k por atraso contratual.",
        "",
        "2. Renegociar preço de aço com fornecedores (mercado caiu 8% no trimestre)",
        "   Economia projetada: R$ 620k no portfólio total.",
        "",
        "3. Implementar gate de aprovação para compras acima de R$ 50k",
        "   Reduz desvios orçamentários em 12% (benchmark setor)."
    ]

    for rec in recomendacoes:
        y_pos -= 15
        if y_pos < 100:
            c.showPage()
            y_pos = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(60, y_pos, rec)

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 40, "Confidencial - BOMTEMPO Engenharia | Documento gerado automaticamente pela Plataforma de BI")
    c.drawRightString(width - 50, 40, f"Página 1 | Código: REL-{datetime.now().strftime('%Y%m%d%H%M%S')}")

    c.save()
    buffer.seek(0)
    return buffer

def generate_report_html():
    date_str = datetime.now().strftime("%d/%m/%Y")
    return f'''
        <div class="doc-preview">
            <div class="doc-watermark">CONFIDENCIAL</div>
            <h2 style="color:#0B5B3E; font-family: Montserrat, sans-serif;">📊 RELATÓRIO EXECUTIVO</h2>
            <p><strong>BOMTEMPO ENGENHARIA</strong> | {date_str}</p>

            <h3 style="font-family: Montserrat, sans-serif; color: #0B5B3E;">1. Resumo Executivo</h3>
            <p>Evolução de <strong>+15% na margem</strong> operacional no trimestre.</p>

            <h3 style="font-family: Montserrat, sans-serif; color: #0B5B3E;">2. Recomendações IA</h3>
            <div style="background:#F0FDF4; border-left:4px solid #0B5B3E; padding:1rem; border-radius: 8px;">
                <p>💡 Renegociar aço. <strong>Economia: R$ 450k</strong>.</p>
            </div>
        </div>
    '''

def render_chat():
    render_breadcrumbs()
    st.markdown('<h2 style="font-family: Montserrat, sans-serif; font-weight: 800; color: #0B5B3E;">Assistente Virtual C-Level</h2>', unsafe_allow_html=True)

    for idx, msg in enumerate(st.session_state.chat_history):
        role_class = "chat-user" if msg['role'] == 'user' else "chat-ai"
        st.markdown(f'<div class="chat-bubble {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

        if msg.get('is_report'):
            st.markdown(generate_report_html(), unsafe_allow_html=True)
            pdf_buffer = generate_pdf_report_rich(BytesIO())
            st.download_button(
                "📥 Baixar PDF",
                data=pdf_buffer,
                file_name=f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="primary",
                key=f"pdf_download_{idx}"
            )

    st.markdown("---")
    st.markdown('<h4 style="font-family: Montserrat, sans-serif; font-weight: 700; color: #0B5B3E;">Sugestões</h4>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    prompt = None
    with c1:
        if st.button("💰 Custos", key="p1"):
            prompt = "Análise de custos."
    with c2:
        if st.button("⏱️ Cronograma", key="p2"):
            prompt = "Status de prazo."
    with c3:
        if st.button("📊 Relatório", key="p3"):
            prompt = "Gere relatório."
    with c4:
        if st.button("🔮 Previsão", key="p4"):
            prompt = "Previsão fluxo."

    user_input = st.chat_input("Digite sua pergunta...")
    final_prompt = prompt if prompt else user_input

    if final_prompt:
        st.session_state.chat_history.append({"role": "user", "content": final_prompt})

        placeholder_typing = st.empty()
        simulate_typing(placeholder_typing)

        is_report = "relatório" in final_prompt.lower() or "relatorio" in final_prompt.lower()

        if is_report:
            resposta = "📊 **Relatório Gerado com Sucesso!** \n\nResumo executivo do portfólio de obras, com análises financeiras e recomendações estratégicas."
        elif "custo" in final_prompt.lower():
            resposta = "💰 **Análise de Custos:**\n\nCusto total consolidado: R$ 32.5M (últimos 6 meses).\nPrincipais drivers: Aço (+28%), Mão de obra (+18%).\nRecomendação: Renegociação com fornecedores."
        elif "prazo" in final_prompt.lower() or "cronograma" in final_prompt.lower():
            resposta = "⏱️ **Status de Cronograma:**\n\n5 obras em andamento. SPI médio: 0.96 (leve atraso).\n**Atenção:** Hospital Norte com 2 semanas de atraso."
        elif "previsão" in final_prompt.lower() or "previsao" in final_prompt.lower():
            resposta = "🔮 **Previsão de Fluxo de Caixa:**\n\nReceita projetada próximos 3 meses: R$ 14.2M (+13.6%).\nMargem esperada: 36.8%.\n2 obras serão concluídas."
        else:
            resposta = f"Entendi sua pergunta sobre '{final_prompt}'. Como assistente de BI, posso te ajudar com análises de custos, cronogramas, relatórios e previsões financeiras. Use os botões de sugestão acima!"

        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": resposta,
            "is_report": is_report
        })

        st.rerun()

# ========================================== 
# 5. MAIN
# ========================================== 
def main():
    set_page_config()
    set_theme()
    init_session_state()

    sidebar()

    if st.session_state.mode == "home":
        render_home()
    elif st.session_state.mode == "analytics":
        render_analytics()
    elif st.session_state.mode == "apresentacao":
        render_apresentacao()
    elif st.session_state.mode == "demo":
        render_demo()
    elif st.session_state.mode == "chat":
        render_chat()

if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Balanço & Perdas | Neo x Bio", layout="wide")

PRIMARY = "#00695C"
WARN    = "#FFC107"
POS     = "#2E7D32"
NEG     = "#C62828"
BG_APP  = "#F6F7F9"
BG_CARD = "#FFFFFF"
TINT_A  = "#E8F5F3"  # teal tint
TINT_B  = "#FFF8E1"  # amber tint

st.markdown(r'''
<style>
/* App background */
.stApp {background: %s;}
/* Section wrappers */
.section {
    border-radius: 18px;
    padding: 16px 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
    margin-bottom: 14px;
}
.sectionA { background: %s; }
.sectionB { background: %s; }

/* Titles */
h1, h2, h3 { font-weight: 800; letter-spacing: .2px; }

/* KPI cards */
.kpi {
    background:%s;
    border:1px solid #eef0f2;
    border-radius:16px;
    padding:14px 16px;
    box-shadow:0 1px 2px rgba(0,0,0,.04);
}
.kpi .title {font-size:.95rem;color:#111827;font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:8px}
.kpi .value {font-size:1.45rem;font-weight:800}
.kpi .aux {font-size:.85rem;color:#6b7280;margin-top:2px}

/* Colored top borders for emphasis */
.kpi.teal    { border-top: 5px solid %s; }
.kpi.amber   { border-top: 5px solid %s; }
.kpi.positive{ border-top: 5px solid %s; }
.kpi.negative{ border-top: 5px solid %s; }

.grid3 {display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.grid4 {display:grid;grid-template-columns:repeat(4,1fr);gap:12px}

hr{margin:10px 0 14px 0}
</style>
''' % (BG_APP, TINT_A, TINT_B, BG_CARD, PRIMARY, WARN, POS, NEG), unsafe_allow_html=True)

def br_money(x: float) -> str:
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def t_fmt(x: float, nd=3) -> str:
    return f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("Balanço de Produção & Perdas (Neo → Bio)")

# ---------- Sidebar (shared inputs) ----------
with st.sidebar:
    st.header("⚙️ Entradas gerais")
    moagem_por_dia = st.number_input("Moagem (t/dia) enviada", min_value=0.0, value=35.0, step=1.0, format="%.3f", key="sb_moagem_dia")
    dias_bio = st.number_input("Dias em produção na Bio", min_value=0, value=25, step=1, key="sb_dias_bio")
    st.caption("Essas entradas alimentam a seção de Perdas Estimadas.")

# ========== Seção 1: Balanço de Produção (Etanol & Vinhaça) ==========
st.header("1) Balanço de produção de etanol e vinhaça (saídas calculadas)")
with st.container():
    st.markdown('<div class="section sectionA">', unsafe_allow_html=True)
    st.caption("As três saídas abaixo são calculadas pelas fórmulas do Excel informadas.")

    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    with col_in1:
        F5_vazao_vinho = st.number_input("F5 • Vazão do vinho (m³/h)", min_value=0.0, value=100.0, step=0.1, format="%.3f", key="f5")
    with col_in2:
        F6_ds_vinho = st.number_input("F6 • %Ds do vinho (%)", min_value=0.0, value=8.5, step=0.1, format="%.3f", key="f6")
    with col_in3:
        F7_conc_ww = st.number_input("F7 • Concentração em massa (w/w)", min_value=0.0, value=14.5, step=0.1, format="%.3f", key="f7")
    with col_in4:
        I8_v1 = st.number_input("I8 • V1 (kgv/L etoh)", min_value=0.0, value=1.65, step=0.01, format="%.3f", key="i8")

    # Constantes
    rho_etoh = 0.789   # t/m3 (kg/L)
    fator_9515 = 0.9515

    # Saídas (fórmulas do Excel)
    etanol_m3h = (F7_conc_ww / rho_etoh) / fator_9515
    vinhaca_m3h = F5_vazao_vinho - F7_conc_ww + (I8_v1 * (F7_conc_ww / rho_etoh))
    ds_vinhaca_perc = F6_ds_vinho / vinhaca_m3h

    # KPIs de saída
    st.markdown('<div class="grid3">', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi teal"><div class="title">🍶 Etanol hidratado (saída)</div><div class="value">{t_fmt(etanol_m3h)} m³/h</div><div class="aux">= F7/0,789/0,9515</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi amber"><div class="title">♨️ Vinhaça (saída)</div><div class="value">{t_fmt(vinhaca_m3h)} m³/h</div><div class="aux">= F5 − F7 + ( I8 × (F7/0,789) )</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi teal"><div class="title">🧪 %%Ds da Vinhaça (saída)</div><div class="value">{t_fmt(ds_vinhaca_perc, nd=2)} %</div><div class="aux">= F6 / Vinhaça</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ========== Seção 2: Perdas Estimadas (Óleo, DDGS, Etanol) ==========
st.header("2) Perdas estimadas (óleo, DDGS) e ganho com etanol (Bio)")
with st.container():
    st.markdown('<div class="section sectionB">', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 1.2])
    with col_left:
        st.subheader("Entradas financeiras e rendimentos")
        preco_oleo_rpt = st.number_input("Óleo - preço líquido (R$/t)", min_value=0.0, value=5000.0, step=50.0, format="%.2f", key="sb_preco_oleo")
        preco_ddgs_rpt = st.number_input("DDGS - preço líquido (R$/t)", min_value=0.0, value=1000.0, step=50.0, format="%.2f", key="sb_preco_ddgs")
        preco_etanol = st.number_input("Etanol (R$/t ou m³)", min_value=0.0, value=2800.0, step=50.0, format="%.2f", key="sb_preco_etanol")
        rendimento_oleo_kgpt = st.number_input("Rendimento de Óleo (kg/t)", min_value=0.0, value=19.0, step=0.1, format="%.2f", key="sb_rend_oleo")
        rendimento_ddgs_kgpt = st.number_input("Rendimento de DDGS (kg/t)", min_value=0.0, value=250.0, step=1.0, format="%.1f", key="sb_rend_ddgs")
        modo_etanol = st.radio("Etanol (período)", ["Capacidade por dia × dias", "Total direto"], index=0, key="sb_modo_etanol")
        if modo_etanol == "Capacidade por dia × dias":
            etanol_por_dia = st.number_input("Produção de etanol (t/dia ou m³/dia)", min_value=0.0, value=463.546, step=1.0, format="%.3f", key="sb_etanol_por_dia")
            etanol_total = etanol_por_dia * dias_bio
        else:
            etanol_total = st.number_input("Etanol total no período (t ou m³)", min_value=0.0, value=11588.666, step=1.0, format="%.3f", key="sb_etanol_total")

    with col_right:
        # Cálculos perdas
        moagem_total = moagem_por_dia * dias_bio
        oleo_perdido_t = (moagem_total * (rendimento_oleo_kgpt / 1000.0))
        ddgs_perdido_t = (moagem_total * (rendimento_ddgs_kgpt / 1000.0))

        valor_oleo_perdido = oleo_perdido_t * preco_oleo_rpt
        valor_ddgs_perdido = ddgs_perdido_t * preco_ddgs_rpt
        valor_etanol_produzido = etanol_total * preco_etanol
        financeiro_total = -valor_oleo_perdido - valor_ddgs_perdido + valor_etanol_produzido

        # KPIs financeiros
        st.markdown('<div class="grid4">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi negative"><div class="title">🛢️ Perda de Óleo</div><div class="value">{t_fmt(oleo_perdido_t)} t</div><div class="aux">{br_money(-valor_oleo_perdido)}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi negative"><div class="title">🌾 Perda de DDGS</div><div class="value">{t_fmt(ddgs_perdido_t)} t</div><div class="aux">{br_money(-valor_ddgs_perdido)}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi positive"><div class="title">🍶 Etanol produzido (Bio)</div><div class="value">{t_fmt(etanol_total)} t/m³</div><div class="aux">{br_money(valor_etanol_produzido)}</div></div>', unsafe_allow_html=True)
        klass = "positive" if financeiro_total >= 0 else "negative"
        st.markdown(f'<div class="kpi {klass}"><div class="title">💰 Total financeiro</div><div class="value">{br_money(financeiro_total)}</div><div class="aux">= −Óleo −DDGS + Etanol</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Obs.: Etanol, Vinhaça e %%Ds da Vinhaça são saídas calculadas. App ignora custos/margens de vapor.")

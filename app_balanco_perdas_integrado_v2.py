
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Balanço & Perdas | Neo x Bio", layout="wide")

PRIMARY = "#00695C"
POS     = "#2E7D32"
NEG     = "#C62828"
BG      = "#ffffff"

st.markdown(r'''
<style>
.kpi {background:%s;border:1px solid #eef0f2;border-radius:16px;padding:14px 16px;box-shadow:0 1px 2px rgba(0,0,0,.04);}
.kpi .title {font-size:.95rem;color:#111827;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:8px}
.kpi .value {font-size:1.4rem;font-weight:800}
.grid4 {display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.total-pos {border-left:6px solid %s}
.total-neg {border-left:6px solid %s}
</style>
''' % (BG, POS, NEG), unsafe_allow_html=True)

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
st.caption("As três saídas abaixo (vazão de etanol, vazão de vinhaça e %Ds da vinhaça) são calculadas pelas fórmulas do Excel informadas.")

col_in1, col_in2, col_in3, col_in4 = st.columns(4)
with col_in1:
    F5_vazao_vinho = st.number_input("F5 Vazão do vinho (m³/h)", min_value=0.0, value=100.0, step=0.1, format="%.3f", key="f5")
with col_in2:
    F6_ds_vinho = st.number_input("F6 %Ds do vinho (%)", min_value=0.0, value=8.5, step=0.1, format="%.3f", key="f6")
with col_in3:
    F7_conc_ww = st.number_input("F7 Conc. em massa (w/w)", min_value=0.0, value=14.5, step=0.1, format="%.3f", key="f7")
with col_in4:
    I8_v1 = st.number_input("I8 V1 (kgv/L etoh)", min_value=0.0, value=1.65, step=0.01, format="%.3f", key="i8")

# Constantes do seu cálculo
rho_etoh = 0.789   # t/m3 (ou kg/L)
fator_9515 = 0.9515

# Saídas (fórmulas do Excel)
etanol_m3h = (F7_conc_ww / rho_etoh) / fator_9515                  # =F7/0,789/0,9515
vinhaca_m3h = F5_vazao_vinho - F7_conc_ww + (I8_v1 * (F7_conc_ww / rho_etoh))  # =F5-F7+(I8*(F7/0,789))
ds_vinhaca_perc = F6_ds_vinho / vinhaca_m3h                        # =F6 / (F5-F7+ (I8*(F7/0,789)) )

# KPIs de saída
st.markdown('<div class="grid4">', unsafe_allow_html=True)
st.markdown(f'<div class="kpi"><div class="title">🍶 Etanol hidratado (saída)</div><div class="value">{t_fmt(etanol_m3h)} m³/h</div><div class="aux">= F7/0,789/0,9515</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kpi"><div class="title">♨️ Vinhaça (saída)</div><div class="value">{t_fmt(vinhaca_m3h)} m³/h</div><div class="aux">= F5 - F7 + ( I8 * (F7/0,789) )</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kpi"><div class="title">🧪 %Ds da Vinhaça (saída)</div><div class="value">{t_fmt(ds_vinhaca_perc, nd=2)} %</div><div class="aux">= F6 / Vinhaça</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ========== Seção 2: Perdas Estimadas (Óleo, DDGS, Etanol) ==========
st.header("2) Perdas estimadas (óleo, DDGS) e ganho com etanol (Bio)")

with st.sidebar:
    st.header("💵 Preços líquidos (R$/t)")
    preco_oleo_rpt = st.number_input("Óleo - preço líquido", min_value=0.0, value=5000.0, step=50.0, format="%.2f", key="sb_preco_oleo")
    preco_ddgs_rpt = st.number_input("DDGS - preço líquido", min_value=0.0, value=1000.0, step=50.0, format="%.2f", key="sb_preco_ddgs")
    preco_etanol = st.number_input("Etanol (R$/t ou m3)", min_value=0.0, value=2800.0, step=50.0, format="%.2f", key="sb_preco_etanol")

    st.header("🧪 Rendimentos (por t de moagem)")
    rendimento_oleo_kgpt = st.number_input("Óleo (kg/t)", min_value=0.0, value=19.0, step=0.1, format="%.2f", key="sb_rend_oleo")
    rendimento_ddgs_kgpt = st.number_input("DDGS (kg/t)", min_value=0.0, value=250.0, step=1.0, format="%.1f", key="sb_rend_ddgs")

    st.header("🍶 Etanol produzido na Bio (período)")
    modo_etanol = st.radio("Como informar etanol?", ["Capacidade por dia × dias", "Total direto"], index=0, key="sb_modo_etanol")
    if modo_etanol == "Capacidade por dia × dias":
        etanol_por_dia = st.number_input("Produção de etanol (t/dia ou m3/dia)", min_value=0.0, value=463.546, step=1.0, format="%.3f", key="sb_etanol_por_dia")
        etanol_total = etanol_por_dia * dias_bio
    else:
        etanol_total = st.number_input("Etanol total no período (t ou m3)", min_value=0.0, value=11588.666, step=1.0, format="%.3f", key="sb_etanol_total")

# Cálculos perdas
moagem_total = moagem_por_dia * dias_bio
oleo_perdido_t = (moagem_total * (rendimento_oleo_kgpt / 1000.0))
ddgs_perdido_t = (moagem_total * (rendimento_ddgs_kgpt / 1000.0))

valor_oleo_perdido = oleo_perdido_t * preco_oleo_rpt
valor_ddgs_perdido = ddgs_perdido_t * preco_ddgs_rpt
valor_etanol_produzido = etanol_total * preco_etanol
financeiro_total = -valor_oleo_perdido - valor_ddgs_perdido + valor_etanol_produzido

# Cards
st.markdown('<div class="grid4">', unsafe_allow_html=True)
st.markdown(f'<div class="kpi"><div class="title">🛢️ Perda de Óleo</div><div class="value">{t_fmt(oleo_perdido_t)} t</div><div class="aux">{br_money(-valor_oleo_perdido)}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kpi"><div class="title">🌾 Perda de DDGS</div><div class="value">{t_fmt(ddgs_perdido_t)} t</div><div class="aux">{br_money(-valor_ddgs_perdido)}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kpi"><div class="title">🍶 Etanol produzido (Bio)</div><div class="value">{t_fmt(etanol_total)} t/m3</div><div class="aux">{br_money(valor_etanol_produzido)}</div></div>', unsafe_allow_html=True)
tot_class = "total-pos" if financeiro_total >= 0 else "total-neg"
st.markdown(f'<div class="kpi {tot_class}"><div class="title">💰 Total financeiro</div><div class="value">{br_money(financeiro_total)}</div><div class="aux">= -Óleo -DDGS + Etanol</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("Obs.: não foi considerado valores financeiros do vapor")

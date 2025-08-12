
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Balanço & Perdas | Neo x Bio", layout="wide")

PRIMARY = "#00695C"
WARN    = "#FFC107"
POS     = "#2E7D32"
NEG     = "#C62828"
BG_APP  = "#F6F7F9"
BG_CARD = "#FFFFFF"
TINT_A  = "#E8F5F3"
TINT_B  = "#FFF8E1"

st.markdown(rf'''
<style>
.stApp, section.main, div[data-testid="stAppViewContainer"], div.block-container {{ background: {BG_APP} !important; }}
div[data-testid="stSidebar"] {{ background: #ffffff !important; }}
.section {{ border-radius: 18px; padding: 16px 18px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,.04); margin-bottom: 14px; }}
.sectionA {{ background: {TINT_A}; }}
.sectionB {{ background: {TINT_B}; }}
h1, h2, h3 {{ font-weight: 800; letter-spacing: .2px; }}
.kpi {{ background:{BG_CARD}; border:1px solid #eef0f2; border-radius:16px; padding:14px 16px; box-shadow:0 1px 2px rgba(0,0,0,.04); }}
.kpi .title {{font-size:.95rem;color:#111827;font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:8px}}
.kpi .value {{font-size:1.45rem;font-weight:800}}
.kpi .aux {{font-size:.85rem;color:#6b7280;margin-top:2px}}
.kpi.teal    {{ border-top: 5px solid {PRIMARY}; }}
.kpi.amber   {{ border-top: 5px solid {WARN}; }}
.kpi.positive{{ border-top: 5px solid {POS}; }}
.kpi.negative{{ border-top: 5px solid {NEG}; }}
.grid3 {{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.grid4 {{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
hr{{margin:10px 0 14px 0}}
</style>
''', unsafe_allow_html=True)

def br_money(x: float) -> str:
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def t_fmt(x: float, nd=3) -> str:
    return f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("Balanço de Produção & Perdas (Neo → Bio)")

# ---------- Sidebar (entradas gerais) ----------
with st.sidebar:
    st.header("⚙️ Entradas gerais")
    moagem_por_dia = st.number_input("Moagem (t/dia) enviada", min_value=0.0, value=35.0, step=1.0, format="%.3f", key="sb_moagem_dia")
    dias_bio = st.number_input("Dias em produção na Bio", min_value=0, value=25, step=1, key="sb_dias_bio")
    st.caption("As entradas abaixo definem as saídas calculadas do balanço e alimentam as perdas estimadas.")

# ========== Seção 1: Balanço (etanol & vinhaça) — saídas calculadas ==========
st.header("1) Balanço de produção de etanol e vinhaça (saídas calculadas)")
st.markdown('<div class="section sectionA">', unsafe_allow_html=True)

col_in1, col_in2, col_in3, col_in4 = st.columns(4)
with col_in1:
    F5_vazao_vinho = st.number_input("F5 • Vazão do vinho (m³/h)", min_value=0.0, value=100.0, step=0.1, format="%.3f", key="f5")
with col_in2:
    F6_ds_vinho = st.number_input("F6 • %Ds do vinho (%)", min_value=0.0, value=8.5, step=0.1, format="%.3f", key="f6")
with col_in3:
    F7_conc_ww = st.number_input("F7 • Concentração em massa (w/w, %)", min_value=0.0, value=14.5, step=0.1, format="%.3f", key="f7")
with col_in4:
    I8_v1 = st.number_input("I8 • V1 (kgv/L etoh)", min_value=0.0, value=1.65, step=0.01, format="%.3f", key="i8")

rho_etoh = 0.789
fator_9515 = 0.9515

# Etanol usa F5 * F7%
etanol_m3h = (F5_vazao_vinho * (F7_conc_ww/100.0)) / rho_etoh / fator_9515
F7_massa_equivalente = F5_vazao_vinho * (F7_conc_ww/100.0)
# Vinhaça conforme sua equação original (com F7 "direto"):
vinhaca_m3h_formula = F5_vazao_vinho - F7_conc_ww + (I8_v1 * (F7_conc_ww / rho_etoh))
# Para consistência, mantenho a card principal usando essa fórmula:
vinhaca_m3h = vinhaca_m3h_formula
# %Ds da vinhaça = F6 / (F5 - F7 + I8*(F7/0,789))  → é fração. Para exibir, multiplicamos por 100.
ds_vinhaca_frac = F6_ds_vinho / vinhaca_m3h if vinhaca_m3h else 0.0
ds_vinhaca_percent = ds_vinhaca_frac * 100.0

horas_periodo = 24 * dias_bio
etanol_total_periodo = etanol_m3h * horas_periodo  # m3 no período

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f'<div class="kpi teal"><div class="title">🍶 Etanol hidratado (saída)</div><div class="value">{t_fmt(etanol_m3h)} m³/h</div><div class="aux">(F5×F7%%)/0,789/0,9515</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kpi amber"><div class="title">♨️ Vinhaça (saída)</div><div class="value">{t_fmt(vinhaca_m3h)} m³/h</div><div class="aux">F5 − F7 + I8×(F7/0,789)</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="kpi teal"><div class="title">🧪 %Ds da Vinhaça (saída)</div><div class="value">{t_fmt(ds_vinhaca_percent, nd=2)} %</div><div class="aux">F6 / (F5 − F7 + I8×(F7/0,789))</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ========== Seção 2: Perdas Estimadas (Óleo, DDGS, Etanol) ==========
st.header("2) Perdas estimadas (óleo, DDGS) e ganho com etanol (Bio)")
st.markdown('<div class="section sectionB">', unsafe_allow_html=True)

col_left, col_right = st.columns([1.1, 1.2])
with col_left:
    st.subheader("Entradas financeiras e rendimentos")
    preco_oleo_rpt = st.number_input("Óleo - preço líquido (R$/t)", min_value=0.0, value=5000.0, step=50.0, format="%.2f", key="sb_preco_oleo")
    preco_ddgs_rpt = st.number_input("DDGS - preço líquido (R$/t)", min_value=0.0, value=1000.0, step=50.0, format="%.2f", key="sb_preco_ddgs")
    preco_etanol = st.number_input("Etanol (R$/m³)", min_value=0.0, value=2800.0, step=50.0, format="%.2f", key="sb_preco_etanol")
    rendimento_oleo_kgpt = st.number_input("Rendimento de Óleo (kg/t)", min_value=0.0, value=19.0, step=0.1, format="%.2f", key="sb_rend_oleo")
    rendimento_ddgs_kgpt = st.number_input("Rendimento de DDGS (kg/t)", min_value=0.0, value=250.0, step=1.0, format="%.1f", key="sb_rend_ddgs")

with col_right:
    moagem_total = moagem_por_dia * dias_bio
    oleo_perdido_t = (moagem_total * (rendimento_oleo_kgpt / 1000.0))
    ddgs_perdido_t = (moagem_total * (rendimento_ddgs_kgpt / 1000.0))

    valor_oleo_perdido = oleo_perdido_t * preco_oleo_rpt
    valor_ddgs_perdido = ddgs_perdido_t * preco_ddgs_rpt
    valor_etanol_produzido = etanol_total_periodo * preco_etanol
    financeiro_total = -valor_oleo_perdido - valor_ddgs_perdido + valor_etanol_produzido

    st.markdown('<div class="grid4">', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi negative"><div class="title">🛢️ Perda de Óleo </div><div class="value">{t_fmt(oleo_perdido_t)} t</div><div class="aux">{br_money(-valor_oleo_perdido)}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi negative"><div class="title">🌾 Perda de DDGS </div><div class="value">{t_fmt(ddgs_perdido_t)} t</div><div class="aux">{br_money(-valor_ddgs_perdido)}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi positive"><div class="title">🍶 Etanol produzido </div><div class="value">{t_fmt(etanol_total_periodo)} m³</div><div class="aux">{br_money(valor_etanol_produzido)}</div></div>', unsafe_allow_html=True)
    klass = "positive" if financeiro_total >= 0 else "negative"
    st.markdown(f'<div class="kpi {klass}"><div class="title">💰 Total financeiro</div><div class="value">{br_money(financeiro_total)}</div><div class="aux">= −Óleo −DDGS + Etanol</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.caption("Obs.: %Ds exibido como porcentagem (fração × 100). Etanol = (F5×F7%%)/0,789/0,9515. Vinhaça = F5 − F7 + I8×(F7/0,789).")

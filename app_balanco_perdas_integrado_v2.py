
import streamlit as st

st.set_page_config(page_title="Balanço Neo Bio — Completo (Standalone)", layout="wide")

# ================= THEME / STYLE =================
PRIMARY = "#0B7A75"
NEG     = "#C62828"
POS     = "#2E7D32"
BG_APP  = "#F6F7F9"
BG_CARD = "#FFFFFF"

css = """
<style>
.stApp, section.main, div[data-testid='stAppViewContainer'], div.block-container {{
  background: {bg_app} !important;
}}
.card {{
  background:{bg_card}; border:1px solid #eef0f2; border-radius:16px; padding:14px 16px; box-shadow:0 1px 3px rgba(0,0,0,.05);
}}
.grid2 {{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.grid3 {{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.badge {{
  display:inline-flex; align-items:center; gap:6px; padding:2px 8px; border-radius:999px; font-size:.75rem;
  border:1px solid #e5e7eb; background:#fff; margin-left:8px
}}
.badge.formula {{ background:#E8F5E9; border-color:#C8E6C9; }}
.badge.variar  {{ background:#FFF3E0; border-color:#FFE0B2; }}
.badge.fixo    {{ background:#ECEFF1; border-color:#CFD8DC; }}
.lock::before  {{ content:"🔒"; }}
.slider::before{{ content:"🛠️"; }}
.fx::before    {{ content:"∑"; }}
h2{{margin-top:8px}}
</style>
""".format(bg_app=BG_APP, bg_card=BG_CARD)

st.markdown(css, unsafe_allow_html=True)

def fmt(x, nd=3):
    try:
        return f"{float(x):,.{nd}f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return str(x)

st.title("Balanço Neo Bio — Aba Completo (sem planilha)")

# ================= ENTRADAS FIXAS (não variam no app) =================
# Edite aqui se precisar mudar os fixos
C4_CANA_FIXO   = 0.0   # Cana
C5_K_CANA_FIXO = 0.0   # K Cana (kg/t)

# ===================== 1) DADOS DA BIO =====================
st.header("1) Dados da Bio")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.write("**Cana (C4)**", "<span class='badge fixo lock'>Fixo</span>", unsafe_allow_html=True)
    C4 = C4_CANA_FIXO
    st.markdown(f"<div class='card' style='font-size:1.25rem'>{fmt(C4)}</div>", unsafe_allow_html=True)
with col2:
    st.write("**K Cana (C5) [kg/t]**", "<span class='badge fixo lock'>Fixo</span>", unsafe_allow_html=True)
    C5 = C5_K_CANA_FIXO
    st.markdown(f"<div class='card' style='font-size:1.25rem'>{fmt(C5)}</div>", unsafe_allow_html=True)
with col3:
    C6 = st.number_input("Vazão do vinho (C6) m³/h", min_value=0.0, value=100.0, step=0.5, format="%.3f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)
with col4:
    st.empty()

col5, col6 = st.columns(2)
with col5:
    C8 = st.number_input("%Ds do vinho (C8) [%]", min_value=0.0, value=8.5, step=0.1, format="%.3f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)
with col6:
    C9 = st.number_input("Concentração em massa / GL (C9) [%]", min_value=0.0, value=14.5, step=0.1, format="%.3f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)

# ----- Fórmulas (iguais à planilha) -----
C7  = (C4*C5/C6) if C6 else 0.0
C10 = (-0.244*C9 + 4.564)
C11 = (C6*C9/96.0*C10)
C12 = (C6*C9/96.0)
C13 = (C12*24.0)
C14 = (C12*1.2)
C15 = (C6 - C12*0.789 + C11 - C14)
C16 = (C6 / C8 / C15) if (C8 and C15) else 0.0
C17 = (C5*C4/C15) if C15 else 0.0

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C7 K vinho</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C7)}</div><div>Fórmula = C4*C5/C6</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C11 V1 total as is (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C11)}</div><div>Fórmula = C6*C9/96*C10</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C12 Etanol as is (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C12)}</div><div>Fórmula = C6*C9/96</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C13 Etanol to be (m³/dia)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C13)}</div><div>Fórmula = C12*24</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C14 Flegmassa (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C14)}</div><div>Fórmula = C12*1.2</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C15 Vinhaça (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C15)}</div><div>Fórmula = C6 - C12*0.789 + C11 - C14</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C16 %Sólidos na vinhaça</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C16*100,2)} %</div><div>Fórmula = C6/C8/C15</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C17 K vinhaça</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C17)}</div><div>Fórmula = C5*C4/C15</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ C10 Consumo específico (as is)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(C10,3)}</div><div>Fórmula = -0.244*C9 + 4.564</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ===================== 2) DADOS NEO =====================
st.header("2) Dados Neo (Volante Neo - Vinho)")
colN1, colN2, colN3 = st.columns(3)
with colN1:
    C19 = st.number_input("C19 Vazão (m³/h)", min_value=0.0, value=0.0, step=0.5, format="%.3f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)
with colN2:
    C20 = st.number_input("C20 %Ds (%)", min_value=0.0, value=0.0, step=0.1, format="%.3f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)
with colN3:
    C21 = st.number_input("C21 Conc. GL (%)", min_value=0.0, value=0.0, step=0.1, format="%.3f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)

st.divider()

# ===================== 3) DADOS DA MISTURA =====================
st.header("3) Dados da Mistura")

H5 = C19 + C6
H6 = ((C19*C20 + C6*C8) / H5) if H5 else 0.0
H7 = ((C19*C21 + C6*C9) / H5) if H5 else 0.0

H8 = st.number_input("H8 Consumo específico to be (kg/L)", min_value=0.0, value=1.65, step=0.01, format="%.3f")
st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)

H9  = H5*H7/96.0*H8
H10 = H9 - C11
H11 = H5*H7/96.0
H12 = H11*24.0
H13 = H11*1.2
H14 = H5 - H11*0.786 + H9 - H13
H15 = (H5*H6/H14) if H14 else 0.0
H16 = H14 - C15
H17 = (C4*C5/H14) if H14 else 0.0

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H5 Vazão Mistura</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H5)}</div><div>Fórmula = C19 + C6</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H6 %Ds Mistura</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H6,2)} %</div><div>Fórmula = (C19*C20 + C6*C8)/H5</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H7 Conc. w/w Mistura</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H7,2)} %</div><div>Fórmula = (C19*C21 + C6*C9)/H5</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H9 V1 total to be (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H9)}</div><div>Fórmula = H5*H7/96*H8</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H10 Diferença V1 (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H10)}</div><div>Fórmula = H9 − C11</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H11 Etanol hidratado (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H11)}</div><div>Fórmula = H5*H7/96</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H12 Etanol dia (m³/dia)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H12)}</div><div>Fórmula = H11*24</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H13 Flegmaça (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H13)}</div><div>Fórmula = H11*1.2</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H14 Vinhaça to be (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H14)}</div><div>Fórmula = H5 − H11*0.786 + H9 − H13</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="grid3">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H15 %Sólidos na vinhaça to be</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H15*100,2)} %</div><div>Fórmula = H5*H6/H14</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H16 Diferença de vinhaça (m³/h)</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H16)}</div><div>Fórmula = H14 − C15</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>∑ H17 K vinhaça</b> <span class='badge formula fx'>Fórmula</span><div style='font-size:1.25rem'>{fmt(H17)}</div><div>Fórmula = C4*C5/H14</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ===================== 4) PRODUÇÕES & FINANCEIRO =====================
st.header("4) Produções & Financeiro")

with st.expander("Parâmetros financeiros (Variar)"):
    preco_etanol = st.number_input("Preço etanol (R$/m³)", min_value=0.0, value=2800.0, step=50.0, format="%.2f")
    st.markdown("<span class='badge variar slider'>Variar</span>", unsafe_allow_html=True)

producao_as_is_m3dia = C13
producao_to_be_m3dia = H12
delta_producao = producao_to_be_m3dia - producao_as_is_m3dia

receita_as_is = producao_as_is_m3dia * preco_etanol
receita_to_be = producao_to_be_m3dia * preco_etanol
delta_receita  = receita_to_be - receita_as_is

st.markdown('<div class="grid2">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>Etanol (as is) — C13</b><div style='font-size:1.25rem'>{fmt(producao_as_is_m3dia)}</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>Etanol (to be) — H12</b><div style='font-size:1.25rem'>{fmt(producao_to_be_m3dia)}</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="grid2">', unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>Δ Produção (m³/dia)</b><div style='font-size:1.25rem'>{fmt(delta_producao)}</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><b>Δ Receita (R$/dia)</b><div style='font-size:1.25rem'>{fmt(delta_receita,2)}</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.caption("""Observações:
- Itens com <span class='badge fixo lock'>Fixo</span> não possuem entrada no app (só editáveis no código).
- Itens com <span class='badge variar slider'>Variar</span> são entradas ajustáveis.
- Itens com <span class='badge formula fx'>Fórmula</span> são calculados exatamente como na planilha (C7…C17; H5…H17).
- Este app NÃO depende de planilha nem de openpyxl. Todas as fórmulas estão implementadas em Python.
""", unsafe_allow_html=True)

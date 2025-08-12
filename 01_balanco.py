
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Perdas de Produção - Óleo, DDGS e Etanol", layout="wide")

st.title("PERDAS DE PRODUÇÃO ESTIMADA (sem custos/margens de vapor)")

with st.sidebar:
    st.header("Entradas - Operação")
    moagem_por_dia = st.number_input("Moagem enviada (t/dia)", min_value=0.0, value=35.0, step=1.0, format="%.3f")
    dias_bio = st.number_input("Dias em produção na Bio (dias)", min_value=0, value=25, step=1)

    st.header("Rendimentos (por tonelada de moagem)")
    rendimento_oleo_kgpt = st.number_input("Rendimento de óleo (kg/t)", min_value=0.0, value=19.0, step=0.1, format="%.2f")
    rendimento_ddgs_kgpt = st.number_input("Produção de DDGS (kg/t)", min_value=0.0, value=250.0, step=1.0, format="%.1f")

    st.header("Financeiro - Preços líquidos")
    preco_oleo_rpt = st.number_input("Preço líquido do óleo (R$/t)", min_value=0.0, value=5000.0, step=100.0, format="%.2f")
    preco_ddgs_rpt = st.number_input("Preço líquido do DDGS (R$/t)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")

    st.header("Produção de Etanol na Bio")
    modo_etanol = st.radio("Como quer informar o etanol?", ["Capacidade por dia × dias", "Total direto"], index=0)
    if modo_etanol == "Capacidade por dia × dias":
        etanol_por_dia = st.number_input("Produção de etanol (t/dia ou m3/dia)", min_value=0.0, value=463.546, step=1.0, format="%.3f")
        etanol_total = etanol_por_dia * dias_bio
    else:
        etanol_total = st.number_input("Produção total de etanol no período (t ou m3)", min_value=0.0, value=11588.666, step=1.0, format="%.3f")

    preco_etanol = st.number_input("Preço líquido do etanol (R$ por t ou m3)", min_value=0.0, value=2800.0, step=50.0, format="%.2f")

# Cálculos
moagem_total = moagem_por_dia * dias_bio  # t
oleo_perdido_t = (moagem_total * (rendimento_oleo_kgpt / 1000.0))  # t
ddgs_perdido_t = (moagem_total * (rendimento_ddgs_kgpt / 1000.0))  # t

valor_oleo_perdido = oleo_perdido_t * preco_oleo_rpt
valor_ddgs_perdido = ddgs_perdido_t * preco_ddgs_rpt
valor_etanol_produzido = etanol_total * preco_etanol

financeiro_total = -valor_oleo_perdido - valor_ddgs_perdido + valor_etanol_produzido

# Apresentação
col1, col2 = st.columns([1.1, 1.3])

with col1:
    st.subheader("Moagem")
    df_moagem = pd.DataFrame({
        "Item": ["Moagem (t) enviada", "Produção de óleo (kg/t)", "Produção de DDGS (kg/t)"],
        "Valor": [moagem_por_dia, rendimento_oleo_kgpt, rendimento_ddgs_kgpt],
        "Unidade": ["t/dia", "kg/t", "kg/t"]
    })
    st.table(df_moagem)

with col2:
    st.subheader("Financeiro")
    df_fin = pd.DataFrame({
        "Item": [
            "Dias em produção na Bio",
            "Perda de produção de óleo (t)",
            "Perda de produção de DDGS (t)",
            "Produção de etanol (t/m3)"
        ],
        "Quantidade": [
            dias_bio,
            round(oleo_perdido_t, 3),
            round(ddgs_perdido_t, 3),
            round(etanol_total, 3)
        ],
        "Preço Líquido (R$/unid.)": ["-", preco_oleo_rpt, preco_ddgs_rpt, preco_etanol],
        "Valor (R$)": [
            0.0,
            -valor_oleo_perdido,
            -valor_ddgs_perdido,
            valor_etanol_produzido
        ]
    })
    st.table(df_fin)

st.markdown("---")
st.subheader("TOTAL FINANCEIRO")
st.metric(label="Resultado líquido (R$)", value=f"{financeiro_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.caption(
    """Notas:
- Este app ignora custos/margens de vapor, como solicitado.
- Unidades de etanol (t ou m3) devem ser consistentes com o preço informado.
- Ajuste os preços líquidos conforme seus valores reais de venda."""
)

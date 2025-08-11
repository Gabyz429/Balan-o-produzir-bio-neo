
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Balanço - Vinhaça, Etanol e Financeiro", page_icon="📊", layout="wide")

st.title("📊 Balanço de Produção — Vinhaça, Etanol e Financeiro")

with st.sidebar:
    st.header("Entradas do processo")
    wine_flow_m3h = st.number_input("Vazão do vinho (m³/h)", min_value=0.0, value=100.0, step=1.0, help="Vazão enviada à destilaria")
    etoh_mass_pct = st.number_input("Etanol no vinho (w/w, %)", min_value=0.0, max_value=100.0, value=14.5, step=0.1)
    ds_wine_pct = st.number_input("Sólidos no vinho (w/w, %)", min_value=0.0, max_value=40.0, value=8.5, step=0.1)
    rho_wine_t_m3 = st.number_input("Densidade do vinho (t/m³)", min_value=0.5, max_value=1.2, value=1.00, step=0.01)

    st.divider()
    st.header("Produto e vapor")
    product_type = st.selectbox("Especificação do etanol produzido", ["Hidratado 92,6 °INPM", "Anidro (100%)"])
    rho_hydrated_t_m3 = st.number_input("Densidade etanol hidratado (t/m³)", min_value=0.75, max_value=0.90, value=0.806, step=0.001, help="Use a densidade do seu laboratório a 20 °C")
    rho_anhydrous_t_m3 = st.number_input("Densidade etanol anidro (t/m³)", min_value=0.75, max_value=0.90, value=0.789, step=0.001)
    vapor_basis = st.selectbox("Base do consumo de vapor (kg por litro de...)", ["etanol hidratado (produto)", "etanol absoluto (LAA)"])
    vapor_kg_per_L = st.number_input("Consumo de vapor (kg/L)", min_value=0.0, value=1.65, step=0.05)

    st.divider()
    st.header("Financeiro")
    days = st.number_input("Dias de operação (d)", min_value=0, value=25, step=1)
    hours_per_day = st.number_input("Horas por dia (h/d)", min_value=1, max_value=24, value=24, step=1)
    price_ethanol_R_per_m3 = st.number_input("Preço do etanol (R$/m³)", min_value=0.0, value=2800.0, step=50.0, help="Digite o preço de venda do etanol")
    cost_steam_R_per_t = st.number_input("Custo de vapor (R$/t)", min_value=0.0, value=90.0, step=5.0)
    vinasse_density_t_m3 = st.number_input("Densidade da vinhaça (t/m³)", min_value=0.8, max_value=1.2, value=1.00, step=0.01)

# ---- Cálculos ----
wine_mass_tph = wine_flow_m3h * rho_wine_t_m3
etoh_mass_tph = wine_mass_tph * (etoh_mass_pct/100.0)
ds_mass_tph = wine_mass_tph * (ds_wine_pct/100.0)

if product_type.startswith("Hidratado"):
    product_mass_tph = etoh_mass_tph / 0.926  # 92,6 INPM
    rho_prod = rho_hydrated_t_m3
else:
    product_mass_tph = etoh_mass_tph
    rho_prod = rho_anhydrous_t_m3

product_vol_m3h = product_mass_tph / rho_prod
laa_vol_m3h = etoh_mass_tph / rho_anhydrous_t_m3  # LAA volume (absolute alcohol)

if vapor_basis.startswith("etanol hidratado"):
    vapor_tph = vapor_kg_per_L * (product_vol_m3h * 1000.0) / 1000.0  # kg/L * L/h -> kg/h -> t/h
else:
    vapor_tph = vapor_kg_per_L * (laa_vol_m3h * 1000.0) / 1000.0

vinasse_mass_tph = wine_mass_tph - product_mass_tph + vapor_tph
vinasse_vol_m3h = vinasse_mass_tph / vinasse_density_t_m3
vinasse_ds_pct = (ds_mass_tph / vinasse_mass_tph * 100.0) if vinasse_mass_tph > 0 else float("nan")

# Financeiro
hours_total = days * hours_per_day
ethanol_total_m3 = product_vol_m3h * hours_total
vapor_total_t = vapor_tph * hours_total
revenue_R = ethanol_total_m3 * price_ethanol_R_per_m3
cost_steam_R = vapor_total_t * cost_steam_R_per_t
gross_margin_R = revenue_R - cost_steam_R

# ---- Saídas ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Etanol (m³/h)", f"{product_vol_m3h:.2f}")
c2.metric("Vinhaça (m³/h)", f"{vinasse_vol_m3h:.2f}")
c3.metric("Vinhaça %DS", f"{vinasse_ds_pct:.2f}%")
c4.metric("Vapor (t/h)", f"{vapor_tph:.2f}")

st.divider()
st.subheader("Financeiro estimado")
f1, f2, f3, f4 = st.columns(4)
f1.metric("Receita de etanol (R$)", f"{revenue_R:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
f2.metric("Custo de vapor (R$)", f"{cost_steam_R:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
f3.metric("Margem bruta (R$)", f"{gross_margin_R:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
f4.metric("Horizonte (h)", f"{hours_total}")

st.subheader("Detalhamento")
df = pd.DataFrame({
    "Variável": [
        "Vazão do vinho (m³/h)", "Massa do vinho (t/h)", "Etanol no vinho (t/h)", "DS do vinho (t/h)",
        "Produto etanol (t/h)", "Produto etanol (m³/h)",
        "Vapor (t/h)", "Vinhaça (t/h)", "Vinhaça (m³/h)", "%DS na vinhaça"
    ],
    "Valor": [
        wine_flow_m3h, wine_mass_tph, etoh_mass_tph, ds_mass_tph,
        product_mass_tph, product_vol_m3h,
        vapor_tph, vinasse_mass_tph, vinasse_vol_m3h, vinasse_ds_pct
    ]
})
st.dataframe(df, use_container_width=True)

with st.expander("Assunções"):
    st.markdown(
        ''' 
- Conversão GL→m/m não é feita aqui; informe diretamente o **% (m/m)** de etanol no vinho.
- Densidade do vinho assumida como 1,00 t/m³ (ajuste se tiver medição).
- Etanol hidratado **92,6 °INPM**: massa do produto = massa de etanol/0,926.
- O vapor consumido é somado à vinhaça (condensado/arraste).
- A parte financeira considera **apenas** receita de etanol e custo de vapor (coloque seus preços reais).
        '''
    )

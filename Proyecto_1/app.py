import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Retail & RFM Analytics", layout="wide")

st.title("📊 Dashboard de Ventas & Segmentación RFM")
st.markdown("Análisis exploratorio y comportamiento de clientes para e-commerce.")

# Cargar datos
@st.cache_data
def load_data():
    df_sales = pd.read_csv('online_retail_clean.csv')
    df_rfm = pd.read_csv('rfm_segmentation.csv')
    return df_sales, df_rfm

sales, rfm = load_data()

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingresos Totales", f"${sales['TotalSales'].sum():,.2f}")
col2.metric("Total Ordenes", f"{sales['InvoiceNo'].nunique():,}")
col3.metric("Total Clientes", f"{rfm['CustomerID'].nunique():,}")
col4.metric("Ticket Promedio", f"${sales['TotalSales'].sum() / sales['InvoiceNo'].nunique():,.2f}")

st.divider()

# --- GRÁFICOS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Clientes por Segmento RFM")
    fig_rfm = px.bar(
        rfm['Segmento'].value_counts().reset_index(),
        x='Segmento',
        y='count',
        color='Segmento',
        labels={'count': 'Número de Clientes', 'Segmento': 'Segmento'},
        template="plotly_dark"
    )
    st.plotly_chart(fig_rfm, width='stretch')

with c2:
    st.subheader("Top 5 Países por Facturación")
    top_countries = sales.groupby('Country')['TotalSales'].sum().nlargest(5).reset_index()
    fig_country = px.pie(
        top_countries,
        values='TotalSales',
        names='Country',
        hole=0.4,
        template="plotly_dark"
    )
    st.plotly_chart(fig_country, width='stretch')
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

# 1. Configuración de la página
st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="🔮",
    layout="wide"
)


# Cargar Modelo de Machine Learning
@st.cache_resource
def load_ml_model():
    try:
        return joblib.load('modelo_churn.pkl')
    except Exception:
        return None


model_churn = load_ml_model()

# Título Principal
st.title("🛡️ Customer Retention & Churn Prediction System")
st.markdown("Plataforma analítica para predecir fuga de clientes y optimizar estrategias de retención.")

st.divider()

# Si el modelo no se encuentra, mostrar advertencia
if model_churn is None:
    st.error(
        "⚠️ No se encontró el archivo 'modelo_churn.pkl'. Por favor ejecuta primero 'churn_model.py' para entrenar y guardar el modelo.")
    st.stop()

# 2. SECCIÓN PRINCIPAL: SIMULADOR PREDICTIVO
st.subheader("🎯 Simulador de Riesgo Individual")
st.caption(
    "Ajusta los parámetros del cliente para obtener un diagnóstico en tiempo real mediante el modelo HistGradientBoosting.")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("#### 📋 Información del Cliente")
    antiguedad = st.slider("Antigüedad (Meses)", min_value=1, max_value=72, value=12)
    gasto_mensual = st.number_input("Gasto Mensual ($USD)", min_value=20.0, max_value=200.0, value=65.0, step=5.0)
    tickets = st.slider("Tickets a Soporte Técnico", min_value=0, max_value=10, value=4)
    contrato = st.selectbox("Modalidad de Contrato", ["Mes a Mes", "Anual"])

    # Variables calculadas
    gasto_total = antiguedad * gasto_mensual
    contrato_val = 1 if contrato == "Anual" else 0
    tickets_por_mes = tickets / (antiguedad + 1)
    ticket_promedio = gasto_total / (antiguedad + 1)

with col_right:
    st.markdown("#### 📊 Resultado de la Evaluación")

    # Formatear datos de entrada
    input_df = pd.DataFrame([{
        'Antiguedad_Meses': antiguedad,
        'Gasto_Mensual': gasto_mensual,
        'Gasto_Total': gasto_total,
        'Soporte_Tecnico_Tickets': tickets,
        'Contrato_Anual': contrato_val,
        'Tickets_Por_Mes': tickets_por_mes,
        'Ticket_Promedio': ticket_promedio
    }])

    # Predecir probabilidad
    prob_churn = model_churn.predict_proba(input_df)[0][1]

    # Visualización gráfica de la probabilidad
    fig_gauge = px.pie(
        names=["Riesgo Churn", "Retención"],
        values=[prob_churn, 1 - prob_churn],
        hole=0.7,
        color_discrete_sequence=["#EF553B" if prob_churn >= 0.45 else "#00CC96", "#2A2D39"],
    )
    fig_gauge.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=200,
        annotations=[dict(text=f"{prob_churn * 100:.1f}%", x=0.5, y=0.5, font_size=32, showarrow=False)]
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Diagnóstico y Recomendación de Negocio
    if prob_churn >= 0.45:
        st.error("🚨 **DIAGNÓSTICO: ALTO RIESGO DE FUGA**")
        st.markdown("""
        **Acciones Recomendadas:**
        * 📞 Asignar ejecutivo de cuenta prioritario en las próximas 24h.
        * 🏷️ Ofrecer un **15% de descuento** por paso a Contrato Anual.
        * 🔧 Revisar el historial de tickets de soporte técnico pendientes.
        """)
    else:
        st.success("✅ **DIAGNÓSTICO: CLIENTE SALUDABLE**")
        st.markdown("""
        **Acciones Recomendadas:**
        * 🚀 Evaluar cliente para campañas de **Cross-selling / Upselling**.
        * ⭐ Incluir en el programa de lealtad y beneficios exclusivos.
        """)

st.divider()

# 3. SECCIÓN SECUNDARIA: ANALÍTICA DE ATRIBUTOS
st.subheader("💡 Métricas Clave de Decisión")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Gasto Total Estimado", f"${gasto_total:,.2f}")
m2.metric("Intensidad Soporte", f"{tickets_por_mes:.2f} t/mes")
m3.metric("Ticket Promedio", f"${ticket_promedio:,.2f}")
m4.metric("Umbral de Decisión", "45.0%")
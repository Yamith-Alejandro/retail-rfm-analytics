# 📊 Retail Data Analytics & Customer Segmentation (RFM)

## 📌 Descripción del Proyecto
Este proyecto analiza más de 500,000 transacciones de un e-commerce para identificar patrones de compra, limpiar anomalías de datos y segmentar a la base de clientes mediante la metodología **RFM (Recency, Frequency, Monetary)**.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python (Pandas, NumPy, Plotly, Streamlit)
* **Base de Datos & SQL:** PostgreSQL (Consultas analíticas, Window Functions, CTEs)
* **IDE & Herramientas:** PyCharm, DBeaver

## 🧹 Proceso de ETL y Limpieza
1. Eliminación de registros sin `CustomerID` (~135k filas).
2. Filtrado de transacciones con precios o cantidades $\le 0$ (devoluciones y errores).
3. Eliminación de duplicados exactos.
4. Dataset final conservado: **392,692 registros de calidad**.

## 📈 Resultados Clave (Segmentación RFM)
* **VIP / Champions:** 1,267 clientes.
* **Perdidos / Inactivos:** 300 clientes.

## 🚀 Cómo Ejecutar el Proyecto

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Yamith-Alejandro/retail-rfm-analytics.git](https://github.com/Yamith-Alejandro/retail-rfm-analytics.git)
import pandas as pd
import numpy as np

df = pd.read_csv('online_retail.csv', encoding='unicode_escape')

print("Dimensions of dataset:", df.shape)
print("\nInformación del DataFrame:")
print(df.info())
print("\nPrimeras filas:")
print(df.head())

print("---Nulos por Columnas---")
print(df.isnull().sum())

print("\n---Registros con cantidad Nula en precios---")
print("Cantidades <=0",(df['Quantity']<=0).sum())
print("Precios <=0",(df['UnitPrice']>0).sum())

print("\n---Registros Duplicados ---")
print("Duplicados Exactos,",df.duplicated().sum())

# A. Eliminar filas sin ID de cliente (imprescindible para segmentación/retención)
df_clean = df.dropna(subset=['CustomerID']).copy()

# B. Asegurar que CustomerID sea tipo entero (no float)
df_clean['CustomerID'] = df_clean['CustomerID'].astype(int)

# C. Filtrar devoluciones y precios inválidos (solo ventas reales)
df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]

# D. Eliminar duplicados
df_clean = df_clean.drop_duplicates()

# E. Corregir formato de fecha y crear variables derivadas de negocio
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
df_clean['TotalSales'] = df_clean['Quantity'] * df_clean['UnitPrice']
df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')

print("\n--- RESUMEN FINAL ---")
print(f"Registros originales: {len(df)}")
print(f"Registros limpios: {len(df_clean)}")
print(f"Porcentaje conservado: {(len(df_clean)/len(df))*100:.2f}%")
print("\nPrimeras filas del dataset limpio:")
print(df_clean.head())

# -------------------------------------------------------------------
# PASO 2: CÁLCULO DE MÉTRICAS RFM
# -------------------------------------------------------------------

# 1. Fijar una fecha de referencia para calcular la 'Recency'
# Usamos el día posterior a la última transacción registrada en los datos
snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)

# 2. Agrupar por CustomerID y calcular métricas
rfm = df_clean.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency (Días)
    'InvoiceNo': 'nunique',                                   # Frequency (Órdenes únicas)
    'TotalSales': 'sum'                                      # Monetary (Gasto total)
}).reset_index()

# Renombrar columnas
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print("--- RESUMEN DE MÉTRICAS RFM ---")
print(rfm.describe())
print("\nPrimeros 5 clientes:")
print(rfm.head())



# Asignar puntuaciones del 1 al 4 (4 es la mejor calificación)

# En Recency, menos días es MEJOR, por eso los labels van invertidos [4, 3, 2, 1]
rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])

# En Frequency y Monetary, más es MEJOR, labels [1, 2, 3, 4]
# Usamos rank(method='first') para evitar errores con valores duplicados
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=4, labels=[1, 2, 3, 4])

# Combinar puntuaciones en una columna
rfm['RFM_Group'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

# Categorización por Segmentos de Negocio
def segmentar_cliente(df):
    if df['RFM_Score'] >= 10:
        return 'VIP / Champions'
    elif (df['RFM_Score'] >= 8) and (df['RFM_Score'] < 10):
        return 'Clientes Leales'
    elif (df['RFM_Score'] >= 6) and (df['RFM_Score'] < 8):
        return 'Prometedores / Potenciales'
    elif (df['RFM_Score'] >= 4) and (df['RFM_Score'] < 6):
        return 'En Riesgo / Inactivos'
    else:
        return 'Perdidos'

rfm['Segmento'] = rfm.apply(segmentar_cliente, axis=1)

print("\n--- DISTRIBUCIÓN DE CLIENTES POR SEGMENTO ---")
print(rfm['Segmento'].value_counts())

# -------------------------------------------------------------------
# PASO 3: EXPORTACIÓN PARA SQL Y POWER BI
# -------------------------------------------------------------------

# 1. Exportar transacciones limpias
df_clean.to_csv('online_retail_clean.csv', index=False)

# 2. Exportar resultados RFM
rfm.to_csv('rfm_segmentation.csv', index=False)

print("\n¡Archivos exportados exitosamente!")
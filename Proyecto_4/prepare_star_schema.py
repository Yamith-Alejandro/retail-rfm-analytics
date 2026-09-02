import pandas as pd
import os

print("🔄 Procesando dataset de Olist...")

# 1. Cargar datasets
orders = pd.read_csv("olist_orders_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")
translations = pd.read_csv("product_category_name_translation.csv")

# 2. Traducir categorías de productos al inglés
products = products.merge(translations, on="product_category_name", how="left")
products['product_category_name_english'] = products['product_category_name_english'].fillna('other')
products = products.drop(columns=['product_category_name'])

# 3. Construir la Tabla de Hechos (Fact_Ventas)
fact_ventas = order_items.merge(orders, on="order_id", how="inner")
fact_ventas = fact_ventas.merge(payments, on="order_id", how="left")

# Seleccionar columnas clave para la Fact Table
fact_ventas = fact_ventas[[
    'order_id',
    'customer_id',
    'product_id',
    'seller_id',
    'order_purchase_timestamp',
    'price',
    'freight_value',
    'payment_value',
    'payment_type'
]]

# Limpiar valores nulos en fecha y convertir a datetime
fact_ventas['order_purchase_timestamp'] = pd.to_datetime(fact_ventas['order_purchase_timestamp'])

# 4. Crear carpeta 'data_processed' si no existe
os.makedirs("data_processed", exist_ok=True)

# 5. Exportar tablas optimizadas para Power BI con codificación UTF-8 BOM
fact_ventas.to_csv("data_processed/Fact_Ventas.csv", index=False, encoding='utf-8-sig')
customers.to_csv("data_processed/Dim_Clientes.csv", index=False, encoding='utf-8-sig')
products.to_csv("data_processed/Dim_Productos.csv", index=False, encoding='utf-8-sig')
sellers.to_csv("data_processed/Dim_Vendedores.csv", index=False, encoding='utf-8-sig')

print("✅ Archivos procesados con éxito en la carpeta 'data_processed/':")
print("   - Fact_Ventas.csv")
print("   - Dim_Clientes.csv")
print("   - Dim_Productos.csv")
print("   - Dim_Vendedores.csv")
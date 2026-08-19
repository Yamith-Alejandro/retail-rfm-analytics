# 🛡️ Customer Churn Prediction & Retention Analytics

Este proyecto implementa una solución end-to-end de **Ciencia de Datos y Machine Learning Aplicado al Negocio** para predecir la probabilidad de cancelación (*Churn*) de clientes e identificar factores clave de insatisfacción.

## 🎯 Problema de Negocio
Retener a un cliente existente es entre 5 y 25 veces más económico que adquirir uno nuevo. La plataforma analiza el comportamiento transaccional e interacciones con soporte técnico para alertar de forma temprana sobre clientes en alto riesgo de abandono, permitiendo al equipo de retención aplicar estrategias proactivas.

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Machine Learning & Preprocesamiento:** `scikit-learn`, `imbalanced-learn` (SMOTE)
* **Algoritmo Seleccionado:** `HistGradientBoostingClassifier` con ajuste de hiperparámetros (`GridSearchCV`)
* **Dashboard Interactivo:** `Streamlit`, `Plotly`
* **Persistencia del Modelo:** `joblib`

---

## 📊 Métricas de Evaluación del Modelo
* **ROC-AUC Score:** ~0.84+
* **Precision (Clase Churn):** 85%
* **Recall (Clase Churn):** 80%
* **F1-Score (Clase Churn):** 0.83

---

## 🚀 Cómo Ejecutar Localmente

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/customer-churn-prediction.git](https://github.com/TU_USUARIO/customer-churn-prediction.git)
   cd customer-churn-prediction
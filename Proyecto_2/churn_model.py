import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib

# 1. Simulación de Dataset con Señal Fuerte
print("🔄 Cargando datos y aplicando Feature Engineering...")
np.random.seed(42)
n_samples = 1500

antiguedad = np.random.randint(1, 72, n_samples)
gasto_mensual = np.random.uniform(20, 120, n_samples)
gasto_total = antiguedad * gasto_mensual + np.random.normal(0, 30, n_samples)
tickets = np.random.randint(0, 10, n_samples)
contrato_anual = np.random.choice([0, 1], size=n_samples, p=[0.6, 0.4])

# Scoring de riesgo con patrones definidos
score = (
    (tickets * 0.6) +
    ((72 - antiguedad) * 0.04) +
    ((1 - contrato_anual) * 2.2) -
    (gasto_mensual * 0.015)
)
prob_churn = 1 / (1 + np.exp(-(score - 3.0)))
churn = (np.random.rand(n_samples) < prob_churn).astype(int)

df = pd.DataFrame({
    'Antiguedad_Meses': antiguedad,
    'Gasto_Mensual': gasto_mensual,
    'Gasto_Total': gasto_total,
    'Soporte_Tecnico_Tickets': tickets,
    'Contrato_Anual': contrato_anual,
    'Churn': churn
})

# 2. FEATURE ENGINEERING (Variables Compuestas)
df['Tickets_Por_Mes'] = df['Soporte_Tecnico_Tickets'] / (df['Antiguedad_Meses'] + 1)
df['Ticket_Promedio'] = df['Gasto_Total'] / (df['Antiguedad_Meses'] + 1)

# 3. Separar Predictoras y Target
X = df.drop('Churn', axis=1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Balanceo con SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# 4. MODELO GRADIENT BOOSTING + TUNING
print("🤖 Entrenando HistGradientBoosting con GridSearchCV...")
base_model = HistGradientBoostingClassifier(random_state=42)

param_grid = {
    'learning_rate': [0.03, 0.1],
    'max_iter': [100, 150],
    'max_depth': [3, 5],
    'l2_regularization': [0.0, 1.0]
}

grid_search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    scoring='roc_auc',
    cv=5,
    n_jobs=-1
)

grid_search.fit(X_train_res, y_train_res)
best_model = grid_search.best_estimator_

# 5. EVALUACIÓN Y THRESHOLD TUNING
y_proba = best_model.predict_proba(X_test)[:, 1]

# Ajuste fino del umbral
opt_threshold = 0.45
y_pred_opt = (y_proba >= opt_threshold).astype(int)

print(f"\n✨ Mejores Parámetros: {grid_search.best_params_}")
print("\n--- 📊 REPORTE OPTIMIZADO ---")
print(classification_report(y_test, y_pred_opt))
print(f"🚀 Área Bajo la Curva ROC (ROC-AUC Score): {roc_auc_score(y_test, y_proba):.4f}")



# Guardar el modelo entrenado y la lista de columnas
joblib.dump(best_model, 'modelo_churn.pkl')
print("\n💾 ¡Modelo guardado exitosamente como 'modelo_churn.pkl'!")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API REST para predecir la probabilidad de abandono de clientes en tiempo real.",
    version="1.0.0"
)

# Cargar el modelo entrenado
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/churn_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None


# Esquema de validación del cliente
class CustomerData(BaseModel):
    antiguedad_meses: int = Field(..., ge=0, description="Meses de permanencia del cliente")
    soporte_tecnico_tickets: int = Field(..., ge=0, description="Número de tickets abiertos")
    gasto_mensual: float = Field(..., gt=0, description="Monto mensual facturado en USD")
    contrato_anual: int = Field(..., ge=0, le=1, description="1 si tiene contrato anual, 0 si no")

    class Config:
        json_schema_extra = {
            "example": {
                "antiguedad_meses": 6,
                "soporte_tecnico_tickets": 5,
                "gasto_mensual": 69.5,
                "contrato_anual": 0
            }
        }


@app.get("/health", tags=["Health Check"])
def health_check():
    """Verifica si la API y el modelo están cargados correctamente."""
    if model is None:
        raise HTTPException(status_code=503, detail="El modelo no se encuentra cargado.")
    return {"status": "ok", "model_loaded": True}


@app.post("/predict", tags=["ML Inference"])
def predict_churn(customer: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible.")

    antiguedad_valida = max(customer.antiguedad_meses, 1)

    # 1. Crear el diccionario con todas las variables calculadas
    data_dict = {
        "Antiguedad_Meses": customer.antiguedad_meses,
        "Soporte_Tecnico_Tickets": customer.soporte_tecnico_tickets,
        "Gasto_Mensual": customer.gasto_mensual,
        "Gasto_Total": customer.gasto_mensual * customer.antiguedad_meses,
        "Contrato_Anual": customer.contrato_anual,
        "Ticket_Promedio": customer.gasto_mensual,
        "Tickets_Por_Mes": customer.soporte_tecnico_tickets / antiguedad_valida
    }

    data_df = pd.DataFrame([data_dict])

    # 2. Reordenar automáticamente las columnas según lo que espera el modelo
    if hasattr(model, "feature_names_in_"):
        data_df = data_df[list(model.feature_names_in_)]

    # 3. Predicción
    prediction = int(model.predict(data_df)[0])
    probability = float(model.predict_proba(data_df)[0][1])

    if probability >= 0.70:
        risk_level = "CRÍTICO"
    elif probability >= 0.40:
        risk_level = "MODERADO"
    else:
        risk_level = "BAJO"

    return {
        "churn_prediction": prediction,
        "churn_probability": round(probability, 4),
        "risk_level": risk_level
    }
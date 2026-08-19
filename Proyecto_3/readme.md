🚀 Proyecto 3: Microservicio REST y Despliegue de Machine Learning con FastAPI & Docker

Dimos el siguiente paso en la arquitectura de datos: llevar el modelo de predicción de abandono de clientes (Customer Churn) a un entorno de producción contenerizado.

🏗️ Arquitectura e Implementación:

    FastAPI: Desarrollo de un microservicio asíncrono para inferencia en tiempo real con validación estricta de esquemas mediante Pydantic.

    ML Inference Pipeline: Integración del modelo predictivo con cálculo dinámico de variables derivadas en tiempo de ejecución.

    Docker: Empaquetado completo de la aplicación, dependencias y runtime en una imagen ultra ligera (python:3.11-slim) para garantizar portabilidad y aislamiento.

⚡ Resultados:

    Endpoints desplegados: /health para monitorización de estado y /predict para consumo HTTP POST.

    Petición en producción: Respuesta en tiempo real con predicción binaria, probabilidad estimada (p. ej., 0.999) y clasificación automática del nivel de riesgo (CRÍTICO, MODERADO, BAJO).

🛠️ Tech Stack: Python | FastAPI | Docker | Scikit-Learn | Pydantic | Linux / Bash | Git

🔗 Repositorio del proyecto y Dockerfile en GitHub: [https://github.com/Yamith-Alejandro/retail-rfm-analytics.git]

#MLOps #FastAPI #Docker #MachineLearning #DataScience #Python #SoftwareEngineering #CloudComputing
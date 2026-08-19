-- Resumen General de Métricas de Churn
SELECT
    COUNT(*) AS total_clientes,
    SUM(churn) AS clientes_churn,
    ROUND(AVG(churn) * 100, 2) AS tasa_churn_porcentaje,
    ROUND(AVG(gasto_mensual), 2) AS ticket_promedio
FROM "db_churn_analytics"."customers";
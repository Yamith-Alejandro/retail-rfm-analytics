-- Segmentación de Churn por Antigüedad del Cliente
SELECT
    CASE
        WHEN antiguedad_meses <= 12 THEN '0-1 Año'
        WHEN antiguedad_meses <= 36 THEN '1-3 Años'
        ELSE 'Más de 3 Años'
    END AS segmento_antiguedad,
    ROUND(AVG(soporte_tecnico_tickets), 2) AS promedio_tickets,
    COUNT(*) AS total_clientes,
    SUM(churn) AS total_churn,
    ROUND(AVG(churn) * 100, 2) AS pct_churn
FROM "db_churn_analytics"."customers"
GROUP BY
    CASE
        WHEN antiguedad_meses <= 12 THEN '0-1 Año'
        WHEN antiguedad_meses <= 36 THEN '1-3 Años'
        ELSE 'Más de 3 Años'
    END
ORDER BY pct_churn DESC;
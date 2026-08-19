-- Análisis de Fricción: Tipo de Contrato vs Tickets de Soporte
SELECT
    CASE WHEN contrato_anual = 1 THEN 'Contrato Anual' ELSE 'Sin Contrato' END AS tipo_contrato,
    CASE
        WHEN soporte_tecnico_tickets >= 5 THEN 'Alto Soporte (>=5)'
        ELSE 'Bajo Soporte (<5)'
    END AS nivel_soporte,
    COUNT(*) AS total_clientes,
    SUM(churn) AS clientes_churn,
    ROUND(AVG(churn) * 100, 2) AS pct_churn,
    ROUND(AVG(gasto_mensual), 2) AS gasto_promedio
FROM "db_churn_analytics"."customers"
GROUP BY
    contrato_anual,
    CASE
        WHEN soporte_tecnico_tickets >= 5 THEN 'Alto Soporte (>=5)'
        ELSE 'Bajo Soporte (<5)'
    END
ORDER BY pct_churn DESC;
WITH quarterly_revenue AS (
    SELECT
        service_type,
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(QUARTER FROM pickup_datetime) AS quarter,
        CONCAT(CAST(EXTRACT(YEAR FROM pickup_datetime) AS STRING), '/Q', 
               CAST(EXTRACT(QUARTER FROM pickup_datetime) AS STRING)) AS year_quarter,
        SUM(total_amount) AS revenue
    FROM `terraform-demo-448809.dbt_y0ussefelbrini.fact_trips`
    WHERE EXTRACT(YEAR FROM pickup_datetime) BETWEEN 2000 AND 2025  -- FIX
    GROUP BY 1, 2, 3, 4
),
yoy_growth AS (
    SELECT
        q1.service_type,
        q1.year_quarter,
        q1.revenue AS current_revenue,
        q2.revenue AS previous_revenue,
        ROUND(100 * (q1.revenue - q2.revenue) / NULLIF(q2.revenue, 0), 2) AS yoy_growth
    FROM quarterly_revenue q1
    LEFT JOIN quarterly_revenue q2
    ON q1.service_type = q2.service_type
    AND q1.year = q2.year + 1
    AND q1.quarter = q2.quarter
)
SELECT * FROM yoy_growth
ORDER BY service_type, yoy_growth DESC;

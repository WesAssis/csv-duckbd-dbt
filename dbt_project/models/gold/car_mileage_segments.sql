-- models/gold/car_mileage_segments.sql

SELECT
    car_id,
    manufacturer,
    model,
    year_of_manufacture,
    mileage,
    price_eur,
    CASE
        WHEN mileage <= 40000 THEN 'Baixa KM'
        WHEN mileage > 40000 AND mileage <= 100000 THEN 'Média KM'
        ELSE 'Alta KM'
    END AS mileage_segment
FROM
    {{ ref('stg_cars') }}
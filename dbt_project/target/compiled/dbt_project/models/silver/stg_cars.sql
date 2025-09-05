-- models/silver/stg_cars.sql

WITH source AS (
    SELECT * FROM "database"."bronze"."raw_cars"
)

SELECT
    -- Usando md5 + hex() para gerar string estável como ID
    hex(md5(Model || "Year of manufacture" || Mileage)) AS car_id,

    -- Renomeando e padronizando colunas
    "Manufacturer" AS manufacturer,
    "Model" AS model,
    "Fuel type" AS fuel_type,

    -- Conversão de tipos no padrão DuckDB
    CAST("Engine size" AS DOUBLE) AS engine_size_liters,
    CAST("Year of manufacture" AS INTEGER) AS year_of_manufacture,
    CAST(Mileage AS BIGINT) AS mileage,
    CAST(Price AS DECIMAL(18,2)) AS price_eur,

    -- Calculando idade do carro
    EXTRACT(YEAR FROM CURRENT_DATE) - CAST("Year of manufacture" AS INTEGER) AS car_age_years

FROM source
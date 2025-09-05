-- models/silver/stg_cars.sql

WITH source AS (
    SELECT * FROM "database"."bronze"."raw_cars"
),

-- Esta etapa usa ROW_NUMBER para numerar linhas que são completamente idênticas,
-- garantindo um desempate para a criação da chave primária.
source_ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY
                "Manufacturer",
                "Model",
                "Year of manufacture",
                "Mileage",
                "Fuel type",
                "Engine size",
                "Price"
            ORDER BY
                (SELECT NULL) -- A ordem não é relevante, apenas o número sequencial.
        ) as duplicate_rank
    FROM source
)

SELECT
    -- A chave primária agora inclui o 'duplicate_rank' para garantir 100% de unicidade.
    hex(md5(
        "Manufacturer" || '-' ||
        "Model" || '-' ||
        "Year of manufacture" || '-' ||
        "Mileage" || '-' ||
        "Fuel type" || '-' ||
        "Engine size" || '-' ||
        "Price" || '-' ||
        duplicate_rank
    )) AS car_id,

    -- Renomeação e conversão de tipos das colunas
    "Manufacturer" AS manufacturer,
    "Model" AS model,
    "Fuel type" AS fuel_type,
    CAST("Engine size" AS DOUBLE) AS engine_size_liters,
    CAST("Year of manufacture" AS INTEGER) AS year_of_manufacture,
    CAST(Mileage AS BIGINT) AS mileage,
    CAST(Price AS DECIMAL(18,2)) AS price_eur,

    -- Cálculo da idade do veículo
    EXTRACT(YEAR FROM CURRENT_DATE) - CAST("Year of manufacture" AS INTEGER) AS car_age_years

FROM source_ranked
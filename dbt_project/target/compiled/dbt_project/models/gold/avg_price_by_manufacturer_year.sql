-- models/gold/avg_price_by_manufacturer_year.sql

SELECT
    manufacturer,
    year_of_manufacture,
    COUNT(car_id) AS total_cars,
    ROUND(AVG(price_eur), 2) AS average_price_eur
FROM
    "database"."main"."stg_cars"
GROUP BY
    manufacturer,
    year_of_manufacture
ORDER BY
    manufacturer,
    year_of_manufacture DESC
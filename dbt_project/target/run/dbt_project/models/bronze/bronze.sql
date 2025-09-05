
  
  create view "database"."main"."bronze__dbt_tmp" as (
    SELECT
  *,
  'teste' AS teste
FROM input
  );

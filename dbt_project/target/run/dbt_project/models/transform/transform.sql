
  
    
    

    create  table
      "database"."main"."transform__dbt_tmp"
  
    as (
      SELECT
  *,
  'teste' AS teste
FROM input
    );
  
  

    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select manufacturer
from "database"."main"."stg_cars"
where manufacturer is null



  
  
      
    ) dbt_internal_test
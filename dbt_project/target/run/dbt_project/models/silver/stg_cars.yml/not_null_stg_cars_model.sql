
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select model
from "database"."main"."stg_cars"
where model is null



  
  
      
    ) dbt_internal_test
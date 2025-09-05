
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select average_price_eur
from "database"."main"."avg_price_by_manufacturer_year"
where average_price_eur is null



  
  
      
    ) dbt_internal_test
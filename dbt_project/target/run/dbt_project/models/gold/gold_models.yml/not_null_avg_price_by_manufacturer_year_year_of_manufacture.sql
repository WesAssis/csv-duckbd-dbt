
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select year_of_manufacture
from "database"."main"."avg_price_by_manufacturer_year"
where year_of_manufacture is null



  
  
      
    ) dbt_internal_test

    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select mileage_segment
from "database"."main"."car_mileage_segments"
where mileage_segment is null



  
  
      
    ) dbt_internal_test
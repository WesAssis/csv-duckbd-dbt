
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    car_id as unique_field,
    count(*) as n_records

from "database"."main"."car_mileage_segments"
where car_id is not null
group by car_id
having count(*) > 1



  
  
      
    ) dbt_internal_test
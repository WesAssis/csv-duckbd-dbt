
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        mileage_segment as value_field,
        count(*) as n_records

    from "database"."main"."car_mileage_segments"
    group by mileage_segment

)

select *
from all_values
where value_field not in (
    'Baixa KM','Média KM','Alta KM'
)



  
  
      
    ) dbt_internal_test
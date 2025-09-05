






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and car_age_years >= 0 and car_age_years <= 100
)
 as expression


    from "database"."main"."stg_cars"
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors








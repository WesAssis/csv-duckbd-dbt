






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and price_eur >= 0
)
 as expression


    from "database"."main"."stg_cars"
    where
        price_eur >= 0
    
    

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








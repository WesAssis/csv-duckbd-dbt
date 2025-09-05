
    
    

with all_values as (

    select
        fuel_type as value_field,
        count(*) as n_records

    from "database"."main"."stg_cars"
    group by fuel_type

)

select *
from all_values
where value_field not in (
    'Petrol','Diesel','Hybrid'
)



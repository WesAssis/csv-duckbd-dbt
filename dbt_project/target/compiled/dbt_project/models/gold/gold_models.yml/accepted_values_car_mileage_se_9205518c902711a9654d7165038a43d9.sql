
    
    

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



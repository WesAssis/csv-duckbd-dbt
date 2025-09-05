
    
    

select
    car_id as unique_field,
    count(*) as n_records

from "database"."main"."stg_cars"
where car_id is not null
group by car_id
having count(*) > 1



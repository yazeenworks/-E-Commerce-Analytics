select d::date as date_day,year(d) as year,quarter(d) as quarter,month(d) as month,dayofweek(d) as weekday
from generate_series((select min(created_at)::date from {{ ref('stg_sessions') }}),
 (select max(created_at)::date from {{ ref('stg_sessions') }}),interval 1 day) as t(d)


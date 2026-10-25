select date_day,count(*) as n from {{ ref('dim_dates') }} group by 1 having date_day is null or count(*)<>1

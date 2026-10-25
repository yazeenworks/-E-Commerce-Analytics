select user_id,count(*) as n from {{ ref('dim_customers') }} group by 1 having user_id is null or count(*)<>1

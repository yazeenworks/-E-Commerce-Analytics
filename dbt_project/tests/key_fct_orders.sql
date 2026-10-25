select order_id,count(*) as n from {{ ref('fct_orders') }} group by 1 having order_id is null or count(*)<>1

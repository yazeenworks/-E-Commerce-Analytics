select user_id,min(created_at) as first_order_at,max(created_at) as last_order_at,
 count(*) as observed_orders,sum(revenue_usd) as observed_sales_usd
from {{ ref('fct_orders') }} group by 1


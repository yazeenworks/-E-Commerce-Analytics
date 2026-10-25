with items as (
 select order_id,count(*) as item_count,sum(revenue_usd) as revenue_usd,sum(cogs_usd) as cogs_usd,
 sum(gross_profit_usd) as gross_profit_usd,sum(refund_usd) as refund_usd,sum(net_sales_usd) as net_sales_usd
 from {{ ref('fct_order_items') }} group by 1
)
select o.order_id,o.created_at,o.created_at::date as order_date,o.user_id,o.website_session_id,o.primary_product_id,
 s.channel,s.campaign,s.device_type,i.item_count,i.revenue_usd,i.cogs_usd,i.gross_profit_usd,i.refund_usd,i.net_sales_usd,
 row_number() over(partition by o.user_id order by o.created_at,o.order_id) as customer_order_number
from {{ ref('stg_orders') }} o join items i using(order_id)
join {{ ref('stg_sessions') }} s using(website_session_id)


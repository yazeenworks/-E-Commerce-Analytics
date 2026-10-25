-- One row per sold item. Aggregate refunds BEFORE any joining.
with refunds as (
 select order_item_id,sum(refund_amount_usd) as refund_usd,count(*) as refund_events
 from {{ ref('stg_refunds') }} group by 1
)
select i.order_item_id,i.order_id,i.product_id,p.product_name,i.is_primary_item,
 o.created_at,o.created_at::date as order_date,o.user_id,o.website_session_id,
 s.channel,s.campaign,s.device_type,i.price_usd as revenue_usd,i.cogs_usd,
 i.price_usd-i.cogs_usd as gross_profit_usd,coalesce(r.refund_usd,0) as refund_usd,
 i.price_usd-coalesce(r.refund_usd,0) as net_sales_usd,
 case when coalesce(r.refund_events,0)>0 then 1 else 0 end as refunded_item
from {{ ref('stg_items') }} i
join {{ ref('stg_orders') }} o using(order_id)
join {{ ref('stg_sessions') }} s using(website_session_id)
join {{ ref('dim_products') }} p using(product_id)
left join refunds r using(order_item_id)


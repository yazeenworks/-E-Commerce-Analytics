select order_item_id from {{ ref('fct_order_items') }} where revenue_usd<=0 or cogs_usd<0 or refund_usd<0

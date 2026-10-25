select order_item_id from {{ ref('fct_order_items') }} where abs(gross_profit_usd-(revenue_usd-cogs_usd))>0.01 or abs(net_sales_usd-(revenue_usd-refund_usd))>0.01

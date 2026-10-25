select order_item_id,count(*) as n from {{ ref('fct_order_items') }} group by 1 having order_item_id is null or count(*)<>1

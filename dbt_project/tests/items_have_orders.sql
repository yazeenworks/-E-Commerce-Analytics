select i.order_item_id from {{ ref('fct_order_items') }} i left join {{ ref('stg_orders') }} o using(order_id) where o.order_id is null

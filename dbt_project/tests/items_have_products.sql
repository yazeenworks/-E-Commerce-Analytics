select i.order_item_id from {{ ref('fct_order_items') }} i left join {{ ref('dim_products') }} p using(product_id) where p.product_id is null

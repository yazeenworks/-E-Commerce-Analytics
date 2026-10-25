select product_id,count(*) as n from {{ ref('dim_products') }} group by 1 having product_id is null or count(*)<>1

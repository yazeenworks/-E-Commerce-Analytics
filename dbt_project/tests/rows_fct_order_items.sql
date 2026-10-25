select 1 where (select count(*) from {{ ref('fct_order_items') }})<>(select count(*) from {{ source('source_csv','order_items') }})

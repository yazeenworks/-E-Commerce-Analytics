select 1 where (select count(*) from {{ ref('fct_orders') }})<>(select count(*) from {{ source('source_csv','orders') }})

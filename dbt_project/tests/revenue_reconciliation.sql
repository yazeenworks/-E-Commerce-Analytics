select 1 where abs((select sum(revenue_usd) from {{ ref('fct_orders') }})-(select sum(price_usd) from {{ source('source_csv','orders') }}))>0.01

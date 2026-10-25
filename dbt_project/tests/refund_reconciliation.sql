select 1 where abs((select sum(refund_usd) from {{ ref('fct_order_items') }})-(select sum(refund_amount_usd) from {{ ref('stg_refunds') }}))>0.01

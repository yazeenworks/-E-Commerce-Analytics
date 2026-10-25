select order_item_refund_id,created_at::timestamp as created_at,order_item_id,order_id,refund_amount_usd::decimal(18,2) as refund_amount_usd from {{ source('source_csv','order_item_refunds') }}

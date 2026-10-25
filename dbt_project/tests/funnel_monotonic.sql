select website_session_id from {{ ref('fct_sessions') }} where reached_thankyou>reached_billing or reached_billing>reached_shipping or reached_shipping>reached_cart or reached_cart>reached_products

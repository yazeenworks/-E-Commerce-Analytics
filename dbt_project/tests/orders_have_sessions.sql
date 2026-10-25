select o.order_id from {{ ref('fct_orders') }} o left join {{ ref('stg_sessions') }} s using(website_session_id) where s.website_session_id is null

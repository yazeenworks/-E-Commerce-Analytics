-- Session grain: pageview and order rollups are joined only after aggregation.
with page_events as (
 select website_session_id,count(*) as pageviews,arg_min(pageview_url,website_pageview_id) as landing_page,
 min(website_pageview_id) filter(where pageview_url='/products') as p,
 min(website_pageview_id) filter(where pageview_url='/cart') as c,
 min(website_pageview_id) filter(where pageview_url='/shipping') as s,
 min(website_pageview_id) filter(where pageview_url in ('/billing','/billing-2')) as b,
 min(website_pageview_id) filter(where pageview_url='/thank-you-for-your-order') as t
 from {{ ref('stg_pageviews') }} group by 1
), order_events as (
 select website_session_id,count(*) as orders,sum(revenue_usd) as revenue_usd,
 sum(gross_profit_usd) as gross_profit_usd,sum(refund_usd) as refund_usd
 from {{ ref('fct_orders') }} group by 1
)
select a.website_session_id,a.created_at,a.created_at::date as session_date,a.user_id,a.is_repeat_session,
 a.channel,a.campaign,a.device_type,coalesce(e.pageviews,0) as pageviews,
 coalesce(e.landing_page,'Unknown') as landing_page,case when e.pageviews=1 then 1 else 0 end as bounced,
 coalesce(o.orders,0) as orders,case when coalesce(o.orders,0)>0 then 1 else 0 end as converted_session,
 coalesce(o.revenue_usd,0) as revenue_usd,coalesce(o.gross_profit_usd,0) as gross_profit_usd,coalesce(o.refund_usd,0) as refund_usd,
 case when p is not null then 1 else 0 end as reached_products,
 case when p<c then 1 else 0 end as reached_cart,
 case when p<c and c<s then 1 else 0 end as reached_shipping,
 case when p<c and c<s and s<b then 1 else 0 end as reached_billing,
 case when p<c and c<s and s<b and b<t then 1 else 0 end as reached_thankyou
from {{ ref('stg_sessions') }} a left join page_events e using(website_session_id)
left join order_events o using(website_session_id)


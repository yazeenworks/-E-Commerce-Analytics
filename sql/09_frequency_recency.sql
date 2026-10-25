with snapshot as (select max(order_date) as snapshot_date from fct_orders)
select user_id,date_diff('day',max(order_date),snapshot_date) as days_since_purchase,count(*) as orders,sum(revenue_usd) as observed_sales,
case when count(*)>=3 then '3+ orders' when count(*)=2 then '2 orders' else '1 order' end as frequency
from fct_orders cross join snapshot group by user_id,snapshot_date order by observed_sales desc;

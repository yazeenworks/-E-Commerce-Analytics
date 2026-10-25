-- SQL long-form reference; dashboard additionally renders observed zero/future null cells.
with first_purchase as (
 select user_id,date_trunc('month',first_order_at)::date as cohort from dim_customers
), active as (
 select distinct o.user_id,f.cohort,date_diff('month',f.cohort,date_trunc('month',o.created_at)) as months_since
 from fct_orders o join first_purchase f using(user_id)
), sizes as (select cohort,count(*) as cohort_buyers from first_purchase group by 1)
select a.cohort,a.months_since,count(*) as active_buyers,s.cohort_buyers,count(*)*1.0/s.cohort_buyers as purchase_retention
from active a join sizes s using(cohort) group by a.cohort,a.months_since,s.cohort_buyers order by 1,2;

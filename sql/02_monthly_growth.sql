-- Only complete interior source months get an unadjusted growth rate.
with monthly as (
 select date_trunc('month',created_at)::date as month,count(*) as orders,sum(revenue_usd) as sales,sum(gross_profit_usd) as gross_profit
 from fct_orders group by 1
), classified as (
 select *,month>(select date_trunc('month',min(session_date)) from fct_sessions)
 and month<(select date_trunc('month',max(session_date)) from fct_sessions) as complete_month from monthly
), lagged as (
 select *,lag(sales) over(order by month) as previous_sales,lag(complete_month) over(order by month) as previous_complete from classified
)
select *,case when complete_month and previous_complete then (sales-previous_sales)/nullif(previous_sales,0) end as sales_mom from lagged order by month;

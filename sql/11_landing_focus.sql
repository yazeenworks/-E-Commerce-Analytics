-- Notebook-specified date window, recomputed from first session entry page.
-- Descriptive comparison, NOT a claim of randomized causal lift or significance.
select landing_page,count(*) as sessions,sum(bounced)*1.0/nullif(count(*),0) as bounce_rate,
sum(reached_products) as reached_products,sum(reached_thankyou) as completed_ordered_path,
sum(reached_thankyou)*1.0/nullif(sum(reached_products),0) as product_to_complete,
sum(converted_session)*1.0/nullif(count(*),0) as session_conversion
from fct_sessions
where session_date between date '2012-06-19' and date '2012-07-28'
and landing_page in ('/home','/lander-1')
group by 1 order by 1;

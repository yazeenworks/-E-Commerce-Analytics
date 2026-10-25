-- Session-grain joins, page-level counts. A session can appear on several different pages.
select p.pageview_url,count(*) as pageviews,count(distinct p.website_session_id) as sessions
from stg_pageviews p join fct_sessions s using(website_session_id)
group by 1 order by pageviews desc;

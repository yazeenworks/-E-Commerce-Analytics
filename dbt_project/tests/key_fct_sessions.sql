select website_session_id,count(*) as n from {{ ref('fct_sessions') }} group by 1 having website_session_id is null or count(*)<>1

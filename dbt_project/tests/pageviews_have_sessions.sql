select p.website_pageview_id from {{ ref('stg_pageviews') }} p left join {{ ref('stg_sessions') }} s using(website_session_id) where s.website_session_id is null

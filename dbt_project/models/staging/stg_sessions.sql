with normalized as (
 select website_session_id,created_at::timestamp as created_at,user_id,is_repeat_session,
 nullif(nullif(trim(utm_source),'NULL'),'') as utm_source,
 nullif(nullif(trim(utm_campaign),'NULL'),'') as utm_campaign,
 nullif(nullif(trim(http_referer),'NULL'),'') as http_referer,device_type
 from {{ source('source_csv','website_sessions') }}
)
select *,coalesce(utm_source,case when http_referer is null then 'Direct' else 'Organic / referral' end) as channel,
 coalesce(utm_campaign,'Unattributed') as campaign from normalized

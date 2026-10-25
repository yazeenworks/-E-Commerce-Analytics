select website_session_id from {{ ref('stg_sessions') }} where channel is null or campaign is null or utm_source='NULL' or utm_campaign='NULL'

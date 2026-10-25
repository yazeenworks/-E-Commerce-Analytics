select 1 where (select count(*) from {{ ref('fct_sessions') }})<>(select count(*) from {{ source('source_csv','website_sessions') }})

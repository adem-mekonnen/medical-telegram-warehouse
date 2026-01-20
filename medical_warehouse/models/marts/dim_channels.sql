with channel_stats as (
    select
        channel_name,
        min(message_date) as first_post_date,
        max(message_date) as last_post_date,
        count(*) as total_posts,
        avg(views) as avg_views
    from {{ ref('stg_telegram_messages') }}
    group by channel_name
)
select 
    -- Generate a surrogate key (hash of the name)
    md5(channel_name) as channel_key,
    channel_name,
    -- Simple logic to determine type based on name (Enhance this logic if you have specific rules)
    case 
        when channel_name ilike '%cosmetic%' then 'Cosmetics'
        when channel_name ilike '%pharma%' then 'Pharmaceutical'
        else 'Medical'
    end as channel_type,
    first_post_date,
    last_post_date,
    total_posts,
    ROUND(avg_views) as avg_views
from channel_stats
with messages as (
    select * from {{ ref('stg_telegram_messages') }}
)
select
    m.message_id,
    -- Foreign Key to dim_channels
    md5(m.channel_name) as channel_key, 
    -- Foreign Key to dim_dates
    date(m.message_date) as date_key,
    m.message_text,
    m.message_length,
    m.views as view_count,
    0 as forward_count, -- Placeholder if you didn't scrape forwards, otherwise use m.forwards
    m.has_media
from messages m
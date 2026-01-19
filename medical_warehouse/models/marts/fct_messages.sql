with messages as (
    select * from {{ ref('stg_telegram_messages') }}
)
select
    m.message_id,
    m.channel_name,
    date(m.message_date) as date_key,
    m.views,
    m.message_text,
    m.has_media
from messages m

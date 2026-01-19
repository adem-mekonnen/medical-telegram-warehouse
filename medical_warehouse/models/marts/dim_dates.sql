select 
    distinct date(message_date) as date_key,
    extract(year from message_date) as year,
    extract(month from message_date) as month,
    to_char(message_date, 'Day') as day_name
from {{ ref('stg_telegram_messages') }}

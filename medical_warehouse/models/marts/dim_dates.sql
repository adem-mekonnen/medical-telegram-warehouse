select 
    distinct date(message_date) as date_key,
    to_char(message_date, 'YYYY-MM-DD') as full_date,
    extract(year from message_date) as year,
    extract(month from message_date) as month,
    to_char(message_date, 'Month') as month_name,
    extract(quarter from message_date) as quarter,
    extract(doy from message_date) as day_of_year,
    to_char(message_date, 'Day') as day_name,
    extract(isodow from message_date) as day_of_week,
    case 
        when extract(isodow from message_date) in (6, 7) then true 
        else false 
    end as is_weekend
from {{ ref('stg_telegram_messages') }}
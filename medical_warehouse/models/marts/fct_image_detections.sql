with source as (
    select * from {{ source('raw_data', 'yolo_detections') }}
),
messages as (
    select message_id, channel_key, date_key from {{ ref('fct_messages') }}
)
select
    s.message_id,
    m.channel_key,
    m.date_key,
    s.detected_class,
    s.confidence as confidence_score,
    s.image_category,
    s.image_path
from source s
-- Inner join to link images to their original messages
join messages m on cast(s.message_id as varchar) = cast(m.message_id as varchar)
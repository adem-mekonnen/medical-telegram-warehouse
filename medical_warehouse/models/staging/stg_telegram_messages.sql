with source as (
    select * from {{ source('raw_data', 'telegram_messages') }}
),
renamed as (
    select
        message_id,
        channel_name,
        CAST(message_date AS TIMESTAMP) as message_date,
        message_text,
        length(message_text) as message_length, -- Added Requirement
        views,
        has_media,
        image_path
    from source
    where message_text is not null
)
select * from renamed
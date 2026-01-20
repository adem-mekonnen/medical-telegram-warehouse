-- This test returns records that are from the future (which shouldn't exist)
select *
from {{ ref('fct_messages') }}
where date_key > CURRENT_DATE
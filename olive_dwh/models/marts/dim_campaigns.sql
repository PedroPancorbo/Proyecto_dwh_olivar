with campaigns as (
    select * from {{ ref('stg_campaigns') }}
)

select
    campaign_id,
    nombre,
    anio_inicio,
    anio_fin,
    estado
from campaigns

with settlements as (
    select * from {{ ref('stg_settlements') }}
),

campaigns as (
    select * from {{ ref('stg_campaigns') }}
),

members as (
    select * from {{ ref('stg_members') }}
)

select
    s.settlement_id,
    s.campaign_id,
    s.member_id,
    s.fecha_liquidacion,
    s.kg_totales,
    s.precio_kg,
    s.importe_final,
    round(s.importe_final / nullif(s.kg_totales, 0), 4)    as precio_efectivo_kg,
    -- claves de dimensiones para joins
    c.nombre                                as campana,
    c.anio_inicio                           as anio_campana,
    m.nombre || ' ' || m.apellidos          as nombre_socio,
    m.municipio                             as municipio_socio
from settlements s
left join campaigns c  on s.campaign_id = c.campaign_id
left join members   m  on s.member_id   = m.member_id

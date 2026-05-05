with deliveries as (
    select * from {{ ref('stg_deliveries') }}
),

campaigns as (
    select * from {{ ref('stg_campaigns') }}
),

members as (
    select * from {{ ref('stg_members') }}
),

plots as (
    select * from {{ ref('stg_plots') }}
),

quality as (
    select * from {{ ref('stg_quality_grades') }}
)

select
    d.delivery_id,
    d.campaign_id,
    d.member_id,
    d.plot_id,
    d.quality_grade_id,
    d.fecha_entrega,
    date_part('year', d.fecha_entrega)      as anio,
    date_part('month', d.fecha_entrega)     as mes,
    d.kg_netos,
    d.origen_recoleccion,
    d.rendimiento_teorico_pct,
    round(d.kg_netos * d.rendimiento_teorico_pct / 100, 2)  as kg_aceite_teorico,
    -- claves de dimensiones para joins
    c.nombre                                as campana,
    m.nombre || ' ' || m.apellidos          as nombre_socio,
    p.municipio                             as municipio_parcela,
    p.variedad                              as variedad,
    q.categoria                             as calidad
from deliveries d
left join campaigns c  on d.campaign_id      = c.campaign_id
left join members   m  on d.member_id        = m.member_id
left join plots     p  on d.plot_id          = p.plot_id
left join quality   q  on d.quality_grade_id = q.quality_grade_id

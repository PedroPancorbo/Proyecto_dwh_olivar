with plots as (
    select * from {{ ref('stg_plots') }}
),

members as (
    select * from {{ ref('stg_members') }}
)

select
    p.plot_id,
    p.member_id,
    m.nombre || ' ' || m.apellidos     as nombre_socio,
    p.referencia_catastral,
    p.municipio,
    p.provincia,
    p.superficie_ha,
    p.variedad,
    p.sistema_riego
from plots p
left join members m on p.member_id = m.member_id

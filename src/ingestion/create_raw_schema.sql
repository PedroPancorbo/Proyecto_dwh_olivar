--==================================
-- ESQUEMAS DEL DATA
--==================================
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

--==================================
-- TABLA: CAMPAÑAS AGRICOLAS
--==================================
CREATE TABLE IF NOT EXISTS raw.campaigns (
    id              SERIAL          PRIMARY KEY,
    nombre          TEXT            NOT NULL,
    anio_inicio     INTEGER         NOT NULL,
    anio_fin        INTEGER         NOT NULL,
    estado          TEXT            NOT NULL,
    _ingested_at    TIMESTAMP       DEFAULT NOW()
);

-- ============================================================
-- TABLA: SOCIOS
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.members (
    id              SERIAL          PRIMARY KEY,
    nombre          TEXT            NOT NULL,
    apellidos       TEXT            NOT NULL,
    nif             TEXT            NOT NULL,
    municipio       TEXT            NOT NULL,
    provincia       TEXT            NOT NULL,
    fecha_alta      DATE            NOT NULL,
    estado          TEXT            NOT NULL,
    _ingested_at    TIMESTAMP       DEFAULT NOW()
);

-- ============================================================
-- TABLA: PARCELAS
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.plots (
    id                      SERIAL          PRIMARY KEY,
    member_id               INTEGER         NOT NULL,
    referencia_catastral    TEXT            NOT NULL,
    municipio               TEXT            NOT NULL,
    provincia               TEXT            NOT NULL,
    superficie_ha           NUMERIC(8,2)    NOT NULL,
    variedad                TEXT            NOT NULL,
    sistema_riego           TEXT            NOT NULL,
    _ingested_at            TIMESTAMP       DEFAULT NOW()
);
-- ============================================================
-- TABLA: GRADOS DE CALIDAD
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.quality_grades (
    id              SERIAL          PRIMARY KEY,
    categoria       TEXT            NOT NULL,
    acidity_max     NUMERIC(4,2)    NOT NULL,
    descripcion     TEXT,
    _ingested_at    TIMESTAMP       DEFAULT NOW()
);
-- ============================================================
-- TABLA: ENTREGAS DE ACEITUNA
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.deliveries (
    id                      SERIAL          PRIMARY KEY,
    campaign_id             INTEGER         NOT NULL,
    member_id               INTEGER         NOT NULL,
    plot_id                 INTEGER         NOT NULL,
    quality_grade_id        INTEGER         NOT NULL,
    fecha_entrega           DATE            NOT NULL,
    kg_netos                NUMERIC(10,2)   NOT NULL,
    origen_recoleccion      TEXT            NOT NULL,
    rendimiento_teorico_pct NUMERIC(5,2)    NOT NULL,
    _ingested_at            TIMESTAMP       DEFAULT NOW()
);
-- ============================================================
-- TABLA: LIQUIDACIONES
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.settlements (
    id                  SERIAL          PRIMARY KEY,
    campaign_id         INTEGER         NOT NULL,
    member_id           INTEGER         NOT NULL,
    fecha_liquidacion   DATE            NOT NULL,
    kg_totales          NUMERIC(12,2)   NOT NULL,
    precio_kg           NUMERIC(8,4)    NOT NULL,
    importe_final       NUMERIC(12,2)   NOT NULL,
    _ingested_at        TIMESTAMP       DEFAULT NOW()
);
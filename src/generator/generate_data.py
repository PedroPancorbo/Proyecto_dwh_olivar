"""
Generador de datos sintéticos para la Cooperativa Olivarera de Jaén.
Produce archivos CSV en data/raw/ listos para ser ingestados en el DWH.
"""

import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta
from pathlib import Path

fake = Faker("es_ES")
random.seed(42)
np.random.seed(42)

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_MEMBERS = 200

MUNICIPIOS_JAEN = [
    "Jaén", "Úbeda", "Baeza", "Linares", "Andújar", "Alcalá la Real",
    "Martos", "Torredelcampo", "Mancha Real", "Mengíbar", "Bailén",
    "Villacarrillo", "Cazorla", "Quesada", "Jodar", "Torredonjimeno",
    "Alcaudete", "Porcuna", "Arjona", "Lopera", "Espeluy", "Guarromán",
    "Iznatoraf", "Segura de la Sierra", "Santiago de la Espada",
]

VARIEDADES = ["Picual"] * 9 + ["Arbequina"]  # 90% Picual

SISTEMAS_RIEGO = ["Secano"] * 8 + ["Goteo"] * 2  # 80% secano

CALIDAD = [
    {"categoria": "Virgen Extra", "acidity_max": 0.80, "descripcion": "Acidez ≤ 0.8%. Máxima calidad."},
    {"categoria": "Virgen",       "acidity_max": 2.00, "descripcion": "Acidez ≤ 2.0%. Buena calidad."},
    {"categoria": "Lampante",     "acidity_max": 9.99, "descripcion": "Acidez > 2.0%. Requiere refinado."},
]

# Campañas: (nombre, anio_inicio, anio_fin, estado, precio_min, precio_max, duracion_dias_aprox)
CAMPANAS = [
    ("Campaña 2019/20", 2019, 2020, "cerrada",  0.44, 0.48, 90),
    ("Campaña 2020/21", 2020, 2021, "cerrada",  0.47, 0.54, 85),
    ("Campaña 2021/22", 2021, 2022, "cerrada",  0.65, 0.75, 95),
    ("Campaña 2022/23", 2022, 2023, "cerrada",  0.95, 1.15, 70),  # sequía → campaña corta
    ("Campaña 2023/24", 2023, 2024, "cerrada",  1.03, 1.25, 75),  # segunda sequía
]

# ─────────────────────────────────────────
# GENERADORES
# ─────────────────────────────────────────

def gen_campaigns():
    rows = []
    for nombre, anio_inicio, anio_fin, estado, _, _, _ in CAMPANAS:
        rows.append({
            "nombre":      nombre,
            "anio_inicio": anio_inicio,
            "anio_fin":    anio_fin,
            "estado":      estado,
        })
    return pd.DataFrame(rows)


def gen_quality_grades():
    return pd.DataFrame(CALIDAD)


def gen_members():
    rows = []
    for _ in range(NUM_MEMBERS):
        municipio = random.choice(MUNICIPIOS_JAEN)
        fecha_alta = fake.date_between(start_date=date(2000, 1, 1), end_date=date(2019, 1, 1))
        rows.append({
            "nombre":     fake.first_name(),
            "apellidos":  f"{fake.last_name()} {fake.last_name()}",
            "nif":        fake.nif(),
            "municipio":  municipio,
            "provincia":  "Jaén",
            "fecha_alta": fecha_alta,
            "estado":     random.choices(["activo", "inactivo"], weights=[95, 5])[0],
        })
    return pd.DataFrame(rows)


def gen_plots(members_df):
    rows = []
    for member_id, _ in members_df.iterrows():
        num_parcelas = int(np.random.triangular(1, 3, 30))  # mayoría 2-5, alguna llega a 30
        for _ in range(num_parcelas):
            # Superficie: distribución realista de Jaén (mediana ~0.68 ha)
            superficie = round(np.random.lognormal(mean=-0.4, sigma=0.9), 2)
            superficie = max(0.10, min(superficie, 15.0))  # clamp entre 0.1 y 15 ha

            municipio = random.choice(MUNICIPIOS_JAEN)
            # Referencia catastral: formato simplificado (14 dígitos + 4 letras)
            ref_catastral = (
                f"{random.randint(10,99)}"
                f"{random.randint(100,999)}"
                f"{random.randint(10000,99999)}"
                f"{''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=4))}"
            )
            rows.append({
                "member_id":            member_id + 1,  # ID en BD empieza en 1
                "referencia_catastral": ref_catastral,
                "municipio":            municipio,
                "provincia":            "Jaén",
                "superficie_ha":        superficie,
                "variedad":             random.choice(VARIEDADES),
                "sistema_riego":        random.choice(SISTEMAS_RIEGO),
            })
    return pd.DataFrame(rows)


def gen_deliveries_and_settlements(members_df, plots_df, campaigns_df, quality_df):
    deliveries = []
    settlements = []

    for camp_idx, camp_row in campaigns_df.iterrows():
        campaign_id  = camp_idx + 1
        anio_inicio  = camp_row["anio_inicio"]
        anio_fin     = camp_row["anio_fin"]
        _, _, _, _, precio_min, precio_max, duracion_dias = CAMPANAS[camp_idx]

        # Ventana de campaña: nov anio_inicio → ene/feb anio_fin
        camp_start = date(anio_inicio, 11, 1)
        camp_end   = camp_start + timedelta(days=duracion_dias)

        precio_kg_final = round(random.uniform(precio_min, precio_max), 4)

        active_members = members_df[members_df["estado"] == "activo"]

        for member_idx, member_row in active_members.iterrows():
            member_id = member_idx + 1

            # Parcelas de este socio
            member_plots = plots_df[plots_df["member_id"] == member_id]
            if member_plots.empty:
                continue

            kg_totales_socio = 0.0

            for plot_idx, plot_row in member_plots.iterrows():
                plot_id = plot_idx + 1

                # kg producidos por parcela: superficie × rendimiento campaña (kg/ha)
                # Varía por campaña (sequía = menos producción)
                kg_ha_base = random.uniform(1500, 5000)
                # Años de sequía: reducción
                if "2022/23" in camp_row["nombre"] or "2023/24" in camp_row["nombre"]:
                    kg_ha_base *= random.uniform(0.35, 0.55)

                kg_parcela = plot_row["superficie_ha"] * kg_ha_base

                # Número de entregas para esta parcela en esta campaña
                num_entregas = max(1, int(np.random.poisson(lam=8)))
                kg_entrega_base = kg_parcela / num_entregas

                for _ in range(num_entregas):
                    fecha = camp_start + timedelta(days=random.randint(0, duracion_dias - 1))
                    kg = round(kg_entrega_base * random.uniform(0.7, 1.3), 2)
                    kg = max(50.0, kg)  # mínimo 50 kg por entrega

                    # Calidad: más VE en inicio de campaña, más lampante al final
                    dias_desde_inicio = (fecha - camp_start).days
                    if dias_desde_inicio < duracion_dias * 0.4:
                        quality_weights = [70, 25, 5]   # inicio: más VE
                    elif dias_desde_inicio < duracion_dias * 0.75:
                        quality_weights = [40, 45, 15]  # mitad: más virgen
                    else:
                        quality_weights = [15, 50, 35]  # final: más lampante

                    quality_id = random.choices([1, 2, 3], weights=quality_weights)[0]
                    rendimiento = round(random.uniform(12.0, 25.0), 2)

                    deliveries.append({
                        "campaign_id":             campaign_id,
                        "member_id":               member_id,
                        "plot_id":                 plot_id,
                        "quality_grade_id":        quality_id,
                        "fecha_entrega":           fecha,
                        "kg_netos":                kg,
                        "origen_recoleccion":      random.choices(
                                                       ["Vareo", "Mecanizada", "Manual"],
                                                       weights=[70, 20, 10]
                                                   )[0],
                        "rendimiento_teorico_pct": rendimiento,
                    })
                    kg_totales_socio += kg

            # Liquidación por socio y campaña
            if kg_totales_socio > 0:
                fecha_liq = camp_end + timedelta(days=random.randint(30, 90))
                importe    = round(kg_totales_socio * precio_kg_final, 2)
                settlements.append({
                    "campaign_id":      campaign_id,
                    "member_id":        member_id,
                    "fecha_liquidacion": fecha_liq,
                    "kg_totales":       round(kg_totales_socio, 2),
                    "precio_kg":        precio_kg_final,
                    "importe_final":    importe,
                })

    return pd.DataFrame(deliveries), pd.DataFrame(settlements)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("Generando datos...")

    campaigns_df    = gen_campaigns()
    quality_df      = gen_quality_grades()
    members_df      = gen_members()
    plots_df        = gen_plots(members_df)
    deliveries_df, settlements_df = gen_deliveries_and_settlements(
        members_df, plots_df, campaigns_df, quality_df
    )

    # Guardar CSVs
    campaigns_df.to_csv(OUTPUT_DIR / "campaigns.csv",     index=False)
    quality_df.to_csv(  OUTPUT_DIR / "quality_grades.csv", index=False)
    members_df.to_csv(  OUTPUT_DIR / "members.csv",        index=False)
    plots_df.to_csv(    OUTPUT_DIR / "plots.csv",          index=False)
    deliveries_df.to_csv(OUTPUT_DIR / "deliveries.csv",   index=False)
    settlements_df.to_csv(OUTPUT_DIR / "settlements.csv", index=False)

    print(f"  campaigns:     {len(campaigns_df):>6} filas")
    print(f"  quality_grades:{len(quality_df):>6} filas")
    print(f"  members:       {len(members_df):>6} filas")
    print(f"  plots:         {len(plots_df):>6} filas")
    print(f"  deliveries:    {len(deliveries_df):>6} filas")
    print(f"  settlements:   {len(settlements_df):>6} filas")
    print(f"\nArchivos guardados en: {OUTPUT_DIR.resolve()}")

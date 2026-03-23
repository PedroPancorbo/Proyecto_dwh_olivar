"""
Script de ingesta: carga los CSVs de data/raw/ en las tablas raw.* de PostgreSQL.
Ejecutar desde la raíz del proyecto con el entorno virtual activado.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────

DB_USER = os.getenv("POSTGRES_USER", "olive")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "olive_pwd")
DB_NAME = os.getenv("POSTGRES_DB", "olive_dwh")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

RAW_DIR = Path("data/raw")

# ─────────────────────────────────────────
# ORDEN DE CARGA (respeta dependencias FK)
# ─────────────────────────────────────────

TABLES = [
    ("campaigns",     "campaigns.csv"),
    ("quality_grades","quality_grades.csv"),
    ("members",       "members.csv"),
    ("plots",         "plots.csv"),
    ("deliveries",    "deliveries.csv"),
    ("settlements",   "settlements.csv"),
]

# ─────────────────────────────────────────
# CARGA
# ─────────────────────────────────────────

def truncate_table(conn, table):
    conn.execute(text(f"TRUNCATE TABLE raw.{table} RESTART IDENTITY CASCADE"))

def load_table(table, csv_file):
    csv_path = RAW_DIR / csv_file
    df = pd.read_csv(csv_path)
    print(f"  Cargando {table:20s} ({len(df):>6} filas)...", end=" ")

    with engine.begin() as conn:
        truncate_table(conn, table)

    df.to_sql(
        name=table,
        schema="raw",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )
    print("OK")

if __name__ == "__main__":
    print("Iniciando ingesta en raw.*\n")
    for table, csv_file in TABLES:
        load_table(table, csv_file)
    print("\nIngesta completada.")

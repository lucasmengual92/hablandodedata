
# Databricks notebook source
# ============================================================
# DATA QUALITY CON DQX SOBRE EXCEL DE PRESUPUESTO FINANCIERO
# ============================================================
#
# Caso de uso:
# Finanzas mantiene un Excel de presupuesto trimestral.
# Queremos validar la calidad antes de consumirlo en BI.
#
# ============================================================

# COMMAND ----------
# 0. Imports necesarios (sin alias F)

from pyspark.sql.functions import col, lower, regexp_replace, current_timestamp
from databricks.labs.dqx.engine import DQEngine
import yaml

# COMMAND ----------
# 1. Funciones auxiliares reutilizables

def sanitize_columns(df):
    new_cols = [regexp_replace(lower(c), "[^a-z0-9_]", "_") for c in df.columns]
    return df.toDF(*new_cols)

# COMMAND ----------
# 2. Configuración del demo

BASE_PATH = "/Workspace/Repos/<TU_USUARIO>/hablandodedata/databricks/notebooks/tutorials/data_quality_con_dqx_excel_budget"
EXCEL_PATH = f"{BASE_PATH}/Finance_Budget_Q1_2026.xlsx"
RULES_PATH = f"{BASE_PATH}/budget_dqx_rules.yml"

TARGET_TABLE = "hive_metastore.default.budget_silver"
QUARANTINE_TABLE = "hive_metastore.default.budget_quarantine"

# COMMAND ----------
# 3. Lectura del Excel

df_raw = (
    spark.read.format("excel")
    .option("headerRows", "1")
    .option("inferColumnTypes", "true")
    .load(EXCEL_PATH)
)

# COMMAND ----------
# 4. Limpieza de nombres de columnas

df_clean = sanitize_columns(df_raw)

# COMMAND ----------
# 5. Tabla de referencia de entidades legales

spark.sql("""
CREATE OR REPLACE TEMP VIEW legal_entity_ref AS
SELECT 'ES01' AS legal_entity UNION ALL
SELECT 'NL01' UNION ALL
SELECT 'CZ01'
""")

allowed_entities = [r.legal_entity for r in spark.table("legal_entity_ref").collect()]

# COMMAND ----------
# 6. Carga de reglas desde YAML

with open(RULES_PATH, "r") as f:
    checks = yaml.safe_load(f)

for c in checks:
    if c["name"] == "legal_entity_permitida":
        c["check"]["arguments"]["allowed"] = allowed_entities

# COMMAND ----------
# 7. Aplicación de Data Quality con DQX

dq_engine = DQEngine()
valid_df, quarantined_df = dq_engine.apply_checks_by_metadata_and_split(
    df_clean, checks
)

# COMMAND ----------
# 8. Escritura de resultados

(valid_df.write.format("delta")
 .mode("overwrite")
 .saveAsTable(TARGET_TABLE))

(quarantined_df
 .withColumn("_quarantine_ts", current_timestamp())
 .write.format("delta")
 .mode("overwrite")
 .saveAsTable(QUARANTINE_TABLE))

# COMMAND ----------
# 9. Resultado final

display(valid_df)
display(quarantined_df)

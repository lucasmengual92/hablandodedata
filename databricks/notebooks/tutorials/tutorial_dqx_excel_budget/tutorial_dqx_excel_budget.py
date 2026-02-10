
# Databricks notebook source
# ============================================================
# TUTORIAL: Data Quality con DQX sobre Excel de Presupuesto
# ============================================================
#
# Caso de uso real:
# El área de Finanzas mantiene un Excel de presupuesto trimestral
# llamado, por ejemplo, Finance_Budget_Q1_2026.xlsx.
#
# Este fichero se actualiza manualmente y se utiliza luego para:
#  - reporting financiero
#  - dashboards de BI
#  - análisis de forecast
#
# Problema:
# - no hay garantías de calidad
# - errores llegan a producción
#
# Objetivo:
# Aplicar Data Quality de forma estandarizada usando DQX,
# separando datos válidos y datos en cuarentena.
#
# ============================================================

# COMMAND ----------
from pyspark.sql import functions as F
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
import yaml
import re

# COMMAND ----------
# ------------------------------------------------------------
# 1. Configuración del demo
# ------------------------------------------------------------
BASE_PATH = "/Workspace/Repos/<TU_USUARIO>/hablandodedata/databricks/notebooks/tutorials/tutorial_dqx_excel_budget"
EXCEL_PATH = f"{BASE_PATH}/Finance_Budget_Q1_2026.xlsx"
RULES_PATH = f"{BASE_PATH}/budget_dqx_rules.yml"

TARGET_TABLE = "default.budget_q1_2026_silver"
QUARANTINE_TABLE = "default.budget_q1_2026_quarantine"

# COMMAND ----------
# ------------------------------------------------------------
# 2. Lectura del Excel de presupuesto
# ------------------------------------------------------------
df_raw = (
    spark.read.format("excel")
    .option("headerRows", "1")
    .option("inferColumnTypes", "true")
    .load(EXCEL_PATH)
)

display(df_raw)

# COMMAND ----------
# ------------------------------------------------------------
# 3. Limpieza de nombres de columnas
# ------------------------------------------------------------
def sanitize_col(c):
    c = c.strip()
    c = re.sub(r"\s+", "_", c)
    c = re.sub(r"[^0-9a-zA-Z_]", "", c)
    return c.lower()

df = df_raw.toDF(*[sanitize_col(c) for c in df_raw.columns])
display(df)

# COMMAND ----------
# ------------------------------------------------------------
# 4. Tabla de referencia de entidades legales
# ------------------------------------------------------------
legal_entities = [("ES01",), ("NL01",), ("CZ01",)]
spark.createDataFrame(legal_entities, ["legal_entity"])      .write.mode("overwrite").saveAsTable("default.ref_legal_entity")

# COMMAND ----------
# ------------------------------------------------------------
# 5. Carga de reglas de Data Quality desde YAML
# ------------------------------------------------------------
with open(RULES_PATH, "r") as f:
    checks = yaml.safe_load(f)

allowed_entities = [
    r["legal_entity"]
    for r in spark.table("default.ref_legal_entity").collect()
]

for c in checks:
    if c["name"] == "legal_entity_allowed":
        c["check"]["arguments"]["allowed"] = allowed_entities

# COMMAND ----------
# ------------------------------------------------------------
# 6. Aplicación de Data Quality con DQX
# ------------------------------------------------------------
dq_engine = DQEngine(WorkspaceClient())
valid_df, quarantine_df = dq_engine.apply_checks_by_metadata_and_split(df, checks)

# COMMAND ----------
# ------------------------------------------------------------
# 7. Escritura de resultados
# ------------------------------------------------------------
valid_df.write.mode("overwrite").saveAsTable(TARGET_TABLE)
quarantine_df.write.mode("overwrite").saveAsTable(QUARANTINE_TABLE)

display(valid_df)
display(quarantine_df)

# COMMAND ----------
# ------------------------------------------------------------
# 8. Patrón estándar de alertas
# ------------------------------------------------------------
if quarantine_df.count() > 0:
    raise Exception("Se detectaron registros en cuarentena. Revisar calidad de datos.")

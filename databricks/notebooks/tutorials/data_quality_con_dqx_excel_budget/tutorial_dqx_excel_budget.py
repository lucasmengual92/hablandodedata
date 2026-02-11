# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # DATA QUALITY CON DQX
# MAGIC
# MAGIC **Caso de uso:**
# MAGIC - Finanzas mantiene un Excel de presupuesto trimestral.
# MAGIC - Queremos validar la calidad antes de consumirlo en BI.
# MAGIC - Vamos a usar una feature (aun part de Databricks-Labs) que se llama DQX.
# MAGIC   - Para crear reglas (aka expectations) para hacer Data quality sobre nuestro data object (aka dataframe del excel).
# MAGIC

# COMMAND ----------

# Imports necesarios

from pyspark.sql.functions import current_timestamp
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
import yaml
import re

# COMMAND ----------

# Funciones auxiliares reutilizables

def sanitize_columns(df):
    new_cols = [
        re.sub(r"[^a-z0-9_]", "_", c.strip().lower())
        for c in df.columns
    ]
    return df.toDF(*new_cols)

# COMMAND ----------

# Configuración del demo

BASE_PATH = "/Workspace/Repos/<TU_USUARIO>/hablandodedata/databricks/notebooks/tutorials/data_quality_con_dqx_excel_budget" # not used por ahora
EXCEL_PATH = "/Volumes/hablando_de_data/demos/read_excel_finanzas/Finance_Budget_Q1_2026.xlsx"
RULES_PATH = "/Volumes/hablando_de_data/demos/read_excel_finanzas/budget_dqx_rules.yml"

TARGET_TABLE = "hablando_de_data.default.budget_bronze"
QUARANTINE_TABLE = "hablando_de_data.default.budget_quarantine"

# COMMAND ----------

# Lectura del Excel y transformación de columnas

df_raw = (
    spark.read.format("excel")
    .option("headerRows", "1")
    .option("inferColumnTypes", "true")
    .load(EXCEL_PATH)
)

df_clean = sanitize_columns(df_raw)

display(df_clean)

# COMMAND ----------

# Creando una tabla de referencia de entidades legales

spark.sql(
    """
    CREATE OR REPLACE TEMP VIEW legal_entity_ref AS
    SELECT 'ES01' AS legal_entity UNION ALL
    SELECT 'NL01' UNION ALL
    SELECT 'CZ01'
    """
    )

# creamos una lista con esas entidades permitidas/legales
allowed_entities = [r.legal_entity for r in spark.table("legal_entity_ref").collect()]

print(allowed_entities)

# COMMAND ----------

# Cargando las reglas desde YAML

with open(RULES_PATH, "r") as f:
    checks = yaml.safe_load(f)

#allowed_entities = 'DtMF'
# Llenamos la regla de 'legal_entity_permitida' a partir de la lista de entidades permitidas
for c in checks:
    if c["name"] == "legal_entity_permitida":
        c["check"]["arguments"]["allowed"] = allowed_entities

checks

# COMMAND ----------

# Validamos las reglas (opcional)

status = DQEngine.validate_checks(checks)
if getattr(status, "has_errors", False):
    raise ValueError(f"DQX checks validation failed: {status}")

# COMMAND ----------

# Aplicación de Data Quality con DQX

dq_engine = DQEngine(WorkspaceClient())
valid_df, quarantined_df = dq_engine.apply_checks_by_metadata_and_split(df_clean, checks)

# COMMAND ----------

# Escritura de los resultados

(valid_df.write.format("delta").mode("overwrite").saveAsTable(TARGET_TABLE))

(
    quarantined_df.withColumn("_quarantine_ts", current_timestamp())
    .write.format("delta")
    .mode("overwrite")
    .saveAsTable(QUARANTINE_TABLE)
)

# COMMAND ----------

# Resultado final

display(valid_df)
display(quarantined_df)

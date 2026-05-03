# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # Azure Databricks Excel Add-in - paso a paso
# MAGIC
# MAGIC En este tutorial vamos a preparar una tabla demo en Databricks
# MAGIC y luego usarla desde Excel con el Azure Databricks Excel Add-in.
# MAGIC
# MAGIC El objetivo no es reemplazar Excel.
# MAGIC
# MAGIC El objetivo es conectar Excel a datos gobernados en Databricks.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Crear datos demo

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.functions import col, round

data = [
    Row(order_id=1, order_date="2026-01-05", country="Netherlands", category="Candy", customer_segment="Retail", quantity=120, unit_price=1.25, discount=0.05),
    Row(order_id=2, order_date="2026-01-08", country="Spain", category="Gum", customer_segment="Wholesale", quantity=300, unit_price=0.80, discount=0.10),
    Row(order_id=3, order_date="2026-01-12", country="Italy", category="Chocolate", customer_segment="Retail", quantity=180, unit_price=1.60, discount=0.00),
    Row(order_id=4, order_date="2026-02-03", country="Germany", category="Candy", customer_segment="Retail", quantity=220, unit_price=1.15, discount=0.07),
    Row(order_id=5, order_date="2026-02-11", country="Netherlands", category="Gum", customer_segment="Online", quantity=140, unit_price=0.95, discount=0.03),
    Row(order_id=6, order_date="2026-02-18", country="France", category="Chocolate", customer_segment="Wholesale", quantity=260, unit_price=1.45, discount=0.12),
    Row(order_id=7, order_date="2026-03-02", country="Spain", category="Candy", customer_segment="Online", quantity=90, unit_price=1.30, discount=0.02),
    Row(order_id=8, order_date="2026-03-09", country="Italy", category="Gum", customer_segment="Retail", quantity=400, unit_price=0.75, discount=0.08),
]

df = spark.createDataFrame(data)

df = df.withColumn(
    "total_amount",
    round(col("quantity") * col("unit_price") * (1 - col("discount")), 2)
)

display(df)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Guardar como tabla Delta
# MAGIC
# MAGIC Cambiá el catálogo/esquema si querés usar otro path.

# COMMAND ----------

catalog = "workspace"
schema = "default"
table_name = "excel_add_in_sales_demo"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

(
    df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{catalog}.{schema}.{table_name}")
)

print(f"Tabla creada: {catalog}.{schema}.{table_name}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Query simple para probar desde Excel

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   country,
# MAGIC   category,
# MAGIC   SUM(total_amount) AS sales_amount,
# MAGIC   SUM(quantity) AS total_quantity
# MAGIC FROM workspace.default.excel_add_in_sales_demo
# MAGIC GROUP BY country, category
# MAGIC ORDER BY sales_amount DESC;

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Query mensual para Pivot Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   date_trunc('month', CAST(order_date AS DATE)) AS sales_month,
# MAGIC   country,
# MAGIC   category,
# MAGIC   customer_segment,
# MAGIC   SUM(total_amount) AS sales_amount,
# MAGIC   SUM(quantity) AS total_quantity
# MAGIC FROM workspace.default.excel_add_in_sales_demo
# MAGIC GROUP BY
# MAGIC   date_trunc('month', CAST(order_date AS DATE)),
# MAGIC   country,
# MAGIC   category,
# MAGIC   customer_segment
# MAGIC ORDER BY sales_month, country, category;

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Checklist de capturas para el post
# MAGIC
# MAGIC Guardar las imágenes en:
# MAGIC
# MAGIC `databricks/notebooks/tutorials/excel_add_in/images/`
# MAGIC
# MAGIC Sugerencia:
# MAGIC
# MAGIC - `01_excel_add_in_install.png`
# MAGIC - `02_connect_to_databricks.png`
# MAGIC - `03_browse_tables.png`
# MAGIC - `04_import_table_to_excel.png`
# MAGIC - `05_run_sql_query.png`
# MAGIC - `06_create_pivot_table.png`
# MAGIC - `07_refresh_data.png`

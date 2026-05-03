# Databricks notebook source
# MAGIC %md
# MAGIC # Azure Databricks Excel Add-in - Paso a paso
# MAGIC
# MAGIC En este tutorial vamos a preparar una tabla demo en Databricks para probar el **Azure Databricks Excel Add-in**.
# MAGIC
# MAGIC La parte interesante no es solo conectar Excel con Databricks.
# MAGIC
# MAGIC La parte interesante es que Excel puede consumir datos gobernados desde Unity Catalog, sin exportar CSVs manualmente.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Crear una tabla demo en Unity Catalog
# MAGIC
# MAGIC En mi caso voy a usar el catálogo:
# MAGIC
# MAGIC `hablando_de_data`
# MAGIC
# MAGIC y el schema:
# MAGIC
# MAGIC `default`
# MAGIC
# MAGIC La tabla final será:
# MAGIC
# MAGIC `hablando_de_data.default.excel_add_in_sales_demo`

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.functions import col, round

catalog = "hablando_de_data"
schema = "default"
table_name = "excel_add_in_sales_demo"

full_table_name = f"{catalog}.{schema}.{table_name}"

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
# MAGIC ## 2. Guardar la tabla como Delta table
# MAGIC
# MAGIC Esta tabla será la que después vamos a consumir desde Excel usando el add-in.

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

(
    df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(full_table_name)
)

print(f"Tabla creada: {full_table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Validar la tabla
# MAGIC
# MAGIC Antes de ir a Excel, validamos que la tabla exista y que se pueda consultar desde Databricks.

# COMMAND ----------

display(spark.table(full_table_name))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   country,
# MAGIC   category,
# MAGIC   SUM(total_amount) AS sales_amount,
# MAGIC   SUM(quantity) AS total_quantity
# MAGIC FROM hablando_de_data.default.excel_add_in_sales_demo
# MAGIC GROUP BY country, category
# MAGIC ORDER BY sales_amount DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Queries para probar desde Excel
# MAGIC
# MAGIC Una vez instalado el Excel Add-in, podés copiar estas queries desde Excel usando la opción de escribir SQL.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 1 - Ventas por país y categoría
# MAGIC
# MAGIC ```sql
# MAGIC SELECT
# MAGIC   country,
# MAGIC   category,
# MAGIC   SUM(total_amount) AS sales_amount,
# MAGIC   SUM(quantity) AS total_quantity
# MAGIC FROM hablando_de_data.default.excel_add_in_sales_demo
# MAGIC GROUP BY country, category
# MAGIC ORDER BY sales_amount DESC;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 2 - Ventas mensuales para Pivot Tables
# MAGIC
# MAGIC ```sql
# MAGIC SELECT
# MAGIC   date_trunc('month', CAST(order_date AS DATE)) AS sales_month,
# MAGIC   country,
# MAGIC   category,
# MAGIC   customer_segment,
# MAGIC   SUM(total_amount) AS sales_amount,
# MAGIC   SUM(quantity) AS total_quantity
# MAGIC FROM hablando_de_data.default.excel_add_in_sales_demo
# MAGIC GROUP BY
# MAGIC   date_trunc('month', CAST(order_date AS DATE)),
# MAGIC   country,
# MAGIC   category,
# MAGIC   customer_segment
# MAGIC ORDER BY sales_month, country, category;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 3 - Detalle completo para importar en Excel
# MAGIC
# MAGIC ```sql
# MAGIC SELECT
# MAGIC   order_id,
# MAGIC   CAST(order_date AS DATE) AS order_date,
# MAGIC   country,
# MAGIC   category,
# MAGIC   customer_segment,
# MAGIC   quantity,
# MAGIC   unit_price,
# MAGIC   discount,
# MAGIC   total_amount
# MAGIC FROM hablando_de_data.default.excel_add_in_sales_demo
# MAGIC ORDER BY order_date, order_id;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Qué sigue en Excel
# MAGIC
# MAGIC A partir de acá, el tutorial continúa en Excel.
# MAGIC
# MAGIC El flujo sería:
# MAGIC
# MAGIC 1. Instalar el Azure Databricks Excel Add-in.
# MAGIC 2. Conectarlo con tu workspace de Azure Databricks.
# MAGIC 3. Seleccionar un SQL Warehouse.
# MAGIC 4. Buscar la tabla:
# MAGIC
# MAGIC `hablando_de_data.default.excel_add_in_sales_demo`
# MAGIC
# MAGIC 5. Importar la tabla directamente en Excel.
# MAGIC 6. Probar una query SQL desde Excel.
# MAGIC 7. Crear una Pivot Table.
# MAGIC 8. Refrescar los datos desde el add-in.
# MAGIC
# MAGIC La idea no es reemplazar Excel.
# MAGIC
# MAGIC La idea es dejar de exportar CSVs manualmente y empezar a consumir datos gobernados desde Databricks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Mensaje clave
# MAGIC
# MAGIC Excel sigue vivo.
# MAGIC
# MAGIC La diferencia es que ahora puede estar conectado a datos gobernados en Unity Catalog.
# MAGIC
# MAGIC Menos exports.
# MAGIC Menos copias manuales.
# MAGIC Menos versiones raras del mismo dato.
# MAGIC
# MAGIC Más governance.

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

# DBTITLE 1,Cell 3
# MAGIC %sql
# MAGIC -- Crear schema si no existe
# MAGIC CREATE SCHEMA IF NOT EXISTS hablando_de_data.default;
# MAGIC
# MAGIC -- Crear y cargar la tabla demo
# MAGIC CREATE OR REPLACE TABLE hablando_de_data.default.excel_add_in_sales_demo (
# MAGIC   order_id INT,
# MAGIC   order_date DATE,
# MAGIC   country STRING,
# MAGIC   category STRING,
# MAGIC   customer_segment STRING,
# MAGIC   quantity INT,
# MAGIC   unit_price DECIMAL(10,2),
# MAGIC   discount DECIMAL(5,2),
# MAGIC   total_amount DECIMAL(10,2)
# MAGIC );
# MAGIC
# MAGIC INSERT INTO hablando_de_data.default.excel_add_in_sales_demo VALUES
# MAGIC   (1, '2026-01-05', 'Netherlands', 'Candy', 'Retail', 120, 1.25, 0.05, ROUND(120 * 1.25 * (1 - 0.05), 2)),
# MAGIC   (2, '2026-01-08', 'Spain', 'Gum', 'Wholesale', 300, 0.80, 0.10, ROUND(300 * 0.80 * (1 - 0.10), 2)),
# MAGIC   (3, '2026-01-12', 'Italy', 'Chocolate', 'Retail', 180, 1.60, 0.00, ROUND(180 * 1.60 * (1 - 0.00), 2)),
# MAGIC   (4, '2026-02-03', 'Germany', 'Candy', 'Retail', 220, 1.15, 0.07, ROUND(220 * 1.15 * (1 - 0.07), 2)),
# MAGIC   (5, '2026-02-11', 'Netherlands', 'Gum', 'Online', 140, 0.95, 0.03, ROUND(140 * 0.95 * (1 - 0.03), 2)),
# MAGIC   (6, '2026-02-18', 'France', 'Chocolate', 'Wholesale', 260, 1.45, 0.12, ROUND(260 * 1.45 * (1 - 0.12), 2)),
# MAGIC   (7, '2026-03-02', 'Spain', 'Candy', 'Online', 90, 1.30, 0.02, ROUND(90 * 1.30 * (1 - 0.02), 2)),
# MAGIC   (8, '2026-03-09', 'Italy', 'Gum', 'Retail', 400, 0.75, 0.08, ROUND(400 * 0.75 * (1 - 0.08), 2));
# MAGIC
# MAGIC -- Mostrar los datos insertados
# MAGIC SELECT * FROM hablando_de_data.default.excel_add_in_sales_demo;

# COMMAND ----------

# DBTITLE 1,Cell 4
# MAGIC %md
# MAGIC ## 2. Validar la tabla
# MAGIC
# MAGIC Antes de ir a Excel, validamos que la tabla exista y que se pueda consultar desde Databricks.

# COMMAND ----------

# DBTITLE 1,Cell 7
# MAGIC %sql
# MAGIC SELECT * FROM hablando_de_data.default.excel_add_in_sales_demo;

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

# DBTITLE 1,Cell 9
# MAGIC %md
# MAGIC ## 3. Queries para probar desde Excel
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

# DBTITLE 1,Cell 13
# MAGIC %md
# MAGIC ## 4. Qué sigue en Excel
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

# DBTITLE 1,Cell 14
# MAGIC %md
# MAGIC ## 5. Mensaje clave
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

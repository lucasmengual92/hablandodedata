# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Permisos PROD
# MAGIC
# MAGIC Gobernanza de Datos en Unity Catalog
# MAGIC En Databricks, la seguridad y el acceso a los datos siguen una estructura jerárquica dentro de Unity Catalog:
# MAGIC
# MAGIC `Catalog → Schema → Table/View`
# MAGIC
# MAGIC Para que un grupo pueda consultar datos, es necesario otorgar permisos en cada uno de estos niveles.
# MAGIC
# MAGIC 1️⃣ Permiso sobre el Catálogo
# MAGIC
# MAGIC ```
# MAGIC GRANT USE CATALOG ON CATALOG hablando_de_data
# MAGIC TO finance_business_users_gl_prod;
# MAGIC ```
# MAGIC
# MAGIC Este permiso permite al grupo usar y visualizar el catálogo. Sin `USE CATALOG`, los usuarios no pueden ver ni navegar el catálogo, aunque tengan permisos sobre esquemas o tablas.
# MAGIC
# MAGIC 2️⃣ Permiso sobre el Esquema
# MAGIC
# MAGIC ```
# MAGIC GRANT USE SCHEMA ON SCHEMA hablando_de_data.default
# MAGIC TO finance_business_users_gl_prod;
# MAGIC ```
# MAGIC
# MAGIC Este permiso permite al grupo acceder al esquema específico dentro del catálogo. Sin `USE SCHEMA`, no es posible consultar tablas aunque exista permiso `SELECT`.
# MAGIC
# MAGIC 3️⃣ Permiso sobre las Tablas
# MAGIC
# MAGIC ```
# MAGIC GRANT SELECT ON hablando_de_data.default.budget_bronze
# MAGIC TO finance_business_users_gl_prod;
# MAGIC ```
# MAGIC
# MAGIC El permiso `SELECT` permite consultar los datos de la tabla.
# MAGIC Este es el nivel más granular de control de acceso.
# MAGIC
# MAGIC **Para que un usuario pueda consultar una tabla:**
# MAGIC - Debe tener USE CATALOG
# MAGIC - Debe tener USE SCHEMA
# MAGIC - Debe tener SELECT sobre la tabla
# MAGIC - Si falta alguno de estos niveles, el acceso no funcionará.
# MAGIC
# MAGIC La relación con Data Quality?
# MAGIC En el notebook anterior aseguramos la calidad del dato. En este paso aseguramos la gobernanza y el control de acceso, garantizando que:
# MAGIC - Solo los grupos autorizados puedan consumir la información.
# MAGIC - El acceso esté alineado con la arquitectura por capas (bronze, silver, curated).
# MAGIC - La seguridad siga el principio de mínimo privilegio.

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT USE CATALOG ON CATALOG hablando_de_data TO `finance_business_users_gl_prod`;
# MAGIC GRANT USE SCHEMA ON SCHEMA hablando_de_data.default TO `finance_business_users_gl_prod`;
# MAGIC GRANT SELECT ON hablando_de_data.default.budget_bronze TO `finance_business_users_gl_prod`;

# Lakeflow Jobs — Databricks Asset Bundles

Esta carpeta contiene un ejemplo sencillo de **Databricks Asset Bundles** para ejecutar un job en Databricks usando Lakeflow Jobs.

El objetivo es mostrar una estructura mínima para:

- definir un bundle
- crear un workflow
- ejecutar un notebook como job

---

# ¿Qué incluye?

### `databricks.yml`
Archivo principal de configuración del **bundle**.

Define el proyecto y qué recursos deben incluirse al desplegar el job.

---

### `workflow_analisis_nyctaxi.yml`

Define el **Lakeflow Job** que ejecuta el análisis.

Incluye:

- definición del job
- configuración del cluster
- task que ejecuta el notebook

---

### `analisis_nyctaxi.py`

Notebook de ejemplo que realiza un pequeño análisis usando el dataset público:

---

Más información en la [documentación oficial](https://docs.databricks.com/en/dev-tools/asset-bundles/index.html).

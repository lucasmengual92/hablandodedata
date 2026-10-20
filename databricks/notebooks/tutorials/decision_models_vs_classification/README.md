# Decision Models vs Classification — ¿nuevo hype o ML de siempre? 🧠

Demo de **Hablando De Data** en Databricks sobre la relación entre la clasificación clásica y los nuevos modelos de decisión.

## Qué incluye

- Notebook: [decision_models_vs_classification_demo.py](decision_models_vs_classification_demo.py)
- Clasificación de documentos sintéticos en español e inglés: **factura / contrato / incidencia**
- **ML clásico** con TF-IDF + Logistic Regression y `predict_proba()`
- **Databricks `ai_decide()`**, opcional: `choice`, `noul` y `score` en una consulta SQL
- Comparación de outputs, consideraciones de coste y checklist para producción

## Formato del notebook

El tutorial utiliza el formato **Databricks Source Notebook** (`.py`) con `# Databricks notebook source`, `# MAGIC %md`, `# DBTITLE` y `# COMMAND ----------`. Esto permite visualizar las celdas como un notebook en Databricks y revisar el código fácilmente en GitHub.

## Cómo ejecutarlo en Databricks

1. Conecta este repositorio desde **Workspace → Git folders → Add Git folder** con `https://github.com/lucasmengual92/hablandodedata` o importa directamente el notebook.
2. Abre `databricks/notebooks/tutorials/decision_models_vs_classification/decision_models_vs_classification_demo.py`.
3. Utiliza Python con `pandas` y `scikit-learn` (si no están instalados, añade una celda con `%pip install pandas scikit-learn`).
4. Ejecuta las celdas con **`RUN_AI_DECIDE = False`** (valor predeterminado). Esta parte funciona sin Spark, UC, credenciales ni llamadas a modelos.
5. Para probar Databricks **`ai_decide()`** cambia `RUN_AI_DECIDE = True`, verifica la disponibilidad en tu región/compute y ejecuta la celda opcional. **Puede generar coste.**

## Compatibilidad y límites

- `ai_decide()` está en **Beta**; necesita región/workspace compatible y Databricks Runtime **15.4 LTS+** (recomendado 18.2+). No es compatible con SQL Classic.
- La parte de ML usa un dataset **sintético, pequeño y equilibrado**. El holdout sirve para aprender, **no** para afirmar que un enfoque supera a otro.
- El notebook solo genera una **vista temporal de sesión** si se activa `ai_decide`; no crea tablas persistentes.
- Las probabilidades de `LogisticRegression` y el campo `confidence` de `ai_decide` **no son directamente comparables ni necesariamente calibrados**.
- Los umbrales de revisión humana son ejemplos didácticos.

## ¿Y Snowflake Decision?

El notebook no ejecuta Snowflake Decision: su propuesta mediante `AI_COMPLETE` requiere acceso a **Snowflake Private Preview**. La comparación con Snowflake se aborda a nivel conceptual en el artículo, no como benchmark ni integración cross-platform.

## Referencias oficiales

- [Databricks `ai_decide` — referencia SQL](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_decide)
- [Databricks — Introducing `ai_decide`](https://www.databricks.com/blog/introducing-aidecide-make-fast-decisions-your-governed-data)
- [Snowflake Decision — Private Preview](https://docs.snowflake.com/en/release-notes/2026/other/2026-10-07-ai-complete-snowflake-decision-preview)
- [Hablando De Data — Substack](https://hablandodedata.substack.com/)

> Material educativo: no utilizar para decisiones de producción sin evaluación, calibración, protección de datos y controles humanos adecuados.

# Databricks notebook source

# MAGIC %md
# MAGIC # 🤖 Decision Models vs Classification: ¿nuevo hype o ML de siempre?
# MAGIC
# MAGIC **Hablando De Data · Demo en Databricks**
# MAGIC
# MAGIC En este notebook clasificamos documentos de negocio sintéticos (`factura`, `contrato`, `incidencia`) con **ML clásico** y, opcionalmente, con **`ai_decide()` de Databricks**.
# MAGIC
# MAGIC El objetivo es comparar interfaces, entradas y salidas; **no** demostrar que una opción es más precisa, rápida o barata con solo unas pocas muestras.
# MAGIC
# MAGIC 📚 [Documentación oficial de ai_decide](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_decide) · [Hablando De Data](https://hablandodedata.substack.com/)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. Antes de empezar
# MAGIC
# MAGIC - Notebook Python, con `pandas` y `scikit-learn`. Si faltan, ejecuta `%pip install pandas scikit-learn` en una celda separada.
# MAGIC - La demo de ML funciona **sin Spark, Unity Catalog, credenciales o servicios AI**. Solo usa textos inventados.
# MAGIC - `ai_decide()` es opcional, está en **Beta** y requiere compute/región compatibles (DBR 15.4 LTS+; Databricks recomienda 18.2+). No está disponible en SQL Classic.
# MAGIC - El bloque opcional puede generar cargos por inferencia. Por defecto está desactivado.
# MAGIC - Ninguna de las puntuaciones de este tutorial está calibrada para uso en producción.

# COMMAND ----------

# DBTITLE 1,Configuración y librerías
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

SEED = 42
LABELS = ["factura", "contrato", "incidencia"]
RUN_AI_DECIDE = False      # Actívalo solo si tienes acceso y aceptas los costes.
REVIEW_THRESHOLD_ML = 0.60 # Threshold didáctico, no calibrado para producción.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Un dataset pequeño y sintético
# MAGIC
# MAGIC Con datos reales necesitarías muestras históricas, etiquetas validadas y un conjunto de test representativo. Aquí usamos frases deliberadamente simples para centrarnos en la arquitectura de decisión.

# COMMAND ----------

# DBTITLE 1,Dataset sintético: facturas, contratos e incidencias
examples = {
    "factura": [
        "Factura F-101. Cliente Acme. Importe 1200 EUR más IVA. Vencimiento a 30 días.",
        "Invoice INV-102: payment due for professional services, total 890 USD.",
        "Adjuntamos factura por compra de suministros: subtotal, impuestos e importe total.",
        "Nota de cargo con número de factura y datos bancarios para el pago.",
        "Resumen de facturación mensual, conceptos, descuentos e IVA correspondiente.",
        "Por favor revisa el importe de la factura emitida para este pedido.",
        "Factura proveedor 203: mantenimiento y vencimiento el 15 de noviembre.",
        "Supplier invoice includes unit price, tax code and outstanding balance.",
        "Solicitud de abono asociada a la factura anterior y nuevo total neto.",
        "Billing statement: invoice amount and bank account for transfer.",
        "Detalle de IVA, número fiscal, total a pagar y referencia de factura.",
        "Factura por equipos recibidos con plazo de pago a 60 días.",
    ],
    "contrato": [
        "Contrato de servicios firmado entre las partes con fecha de inicio y duración anual.",
        "Acuerdo de confidencialidad NDA con cláusulas de tratamiento de información.",
        "Service agreement specifying termination conditions and parties responsibilities.",
        "Anexo al contrato comercial con renovación automática y firma del proveedor.",
        "Las cláusulas establecen penalidades por incumplimiento y jurisdicción.",
        "Documento contractual: términos y condiciones de prestación, firmado digitalmente.",
        "Master services agreement MSA, scope of work and legal obligations.",
        "Contrato de licencia de software con derechos de uso y vigencia.",
        "Acuerdo marco de suministro con mecanismo de rescisión.",
        "Legal contract outlining liability, indemnification and effective date.",
        "Propuesta aceptada con firma, obligaciones mutuas y cláusula de confidencialidad.",
        "Adenda de renovación del contrato y modificación de términos comerciales.",
    ],
    "incidencia": [
        "Incidente crítico: API devuelve HTTP 500 desde esta mañana y bloquea pedidos.",
        "Ticket de soporte: no puede iniciar sesión por error de autenticación.",
        "Service outage detected. Application unavailable and requests time out.",
        "Bug report: el pipeline falla por permisos y requiere investigación.",
        "Alerta operativa por caída del servicio y errores en producción.",
        "El dashboard no carga. Error 503 en backend y usuarios afectados.",
        "Incidencia técnica por latencia elevada y reintentos constantes.",
        "Support issue: database connection refused after deployment.",
        "Fallo en la integración OAuth, token expirado y logs de excepción.",
        "Incident report: failed job, stack trace and missing dependency.",
        "Aplicación bloqueada por un error de servidor; solicitan soporte urgente.",
        "Ticket técnico por pipeline detenido y timeout en el cluster.",
    ],
}
records = [
    {"doc_id": f"{label[:3].upper()}-{i:02d}", "texto": text, "etiqueta": label}
    for label, texts in examples.items()
    for i, text in enumerate(texts, start=1)
]
df = pd.DataFrame(records)
print(f"Documentos sintéticos: {len(df)}")
print(df.groupby("etiqueta").size())
print(df.head(6).to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. ML clásico: TF-IDF + Logistic Regression
# MAGIC
# MAGIC Entrenamos un clasificador con muestras etiquetadas. `TfidfVectorizer` produce features; `LogisticRegression` devuelve la categoría y `predict_proba()`. Estas puntuaciones no garantizan acierto y requieren evaluación y calibración.

# COMMAND ----------

# DBTITLE 1,Entrenar Logistic Regression y evaluar
X_train, X_test, y_train, y_test = train_test_split(
    df["texto"], df["etiqueta"],
    test_size=0.25, stratify=df["etiqueta"], random_state=SEED
)
classic_model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode")),
    ("logreg", LogisticRegression(max_iter=1000, random_state=SEED)),
])
classic_model.fit(X_train, y_train)
pred_test = classic_model.predict(X_test)
print("Holdout ilustrativo de 9 textos (NO es un benchmark):")
print(classification_report(y_test, pred_test, labels=LABELS, zero_division=0))
print(pd.DataFrame(confusion_matrix(y_test, pred_test, labels=LABELS),
                   index=LABELS, columns=LABELS))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. La misma salida estructurada, sin LLM
# MAGIC
# MAGIC `decision`, `probabilities` y `needs_human_review` son valores que una aplicación puede utilizar directamente. El umbral es meramente didáctico.

# COMMAND ----------

# DBTITLE 1,Clasificar nuevos documentos con probabilidades
new_docs = pd.DataFrame([
    {"doc_id": "NEW-1", "texto": "Factura de servicios cloud: total a pagar y fecha de vencimiento."},
    {"doc_id": "NEW-2", "texto": "Acuerdo de confidencialidad firmado, obligaciones legales de ambas partes."},
    {"doc_id": "NEW-3", "texto": "El servicio de pagos no responde y hay errores HTTP 500 en producción."},
    {"doc_id": "NEW-4", "texto": "Revisa el documento del proveedor y dime si requiere atención."},
])
ml_probs = classic_model.predict_proba(new_docs["texto"])
ml_output = new_docs.copy()
ml_output["decision_ml"] = classic_model.predict(new_docs["texto"])
ml_output["max_score_ml"] = ml_probs.max(axis=1).round(3)
ml_output["probabilidades_ml"] = [
    {label: round(float(p), 3) for label, p in zip(classic_model.classes_, row)}
    for row in ml_probs
]
ml_output["revision_humana_ml"] = ml_output["max_score_ml"] < REVIEW_THRESHOLD_ML
print(ml_output[["doc_id","decision_ml","max_score_ml",
                 "revision_humana_ml","probabilidades_ml"]].to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Decision Model con `ai_decide()` (opcional)
# MAGIC
# MAGIC A diferencia del clasificador entrenado, aquí definimos **preguntas y criterios** sobre el texto. En una única llamada `ai_decide` evalúa:
# MAGIC
# MAGIC - `choice`: categoría y distribución entre etiquetas;
# MAGIC - `noul`: probabilidad de que exista una condición (así se llama el tipo en la API);
# MAGIC - `score`: valoración de urgencia en una escala ordenada.
# MAGIC
# MAGIC La función devuelve un `VARIANT` con `response.answers`, `metadata` y `error_message`. Su `confidence` no es equivalente a la probabilidad de éxito ni directamente comparable con `predict_proba`.

# COMMAND ----------

# DBTITLE 1,Preguntas para ai_decide: choice, noul y score
questions = {
    "tipo_documento": {
        "type": "choice",
        "instructions": "Clasifica el propósito principal del texto usando solo la información presente.",
        "criteria": {
            "factura": "Facturación, pago, IVA, cargos o importes a abonar.",
            "contrato": "Acuerdo, cláusulas, firmas o condiciones legales entre partes.",
            "incidencia": "Error, interrupción de servicio, bug o ticket de soporte.",
        },
    },
    "incidente_critico": {
        "type": "noul",
        "instructions": "¿Hay evidencia clara de un incidente técnico crítico que bloquea el servicio?",
    },
    "urgencia": {
        "type": "score",
        "instructions": "Valora la urgencia operativa sin inventar hechos.",
        "criteria": [
            "Sin urgencia operativa; trámite habitual",
            "Revisión pronta, pero sin bloqueo confirmado",
            "Urgencia alta: interrupción de servicio confirmada",
        ],
    },
}
print(json.dumps(questions, ensure_ascii=False, indent=2))

# COMMAND ----------

# DBTITLE 1,Llamada opcional a ai_decide en Databricks SQL
# Este bloque hace inferencias con coste. Por defecto no se ejecuta.
ai_decide_output = None
if RUN_AI_DECIDE:
    spark.createDataFrame(new_docs[["doc_id", "texto"]]).createOrReplaceTempView(
        "demo_decision_documents"
    )
    # La definición 'questions' debe ser constante dentro de la consulta SQL.
    questions_sql_literal = json.dumps(questions, ensure_ascii=False).replace("'", "''")
    sql = f"""
    SELECT doc_id,
           to_json(ai_decide(texto, '{questions_sql_literal}', map('version', '1.0'))) AS decision_json
    FROM demo_decision_documents
    ORDER BY doc_id
    """
    ai_decide_output = spark.sql(sql).toPandas()
    print(ai_decide_output.to_string(index=False))
else:
    print("ai_decide omitido. Cambia RUN_AI_DECIDE = True si tu workspace lo soporta.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Comparar salidas, no confundir probabilidades
# MAGIC
# MAGIC En esta demo solo comparamos la estructura: ¿qué categoría devuelve?, ¿qué puntuación?, ¿qué campos podemos utilizar en SQL o Python? No compares estos porcentajes como un benchmark A/B; para eso necesitamos un golden dataset y métricas consistentes.

# COMMAND ----------

# DBTITLE 1,Comparación de las salidas estructuradas
if ai_decide_output is not None:
    parsed = []
    for row in ai_decide_output.itertuples(index=False):
        data = json.loads(row.decision_json) if row.decision_json else {}
        answers = (data.get("response") or {}).get("answers") or {}
        choice = answers.get("tipo_documento") or {}
        parsed.append({
            "doc_id": row.doc_id,
            "decision_ai": choice.get("choice"),
            "confidence_ai": choice.get("confidence"),
            "probabilidades_ai": choice.get("probabilities"),
            "p_incidente_critico": (answers.get("incidente_critico") or {}).get("probability"),
            "score_urgencia": (answers.get("urgencia") or {}).get("score"),
            "error_ai": data.get("error_message"),
        })
    comparison = ml_output[["doc_id", "decision_ml", "max_score_ml"]].merge(
        pd.DataFrame(parsed), on="doc_id", how="left"
    )
    print(comparison.to_string(index=False))
else:
    print("Tabla comparativa opcional omitida.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. ¿Qué cambia de verdad?
# MAGIC
# MAGIC | | ML clásico | Decision Model (`ai_decide`) |
# MAGIC |---|---|---|
# MAGIC | Input | Features derivadas de datos históricos | Estado/contexto como texto o `VARIANT` |
# MAGIC | Setup | Ejemplos etiquetados + entrenamiento | Preguntas y criterios en SQL |
# MAGIC | Output | Clase + `predict_proba` | `choice`, `noul`, `score`, distribución |
# MAGIC | Beneficio | Eficiente y controlable con datos representativos | Interfaz flexible sobre contexto variado |
# MAGIC | Trade-offs | Drift, etiquetas y calibración | Coste por inferencia, disponibilidad, validación |
# MAGIC
# MAGIC **Importante:** Snowflake Decision mediante `AI_COMPLETE` es una propuesta relacionada, pero no se ejecuta en este notebook de Databricks. No estamos demostrando superioridad de ningún proveedor.
# MAGIC
# MAGIC [Snowflake Decision (Private Preview)](https://docs.snowflake.com/en/release-notes/2026/other/2026-10-07-ai-complete-snowflake-decision-preview)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Checklist para producción
# MAGIC
# MAGIC 1. Construir un **golden dataset** con ground truth acordado.
# MAGIC 2. Medir precisión por clase, latencia, coste, estabilidad y human review rate.
# MAGIC 3. Comprobar calibración y umbrales según el coste del error.
# MAGIC 4. Proteger PII; observar drift, cambios de prompts/criterios y fallos.
# MAGIC 5. Definir fallback cuando `ai_decide` no esté disponible o devuelva `error_message`.
# MAGIC
# MAGIC **Mi take 👀**: clasificar y puntuar no es nuevo. Lo novedoso es una interfaz de decisión estructurada sobre contexto abierto, accesible desde SQL y aplicaciones. Si tienes features y etiquetas de calidad, evalúa primero ML clásico; si necesitas comprensión de contexto heterogéneo, prueba un Decision Model **con métricas reales**.
# MAGIC
# MAGIC [Hablando De Data](https://hablandodedata.substack.com/) · [Repositorio GitHub](https://github.com/lucasmengual92/hablandodedata)

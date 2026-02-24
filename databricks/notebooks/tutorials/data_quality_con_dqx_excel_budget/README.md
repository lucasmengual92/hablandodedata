# 📊 Data Quality con DQX sobre Excel de Presupuesto

Este repositorio demuestra cómo aplicar **Data Quality de forma
estandarizada** sobre un Excel financiero utilizando **Databricks + DQX
(Data Quality Framework)**.

La idea no es solo validar datos.\
Es mostrar cómo llevar un Excel real de negocio a un pipeline gobernado,
reproducible y listo para producción.

------------------------------------------------------------------------

## 🎯 Objetivo

Muchos equipos siguen recibiendo información crítica en formato Excel.\
El problema no es Excel.\
El problema es cómo lo integramos al Data Platform.

Este ejemplo muestra cómo:

-   Leer un `.xlsx` directamente en Spark\
-   Limpiar y estandarizar columnas\
-   Aplicar reglas de calidad desacopladas en YAML\
-   Separar datos válidos (Silver) de datos rechazados (Quarantine)\
-   Mantener trazabilidad y gobernanza

------------------------------------------------------------------------

## 🧱 Arquitectura simplificada

    Excel (Finance_Budget_Q1_2026.xlsx)
            ↓
    Spark Read
            ↓
    Transformaciones básicas
            ↓
    DQX (reglas en YAML)
            ↓
    Silver Table   +   Quarantine Table

------------------------------------------------------------------------

## 📂 Estructura del proyecto

    databricks/
     └── notebooks/tutorials/
          └── data_quality_con_dqx_excel_budget/
               ├── Finance_Budget_Q1_2026.xlsx
               ├── tutorial_dqx_excel_budget.py
               ├── budget_dqx_rules.yml
               └── README.md

------------------------------------------------------------------------

## ⚙️ Qué se demuestra

### ✅ 1. Lectura de Excel realista

Carga directa del archivo financiero usando Spark.

------------------------------------------------------------------------

### ✅ 2. Limpieza de columnas

Estandarización de nombres y tipos de datos para asegurar consistencia.

------------------------------------------------------------------------

### ✅ 3. Reglas desacopladas en YAML

Las reglas no viven en el código.\
Viven en configuración.

Ejemplo conceptual:

``` yaml
rules:
  - name: amount_not_null
    column: amount
    expectation: not_null

  - name: department_valid
    column: department
    expectation: in_set
    values: ["Finance", "HR", "IT"]
```

Esto permite:

-   Versionado de reglas\
-   Cambios sin modificar código\
-   Reutilización entre pipelines

------------------------------------------------------------------------

### ✅ 4. Separación Silver / Quarantine

Los datos se dividen en:

-   ✔️ Válidos → Silver\
-   ❌ Inválidos → Quarantine

Esto habilita:

-   Observabilidad\
-   Auditoría\
-   Reprocesamiento controlado

------------------------------------------------------------------------

## 🚀 Cómo ejecutarlo

1.  Subir el repositorio a tu workspace de Databricks.\
2.  Abrir `tutorial_dqx_excel_budget.py`.\
3.  Ejecutar el notebook paso a paso.\
4.  Revisar resultados en Silver y Quarantine.

------------------------------------------------------------------------

## 🧠 ¿Por qué importa?

Porque la calidad de datos no es un check técnico.\
Es una decisión de arquitectura.

Este repo es ideal para:

-   Demos\
-   Workshops\
-   Webinars\
-   Equipos que están profesionalizando su Data Platform\
-   Casos donde Excel sigue siendo el input real del negocio

------------------------------------------------------------------------

## 🔎 Enfoque

Este proyecto sigue principios que promueve **Hablando de Data**:

-   Gobernanza práctica\
-   Data Quality como estándar, no parche\
-   Arquitectura simple pero profesional\
-   Reglas desacopladas\
-   Separación clara entre lógica y validación

------------------------------------------------------------------------

## 🤝 Contribuciones

Si querés extender el ejemplo:

-   Agregar más reglas\
-   Incorporar métricas de observabilidad\
-   Integrarlo con Jobs o Workflows\
-   Adaptarlo a otros dominios (ventas, HR, supply)

Pull requests son bienvenidos.

------------------------------------------------------------------------

## 📬 Sobre Hablando de Data

Contenido práctico sobre:

-   Databricks\
-   Data Engineering\
-   Analytics Engineering\
-   Gobernanza\
-   Data Quality real en producción

👉 https://hablandodedata.substack.com

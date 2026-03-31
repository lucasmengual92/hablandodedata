# Tutorial End-to-End de AutoCDC

## Dejá de Codear a Mano Pipelines de Change Data Capture

Este tutorial muestra **AutoCDC**, una feature de Databricks que automatiza pipelines de Change Data Capture (CDC) y Slowly Changing Dimensions (SCD), sin necesidad de código complejo hecho a mano.

### 📚 Qué vas a aprender

- **Fundamentos de AutoCDC**: Entender cómo AutoCDC automatiza patrones CDC de forma declarativa
- **SCD Type 1**: Actualizar registros automáticamente con los últimos valores (sobreescribir cambios)
- **Arquitectura Medallion**: Construir pipelines de datos production-grade (Bronze → Silver → Gold)
- **Beneficios de performance**: Ver mejoras de performance del mundo real (hasta 2x mejor price-performance)

### 🎯 ¿Por qué AutoCDC?

Los pipelines CDC y SCD tradicionales son:
- **Frágiles**: Se rompen fácil cuando cambia el schema de origen
- **Complejos**: Requieren lógica custom extensa para operaciones de merge
- **Caros**: Overhead de codeo manual y mantenimiento a escala

**AutoCDC resuelve esto** con sintaxis declarativa que maneja automáticamente:
- Evolución de schema y cambios de tipos de datos
- Procesamiento incremental con semántica exactly-once
- Tracking histórico con versionado automático
- Operaciones de merge optimizadas

### 🚀 Qué hay adentro

Este tutorial incluye:

1. **Notebook Interactivo** (`AutoCDC_Tutorial.ipynb`)
   - Ejemplo simplificado, hands-on con datos de muestra de Delta Shared
   - Celdas de código completas listas para correr
   - Explicaciones paso a paso
   - Sigue la arquitectura Medallion (Bronze → Silver → Gold)

2. **Datasets de Muestra**
   - **Origen**: Usa el catálogo de muestras públicas de Delta Shared (`samples.tpch`)
   - **Destino**: Tu schema `hablando_de_data.default`
   - Funciona en cualquier workspace de Databricks
   - Sin setup complejo requerido

### 📋 Requisitos

- Workspace de Databricks (cualquier edición)
- Databricks Runtime 14.3 LTS o superior
- Acceso a muestras de Delta Shared (disponible por defecto)
- Catálogo `hablando_de_data` (el tutorial lo va a usar para las tablas de salida)

### 🏃 Cómo empezar

1. Abrí `AutoCDC_Tutorial.ipynb` en tu workspace de Databricks
2. Conectalo a un cluster (o usá serverless compute)
3. Ejecutá las celdas secuencialmente para ver AutoCDC en acción
4. Todas las tablas de salida se van a crear en el schema `hablando_de_data.default`

### 📖 Recursos relacionados

- [Blog Post Oficial](https://www.databricks.com/blog/stop-hand-coding-change-data-capture-pipelines): Stop Hand-Coding Change Data Capture Pipelines
- [Documentación de AutoCDC](https://docs.databricks.com/delta-live-tables/auto-cdc.html)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/index.html)
- [Arquitectura Medallion](https://www.databricks.com/glossary/medallion-architecture)

### 🎨 Arquitectura

Este tutorial simplificado sigue la **Arquitectura Medallion**:

```
Bronze (Raw)              →  Silver (Cleaned)       →  Gold (Aggregated)
├─ Datos CDC crudos          ├─ SCD Type 1             ├─ Métricas de negocio
└─ samples.tpch.customer     └─ Estado latest cliente  └─ Balance por segmento
   ↓                            ↓                         ↓
   hablando_de_data.default.   hablando_de_data.default. hablando_de_data.default.
   bronze_customer_cdc         silver_customer_scd1      gold_customer_balance_summary
```

### 💡 Conceptos clave

**SCD Type 1**: Solo últimos valores (foco de este tutorial)
- Sobreescribe registros existentes
- No trackea historia
- Ideal para correcciones o dimensiones no críticas
- Implementación simple con AutoCDC

**SCD Type 2**: Trackeo completo de historia (mencionado en el tutorial)
- Crea nuevas versiones para cambios
- Preserva todos los estados históricos
- ¡Solo cambiás un parámetro en AutoCDC!

**Snapshot CDC**: Derivar cambios desde snapshots
- Compara snapshots actuales vs. previos
- Identifica automáticamente inserts, updates, deletes
- Genial para sistemas sin CDC nativo

### 📊 Mejoras de performance

Basado en workloads de producción, AutoCDC entrega:
- **Hasta 2x mejor** price-performance para SCD Type 1
- **Hasta 2x mejor** price-performance para SCD Type 2
- Optimización y paralelización automática
- Overhead de mantenimiento reducido

### 🗂️ Estructura del tutorial

El notebook está simplificado para enfocarse en conceptos core:
1. **Setup**: Conectar a muestras de Delta Shared y catálogo `hablando_de_data`
2. **Capa Bronze**: Simular eventos CDC desde datos de customer
3. **Capa Silver**: Aplicar SCD Type 1 (implementación manual para mostrar qué hace AutoCDC)
4. **Capa Gold**: Crear métricas de negocio
5. **Código de Producción**: Ejemplo completo de pipeline DLT con AutoCDC

### 🤝 Contribuir

Este tutorial acompaña un blog post detallado en Substack. ¡Sentite libre de adaptar y compartir!

### 📝 Licencia

Este tutorial se proporciona as-is con fines educativos.

---

**Autor**: Creado para demostrar capacidades de AutoCDC
**Última actualización**: Marzo 2026

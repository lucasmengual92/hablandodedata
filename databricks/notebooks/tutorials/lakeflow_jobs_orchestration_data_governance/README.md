# 🔐 Gobernanza y Permisos en Unity Catalog (Lakeflow + Jobs)

Este módulo demuestra cómo implementar **gobernanza de datos real en
producción** usando **Unity Catalog en Databricks**, aplicando permisos
de forma jerárquica y controlada.

Forma parte de la serie práctica de *Hablando de Data* sobre:

-   Orquestación con Jobs
-   Data Quality
-   Gobernanza aplicada
-   Seguridad alineada a arquitectura Bronze / Silver / Curated

------------------------------------------------------------------------

## 🎯 Objetivo

En Unity Catalog, el acceso a los datos sigue una estructura jerárquica:

Catalog → Schema → Table / View

Para que un usuario pueda consultar una tabla correctamente, debe tener
permisos en cada uno de esos niveles.

Este ejemplo muestra cómo:

-   Otorgar `USE CATALOG`
-   Otorgar `USE SCHEMA`
-   Otorgar `SELECT`
-   Aplicar principio de mínimo privilegio
-   Alinear permisos a dominios de negocio

------------------------------------------------------------------------

## 🧱 Qué se demuestra

### 1️⃣ Permiso sobre el Catálogo

``` sql
GRANT USE CATALOG ON CATALOG hablando_de_data
TO `finance_business_users_gl_prod`;
```

Sin este permiso, el usuario no puede ni siquiera visualizar el
catálogo.

------------------------------------------------------------------------

### 2️⃣ Permiso sobre el Schema

``` sql
GRANT USE SCHEMA ON SCHEMA hablando_de_data.default
TO `finance_business_users_gl_prod`;
```

Permite acceder al esquema dentro del catálogo.

Sin `USE SCHEMA`, no se pueden consultar tablas aunque exista `SELECT`.

------------------------------------------------------------------------

### 3️⃣ Permiso sobre la Tabla

``` sql
GRANT SELECT ON hablando_de_data.default.budget_bronze
TO `finance_business_users_gl_prod`;
```

Este es el nivel más granular de control.

------------------------------------------------------------------------

## 🛑 Regla Clave

Para que un usuario pueda consultar una tabla necesita:

-   ✔️ USE CATALOG\
-   ✔️ USE SCHEMA\
-   ✔️ SELECT

Si falta uno de estos niveles, el acceso no funcionará.

------------------------------------------------------------------------

## 🏗 Enfoque Arquitectónico

Este módulo se alinea con:

-   Separación por capas (Bronze / Silver / Curated)
-   Permisos por dominio
-   Seguridad basada en grupos (no usuarios individuales)
-   Gobierno reproducible vía código (Infrastructure as Code mindset)

------------------------------------------------------------------------

## 🚀 Casos de uso reales

Este patrón es clave cuando:

-   Migrás de Hive Metastore a Unity Catalog
-   Profesionalizás tu Data Platform
-   Querés evitar accesos directos a Bronze
-   Necesitás trazabilidad y control en producción

------------------------------------------------------------------------

## 🧠 Filosofía

La gobernanza no es burocracia. Es arquitectura aplicada.

Los permisos bien diseñados evitan:

-   Accesos accidentales
-   Costos innecesarios
-   Dependencias frágiles
-   Problemas de auditoría



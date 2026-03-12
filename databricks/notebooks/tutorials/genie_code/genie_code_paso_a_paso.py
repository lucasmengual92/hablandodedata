# Databricks notebook source
# MAGIC %md
# MAGIC # 🤖 Genie Code en Databricks
# MAGIC
# MAGIC En este tutorial vamos a probar **Genie Code**, el nuevo agente de AI dentro de Databricks.
# MAGIC
# MAGIC La idea no es simplemente ver una demo bonita.
# MAGIC
# MAGIC La idea es probar algo más realista:
# MAGIC
# MAGIC - explorar un dataset real del catálogo `samples`
# MAGIC - generar insights
# MAGIC - pedir un modelo de ML
# MAGIC - comparar enfoques
# MAGIC - entender por qué **Instructions** puede ser una de las partes más potentes de Genie Code
# MAGIC
# MAGIC Si vienes de trabajar con notebooks, pipelines y bastante código repetitivo...
# MAGIC probablemente aquí haya algo interesante.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Qué vas a probar en este notebook
# MAGIC
# MAGIC Durante este walkthrough vamos a pedirle a Genie Code que:
# MAGIC
# MAGIC 1. Explore una tabla de ejemplo
# MAGIC 2. Genere insights con visualizaciones
# MAGIC 3. Cree un modelo de ML
# MAGIC 4. Compare ese modelo con otro enfoque
# MAGIC 5. Respete instrucciones o convenciones definidas por nosotros
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC Dataset principal usado en este ejemplo:
# MAGIC
# MAGIC ```sql
# MAGIC samples.wanderbricks.properties
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1️⃣ Abre Genie Code
# MAGIC
# MAGIC Desde este notebook, abre **Genie Code** desde el botón en la parte superior derecha.
# MAGIC
# MAGIC La gracia de Genie Code no es solo que escriba código.
# MAGIC
# MAGIC Lo interesante es que:
# MAGIC
# MAGIC - entiende el contexto del notebook
# MAGIC - puede navegar entre assets
# MAGIC - no pierde el hilo fácilmente
# MAGIC - y además puede seguir convenciones definidas por ti o por tu organización

# COMMAND ----------

# MAGIC %md
# MAGIC ![Genie Code Intro](../../../../src/media/08_genie_code_intro.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2️⃣ Carga rápida del dataset
# MAGIC
# MAGIC Antes de empezar con Genie Code, cargamos la tabla para confirmar que todo está accesible desde este workspace.

# COMMAND ----------

df = spark.table("samples.wanderbricks.properties")
display(df.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3️⃣ Primer prompt: explorar datos
# MAGIC
# MAGIC Copia este prompt en Genie Code:
# MAGIC
# MAGIC ```
# MAGIC Give me 4 insights about the @samples.wanderbricks.properties table and visualize them
# MAGIC ```
# MAGIC
# MAGIC Si quieres ser más explícito, también puedes probar:
# MAGIC
# MAGIC ```
# MAGIC Give me 4 useful business insights about the @samples.wanderbricks.properties table
# MAGIC and include visualizations
# MAGIC ```
# MAGIC
# MAGIC **Importante**: Fijense como agrego el caracter `@` para definir los assets
# MAGIC como una tabla por ejemplo, asi Genie entiende el contexto de tus datos.
# MAGIC
# MAGIC ### Qué deberías observar
# MAGIC
# MAGIC Genie Code normalmente:
# MAGIC
# MAGIC - lee el schema
# MAGIC - inspecciona columnas y tipos
# MAGIC - toma algunos samples
# MAGIC - genera un plan
# MAGIC - y luego propone celdas nuevas en el notebook
# MAGIC
# MAGIC No te quedes solo con el resultado final.
# MAGIC
# MAGIC Fíjate también en **cómo estructura el trabajo**.

# COMMAND ----------

# MAGIC %md
# MAGIC ![Genie Insights](../../../../src/media/09_genie_code_insights.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4️⃣ Un ejemplo simple de insight
# MAGIC
# MAGIC Genie Code probablemente te genere algo parecido a esto:
# MAGIC
# MAGIC - distribución por tipo de propiedad
# MAGIC - nuevas propiedades por categoría
# MAGIC - distribución de precios
# MAGIC - comparaciones entre segmentos
# MAGIC
# MAGIC Este bloque es solo una referencia mínima para que el notebook también tenga algo ejecutable sin depender del agente.

# COMMAND ----------

# DBTITLE 1,Insight 1 - Distribution of properties
import matplotlib.pyplot as plt
import pandas as pd

# Display a boxplot for base_price to see outliers and spread
price_pd = df.select('base_price').toPandas()
plt.figure(figsize=(7, 3))
plt.boxplot(price_pd['base_price'].dropna(), vert=False)
plt.title('Distribution of Property Base Price')
plt.xlabel('Base Price')
plt.show()

# COMMAND ----------

# DBTITLE 1,Insight 2 - Avg price by property type
display(
    df.groupBy("property_type")
      .avg("base_price")
      .orderBy("avg(base_price)", ascending=False)
)

# COMMAND ----------

# DBTITLE 1,Insight 3 - Most common max_guests
# Most common max_guests values
display(
    df.groupBy('max_guests')
     .count()
     .orderBy('count', ascending=False)
)

# COMMAND ----------

# DBTITLE 1,Insight 4 - Avg price vs. bedrooms
# Average base price by number of bedrooms
display(
    df.groupBy('bedrooms')
      .avg('base_price')
      .orderBy('bedrooms')
)

# COMMAND ----------

# MAGIC %md
# MAGIC ![Genie MLflow](../../../../src/media/10_genie_code_ml.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5️⃣ Segundo prompt: entrenar un modelo
# MAGIC
# MAGIC Ahora probá esto en Genie Code:
# MAGIC
# MAGIC ```
# MAGIC Train an scikit-learn model to predict property price using 
# MAGIC the @samples.wanderbricks.properties table
# MAGIC ```
# MAGIC
# MAGIC ### Qué mirar acá
# MAGIC
# MAGIC Lo interesante no es solo que entrene algo.
# MAGIC
# MAGIC Lo interesante es ver si:
# MAGIC
# MAGIC - hace una selección razonable de features
# MAGIC - organiza el código con claridad
# MAGIC - registra el resultado en MLflow (no me lo hizo a la 1ra)
# MAGIC - y deja algo suficientemente limpio como para seguir trabajando después

# COMMAND ----------

# DBTITLE 1,Scikit-learn price prediction (RandomForest)
# Scikit-learn price prediction (RandomForest)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Prepare the dataframe
features = ['bedrooms','bathrooms','max_guests','property_type']
df_pd = df.select(['base_price'] + features).dropna().toPandas()

# One-hot encode property_type
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
onehot = encoder.fit_transform(df_pd[['property_type']])
encoded_types = encoder.get_feature_names_out(['property_type'])
df_encoded = pd.DataFrame(onehot, columns=encoded_types)
df_pd = pd.concat([df_pd.reset_index(drop=True), df_encoded], axis=1)

# Define X/y
X = df_pd.drop(['base_price','property_type'], axis=1)
y = df_pd['base_price']

# Standardize numeric columns
scaler = StandardScaler()
X[['bedrooms','bathrooms','max_guests']] = scaler.fit_transform(X[['bedrooms','bathrooms','max_guests']])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)

# Display evaluation metrics
mse = mean_squared_error(y_test, preds)
r2 = r2_score(y_test, preds)
print(f"RandomForest MSE: {mse:.2f}, R2: {r2:.2f}")

# COMMAND ----------

# DBTITLE 1,Plot feature importances
# Show feature importances from RandomForest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Use model and X from previous cell
def plot_top_feature_importances(model, X, top_n=10):
    importances = model.feature_importances_
    feat_names = X.columns
    sorted_idx = np.argsort(importances)[::-1][:top_n]
    plt.figure(figsize=(8, 3))
    plt.barh(feat_names[sorted_idx], importances[sorted_idx])
    plt.xlabel('Importance')
    plt.title(f'Top {top_n} Feature Importances (RandomForest)')
    plt.gca().invert_yaxis()
    plt.show()

plot_top_feature_importances(model, X, top_n=10)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6️⃣ Instructions: probablemente la parte más underrated
# MAGIC
# MAGIC Genie Code también permite definir **Instructions**.
# MAGIC
# MAGIC Y acá es donde la cosa se pone realmente interesante para equipos de datos.
# MAGIC
# MAGIC Por ejemplo, empeza haciendo clic en el icono ⚙️ arriba de Genie Code que te llevará a la vista de Settings, y ahora clic en la opción **"Open Instructions file"** (si es tu 1ra vez, te lo creará por defecto), y ahora le vas a poder indicar que:
# MAGIC
# MAGIC - siga arquitectura medallion
# MAGIC - use siempre MLflow
# MAGIC - mantenga ciertos estándares de visualización
# MAGIC - respete convenciones internas de nombres
# MAGIC
# MAGIC Esto significa que el agente no solo genera código.
# MAGIC
# MAGIC También puede **alinearse con cómo trabaja tu equipo**.

# COMMAND ----------

# MAGIC %md
# MAGIC ![Genie Instructions](../../../../src/media/11_genie_code_instructions.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7️⃣ Prompt bonus: empujar Genie Code un poco más
# MAGIC
# MAGIC Si querés ir un paso más allá, probá alguno de estos prompts:
# MAGIC
# MAGIC ### Opción A — pipeline
# MAGIC
# MAGIC ```
# MAGIC Create a medallion architecture pipeline from the samples.wanderbricks.properties dataset
# MAGIC ```
# MAGIC
# MAGIC ### Opción B — dashboard
# MAGIC
# MAGIC ```
# MAGIC Create a dashboard with 5 visualizations from the outputs of this analysis
# MAGIC ```
# MAGIC
# MAGIC ### Opción C — feature engineering
# MAGIC
# MAGIC ```
# MAGIC Create a feature table for a property price prediction model
# MAGIC ```
# MAGIC
# MAGIC Acá ya entrás en una zona donde Genie Code puede empezar a mostrar si realmente entiende el flujo de trabajo de datos... o si solo está improvisando bonito.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8️⃣ Qué mirar críticamente mientras lo probás
# MAGIC
# MAGIC No todo debería aceptarse sin revisar.
# MAGIC
# MAGIC Cuando pruebes Genie Code, fíjate en:
# MAGIC
# MAGIC - si los joins tienen sentido
# MAGIC - si las agregaciones son razonables
# MAGIC - si las features elegidas están bien
# MAGIC - si el código es mantenible
# MAGIC - y si realmente está respetando las instrucciones
# MAGIC
# MAGIC Genie Code puede acelerar bastante.
# MAGIC
# MAGIC Pero sigue siendo responsabilidad tuya decidir si el resultado merece quedarse en el repo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧠 Conclusión
# MAGIC
# MAGIC Después de probar Genie Code, mi impresión es bastante simple:
# MAGIC
# MAGIC No reemplaza a los data engineers, data scientists, o otros.
# MAGIC
# MAGIC Pero sí puede quitar bastante fricción en tareas como:
# MAGIC
# MAGIC - exploración inicial
# MAGIC - código repetitivo
# MAGIC - comparación rápida de enfoques
# MAGIC - primeros borradores de pipelines o análisis
# MAGIC
# MAGIC Lo más potente, al menos por ahora, no es que “escribe código”.
# MAGIC
# MAGIC Lo más potente es que empieza a **trabajar dentro del contexto del Lakehouse**.
# MAGIC
# MAGIC Y eso cambia bastante el juego.

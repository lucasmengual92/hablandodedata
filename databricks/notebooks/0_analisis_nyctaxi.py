# Análisis básico del dataset 'samples.nyctaxi.trips'

# COMMAND ----------
# Cargar el dataset de ejemplo
df = spark.read.table("samples.nyctaxi.trips")

# Mostrar las primeras filas
display(df.limit(10))

# COMMAND ----------
# Descripción del esquema
df.printSchema()

# COMMAND ----------
# Estadísticas descriptivas de las columnas principales
columnas = [
    "trip_distance",
    "fare_amount",
    "pickup_zip",
    "dropoff_zip"
]

df.select(columnas).describe().show()

# COMMAND ----------
# Distribución de la distancia de viaje
import matplotlib.pyplot as plt

distancias = df.select("trip_distance").rdd.flatMap(lambda x: x).collect()
plt.hist(distancias, bins=50, color='skyblue', edgecolor='black')
plt.title("Distribución de la distancia de viaje (millas)")
plt.xlabel("Distancia")
plt.ylabel("Cantidad de viajes")
plt.show()

# COMMAND ----------
# Viajes por código postal de pickup
pickup_counts = (
    df.groupBy("pickup_zip")
    .count()
    .orderBy("count", ascending=False)
)
display(pickup_counts)

# COMMAND ----------
# Conclusiones
print("Personaliza este notebook para tus propios experimentos!")
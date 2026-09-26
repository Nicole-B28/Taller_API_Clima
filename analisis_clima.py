# ============================================================
# TALLER: CONTESTANDO PREGUNTAS SOBRE LOS DATOS
# ANÁLISIS DE DATOS METEOROLÓGICOS
# Fuente: Open-Meteo Historical Weather API
# Periodo: Agosto de 2026
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTAR LIBRERÍAS
# ------------------------------------------------------------

import requests
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ------------------------------------------------------------
# 2. URL DE LA API DE OPEN-METEO
# ------------------------------------------------------------

url = "https://archive-api.open-meteo.com/v1/archive?latitude=0.3442&longitude=-78.1213&start_date=2026-08-01&end_date=2026-08-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone=auto"


# ------------------------------------------------------------
# 3. CONSULTAR LA API
# ------------------------------------------------------------

print("Consultando datos de Open-Meteo...")

respuesta = requests.get(
    url,
    timeout=30
)

print(
    "Código de respuesta HTTP:",
    respuesta.status_code
)

# Si existe un error en la consulta,
# Python detendrá el programa aquí.
respuesta.raise_for_status()


# ------------------------------------------------------------
# 4. CONVERTIR LA RESPUESTA JSON
# ------------------------------------------------------------

datos = respuesta.json()

datos_diarios = datos["daily"]

tabla = pd.DataFrame(datos_diarios)


# ------------------------------------------------------------
# 5. CAMBIAR LOS NOMBRES DE LAS COLUMNAS
# ------------------------------------------------------------

tabla = tabla.rename(
    columns={
        "time": "fecha",
        "temperature_2m_mean": "temperatura_media",
        "temperature_2m_max": "temperatura_maxima",
        "temperature_2m_min": "temperatura_minima",
        "precipitation_sum": "precipitacion",
        "wind_speed_10m_max": "viento_maximo"
    }
)


# ------------------------------------------------------------
# 6. CONVERTIR LA COLUMNA FECHA
# ------------------------------------------------------------

tabla["fecha"] = pd.to_datetime(
    tabla["fecha"]
)


# ------------------------------------------------------------
# 7. MOSTRAR LOS DATOS
# ------------------------------------------------------------

print("\nDATOS OBTENIDOS:")
print(tabla)


# ------------------------------------------------------------
# 8. IDENTIFICAR LA CARPETA DEL PROYECTO
# ------------------------------------------------------------

carpeta = Path(__file__).parent


# ------------------------------------------------------------
# 9. CREAR CARPETAS PARA GRÁFICAS Y RESULTADOS
# ------------------------------------------------------------

carpeta_graficas = carpeta / "graficas"

carpeta_resultados = carpeta / "resultados"

carpeta_graficas.mkdir(
    exist_ok=True
)

carpeta_resultados.mkdir(
    exist_ok=True
)


# ------------------------------------------------------------
# 10. GUARDAR LOS DATOS EN UN ARCHIVO CSV
# ------------------------------------------------------------

archivo_csv = (
    carpeta / "datos_clima_agosto_2026.csv"
)

tabla.to_csv(
    archivo_csv,
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nArchivo CSV guardado correctamente."
)


# ============================================================
# PREGUNTA 1
# ¿QUÉ DÍA PRESENTÓ LA MAYOR AMPLITUD TÉRMICA?
# ============================================================

# La amplitud térmica es la diferencia entre
# la temperatura máxima y la temperatura mínima.

tabla["amplitud_termica"] = (
    tabla["temperatura_maxima"]
    - tabla["temperatura_minima"]
)

dia_mayor_amplitud = tabla.loc[
    tabla["amplitud_termica"].idxmax()
]


print("\n========================================")
print("PREGUNTA 1")
print("========================================")

print(
    "¿Qué día de agosto presentó "
    "la mayor amplitud térmica?"
)

print(
    "Fecha:",
    dia_mayor_amplitud["fecha"].strftime(
        "%Y-%m-%d"
    )
)

print(
    "Temperatura máxima:",
    dia_mayor_amplitud[
        "temperatura_maxima"
    ],
    "°C"
)

print(
    "Temperatura mínima:",
    dia_mayor_amplitud[
        "temperatura_minima"
    ],
    "°C"
)

print(
    "Amplitud térmica:",
    round(
        dia_mayor_amplitud[
            "amplitud_termica"
        ],
        2
    ),
    "°C"
)


# ============================================================
# PREGUNTA 2
# ¿QUÉ SEMANA REGISTRÓ LA TEMPERATURA PROMEDIO MÁS ALTA?
# ============================================================

# Primero obtenemos el número del día del mes.

tabla["dia_mes"] = (
    tabla["fecha"].dt.day
)


# Después dividimos agosto en periodos:
#
# Semana 1 = días 1 al 7
# Semana 2 = días 8 al 14
# Semana 3 = días 15 al 21
# Semana 4 = días 22 al 28
# Semana 5 = días 29 al 31

tabla["semana_agosto"] = (
    (tabla["dia_mes"] - 1) // 7
) + 1


# Agrupamos los datos por semana
# y calculamos la temperatura media.

temperatura_semanal = (
    tabla
    .groupby("semana_agosto")[
        "temperatura_media"
    ]
    .mean()
)


semana_mas_calida = (
    temperatura_semanal.idxmax()
)

temperatura_semana_mas_calida = (
    temperatura_semanal.max()
)


print("\n========================================")
print("PREGUNTA 2")
print("========================================")

print(
    "¿Qué semana de agosto registró "
    "la temperatura promedio más alta?"
)

print(
    "Semana:",
    semana_mas_calida
)

print(
    "Temperatura promedio:",
    round(
        temperatura_semana_mas_calida,
        2
    ),
    "°C"
)


# ============================================================
# PREGUNTA 3
# ¿LOS DÍAS CON LLUVIA TUVIERON UNA TEMPERATURA
# PROMEDIO DIFERENTE A LOS DÍAS SIN LLUVIA?
# ============================================================

# Días con precipitación mayor que cero.

dias_con_lluvia = tabla[
    tabla["precipitacion"] > 0
]


# Días sin precipitación.

dias_sin_lluvia = tabla[
    tabla["precipitacion"] == 0
]


# Promedio de temperatura
# de los días con lluvia.

temperatura_con_lluvia = (
    dias_con_lluvia[
        "temperatura_media"
    ].mean()
)


# Promedio de temperatura
# de los días sin lluvia.

temperatura_sin_lluvia = (
    dias_sin_lluvia[
        "temperatura_media"
    ].mean()
)


# Diferencia entre ambos grupos.

diferencia_temperatura = (
    temperatura_con_lluvia
    - temperatura_sin_lluvia
)


print("\n========================================")
print("PREGUNTA 3")
print("========================================")

print(
    "¿Los días con lluvia tuvieron "
    "una temperatura promedio diferente "
    "a los días sin lluvia?"
)

print(
    "Temperatura promedio "
    "en días con lluvia:",
    round(
        temperatura_con_lluvia,
        2
    ),
    "°C"
)

print(
    "Temperatura promedio "
    "en días sin lluvia:",
    round(
        temperatura_sin_lluvia,
        2
    ),
    "°C"
)

print(
    "Diferencia:",
    round(
        diferencia_temperatura,
        2
    ),
    "°C"
)


# ============================================================
# PREGUNTA 4
# ¿EXISTE RELACIÓN ENTRE LA PRECIPITACIÓN
# Y LA VELOCIDAD MÁXIMA DEL VIENTO?
# ============================================================

# Calculamos la correlación de Pearson.

correlacion = (
    tabla["precipitacion"]
    .corr(
        tabla["viento_maximo"]
    )
)


print("\n========================================")
print("PREGUNTA 4")
print("========================================")

print(
    "¿Existe relación entre la "
    "precipitación y la velocidad "
    "máxima del viento?"
)

print(
    "Correlación de Pearson:",
    round(
        correlacion,
        3
    )
)


# Identificamos si la relación
# es positiva o negativa.

if correlacion > 0:
    direccion_correlacion = "positiva"

elif correlacion < 0:
    direccion_correlacion = "negativa"

else:
    direccion_correlacion = "nula"


print(
    "Dirección de la relación:",
    direccion_correlacion
)

print(
    "Importante: correlación "
    "no significa causalidad."
)


# ============================================================
# GRÁFICA 1
# TEMPERATURA PROMEDIO DIARIA
# Tipo: GRÁFICA DE LÍNEAS
# ============================================================

# Utilizamos una línea porque queremos observar
# cómo cambia una variable a través del tiempo.

plt.figure(
    figsize=(11, 6)
)

plt.plot(
    tabla["fecha"],
    tabla["temperatura_media"],
    marker="o"
)

plt.title(
    "Temperatura promedio diaria - Agosto 2026"
)

plt.xlabel(
    "Fecha"
)

plt.ylabel(
    "Temperatura promedio (°C)"
)

plt.grid(
    alpha=0.3
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    carpeta_graficas
    / "01_temperatura_promedio.png",
    dpi=300
)

plt.close()


# ============================================================
# GRÁFICA 2
# AMPLITUD TÉRMICA DIARIA
# Tipo: GRÁFICA DE BARRAS
# ============================================================

# Utilizamos barras porque queremos comparar
# la amplitud térmica entre diferentes días.

plt.figure(
    figsize=(11, 6)
)

plt.bar(
    tabla["fecha"],
    tabla["amplitud_termica"]
)

plt.title(
    "Amplitud térmica diaria - Agosto 2026"
)

plt.xlabel(
    "Fecha"
)

plt.ylabel(
    "Amplitud térmica (°C)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    carpeta_graficas
    / "02_amplitud_termica.png",
    dpi=300
)

plt.close()


# ============================================================
# GRÁFICA 3
# TEMPERATURA PROMEDIO POR SEMANA
# Tipo: GRÁFICA DE BARRAS
# ============================================================

# Usamos barras porque estamos comparando
# grupos o categorías: las semanas.

plt.figure(
    figsize=(8, 6)
)

plt.bar(
    temperatura_semanal.index,
    temperatura_semanal.values
)

plt.title(
    "Temperatura promedio por semana - Agosto 2026"
)

plt.xlabel(
    "Semana de agosto"
)

plt.ylabel(
    "Temperatura promedio (°C)"
)

plt.xticks(
    temperatura_semanal.index
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    carpeta_graficas
    / "03_temperatura_semanal.png",
    dpi=300
)

plt.close()


# ============================================================
# GRÁFICA 4
# TEMPERATURA DE DÍAS CON LLUVIA VS. SIN LLUVIA
# Tipo: GRÁFICA DE BARRAS
# ============================================================

# Tenemos dos categorías:
# con lluvia y sin lluvia.

categorias = [
    "Con lluvia",
    "Sin lluvia"
]

temperaturas = [
    temperatura_con_lluvia,
    temperatura_sin_lluvia
]


plt.figure(
    figsize=(8, 6)
)

plt.bar(
    categorias,
    temperaturas
)

plt.title(
    "Temperatura promedio: días con lluvia vs. sin lluvia"
)

plt.xlabel(
    "Tipo de día"
)

plt.ylabel(
    "Temperatura promedio (°C)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    carpeta_graficas
    / "04_lluvia_temperatura.png",
    dpi=300
)

plt.close()


# ============================================================
# GRÁFICA 5
# PRECIPITACIÓN VS. VELOCIDAD MÁXIMA DEL VIENTO
# Tipo: GRÁFICA DE DISPERSIÓN
# ============================================================

# Utilizamos scatter porque queremos analizar
# la relación entre dos variables numéricas.

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    tabla["precipitacion"],
    tabla["viento_maximo"]
)

plt.title(
    "Precipitación vs. velocidad máxima del viento"
)

plt.xlabel(
    "Precipitación (mm)"
)

plt.ylabel(
    "Velocidad máxima del viento (km/h)"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    carpeta_graficas
    / "05_precipitacion_viento.png",
    dpi=300
)

plt.close()


# ============================================================
# GUARDAR LOS RESULTADOS EN UN ARCHIVO DE TEXTO
# ============================================================

resumen = f"""
ANÁLISIS METEOROLÓGICO
PERIODO: AGOSTO DE 2026


PREGUNTA 1
¿Qué día presentó la mayor amplitud térmica?

Fecha:
{dia_mayor_amplitud["fecha"].strftime("%Y-%m-%d")}

Temperatura máxima:
{dia_mayor_amplitud["temperatura_maxima"]:.2f} °C

Temperatura mínima:
{dia_mayor_amplitud["temperatura_minima"]:.2f} °C

Amplitud térmica:
{dia_mayor_amplitud["amplitud_termica"]:.2f} °C


PREGUNTA 2
¿Qué semana registró la temperatura promedio más alta?

Semana:
{semana_mas_calida}

Temperatura promedio:
{temperatura_semana_mas_calida:.2f} °C


PREGUNTA 3
¿Los días con lluvia tuvieron una temperatura promedio
diferente a los días sin lluvia?

Temperatura promedio con lluvia:
{temperatura_con_lluvia:.2f} °C

Temperatura promedio sin lluvia:
{temperatura_sin_lluvia:.2f} °C

Diferencia:
{diferencia_temperatura:.2f} °C


PREGUNTA 4
¿Existe relación entre la precipitación
y la velocidad máxima del viento?

Correlación de Pearson:
{correlacion:.3f}

Dirección de la relación:
{direccion_correlacion}

La correlación representa una asociación estadística
y no implica causalidad.
"""


archivo_resumen = (
    carpeta_resultados
    / "resumen_resultados.txt"
)


with open(
    archivo_resumen,
    "w",
    encoding="utf-8"
) as archivo:
    archivo.write(
        resumen
    )


# ============================================================
# MENSAJE FINAL
# ============================================================

print("\n========================================")
print("ANÁLISIS TERMINADO CORRECTAMENTE")
print("========================================")

print(
    "\nSe generaron las cinco gráficas "
    "en la carpeta 'graficas'."
)

print(
    "Los resultados fueron guardados "
    "en la carpeta 'resultados'."
)

print(
    "Los datos fueron guardados "
    "en el archivo CSV."
)

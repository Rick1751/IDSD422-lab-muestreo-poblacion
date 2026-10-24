# clasificacion_variables.py — Parte A: clasificación de las variables de clientes.csv.
#
# El archivo data/clientes.csv tiene 12 clientes y 7 variables (más el id).
# El objetivo: clasificar cada variable (numérica continua/discreta, categórica
# binaria/ordinal/nominal) y verificar la clasificación en código.
#
# Regla del capítulo 3: el dtype es una pista, no la clasificación — el criterio
# (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?) decide.
#
# Uso (desde la raíz del repositorio):  python scripts/clasificacion_variables.py

import pandas as pd

clientes = pd.read_csv("data/clientes.csv")

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas")
print()
print("Primeras filas:")
print(clientes.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (dtype) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
print("Tipos inferidos (dtype):")
print(clientes.dtypes)
print()

# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
print("Valores únicos por columna (antes de ordenar categorías):")
for columna in clientes.columns:
    print(f"  {columna}: {clientes[columna].nunique()} valores -> "
          f"{clientes[columna].unique().tolist()}")
print()

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# Una ordinal se guarda como texto (o como número) y su orden natural se pierde:
# alfabéticamente "Posgrado" iría antes que "Primaria", que no tiene sentido.
#
niveles_educacion = ["Primaria", "Secundaria", "Universidad", "Posgrado"]
tipo_educacion = pd.CategoricalDtype(
    categories=niveles_educacion, ordered=True
)
clientes["nivel_educacion"] = clientes["nivel_educacion"].astype(tipo_educacion)

niveles_satisfaccion = [
    int(nivel) for nivel in sorted(clientes["satisfaccion"].unique())
]
tipo_satisfaccion = pd.CategoricalDtype(
    categories=niveles_satisfaccion, ordered=True
)
clientes["satisfaccion"] = clientes["satisfaccion"].astype(tipo_satisfaccion)

print("Orden declarado para nivel_educacion:")
print(f"  niveles: {niveles_educacion}")
print(f"  mínimo: {clientes['nivel_educacion'].min()}")
print(f"  máximo: {clientes['nivel_educacion'].max()}")
print(f"  dtype: {clientes['nivel_educacion'].dtype}")
print("Orden declarado para satisfaccion:")
print(f"  niveles: {niveles_satisfaccion}")
print(f"  mínimo: {clientes['satisfaccion'].min()}")
print(f"  máximo: {clientes['satisfaccion'].max()}")
print(f"  dtype: {clientes['satisfaccion'].dtype}")
print()

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
# cliente_id: nominal, porque identifica clientes y no tiene orden ni promedio.
# edad: discreta en estos datos, porque se registra en años enteros; la mitad
#       de un año no es una categoría observada para esta variable.
# numero_hijos: discreta, porque es un conteo entero y no tiene sentido contar
#               una fracción de hijo.
# genero: nominal, porque sus categorías no tienen un orden natural.
# nivel_educacion: ordinal, porque sus categorías sí tienen un orden educativo.
# ciudad: nominal, porque las ciudades son nombres sin jerarquía.
# ingresos_mensuales: continua, porque el ingreso puede tomar valores con
#                      centavos y tiene sentido comparar promedios.
# satisfaccion: ordinal, aunque llegue como número; sus valores ordenan niveles
#               de satisfacción, pero 4 no significa el doble que 2.
clasificacion = {
    "cliente_id": "categórica nominal",
    "edad": "numérica discreta",
    "numero_hijos": "numérica discreta",
    "genero": "categórica nominal",
    "nivel_educacion": "categórica ordinal",
    "ciudad": "categórica nominal",
    "ingresos_mensuales": "numérica continua",
    "satisfaccion": "categórica ordinal",
}
print("Resumen de la clasificación (para el informe):")
for variable, tipo in clasificacion.items():
    print(f"  {variable:20s} {tipo}")

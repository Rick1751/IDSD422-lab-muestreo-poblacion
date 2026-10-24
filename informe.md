# Informe — Clasificación de variables y población vs. muestra

**Para:** Gerencia de RetailAndina S.A. · **De:** Equipo de Business Intelligence
**Fecha:** ___/___/2026 · **Asunto:** Base de fidelización: tipos de variables y estimación por muestreo

---

## Resumen ejecutivo

Clasifiqué las variables de la base de clientes según fueran nominales, ordinales, discretas o continuas, usando el orden de las categorías y el sentido de las fracciones como criterios. Después estimé el ingreso mensual promedio mediante muestras de conveniencia, aleatoria simple y estratificada, comparándolas con el parámetro poblacional de 1330.72 USD. Observé que una muestra de 20 filas podía tener sesgo si se seleccionaba por conveniencia, mientras que el sorteo aleatorio presentaba variabilidad. Recomendé elegir el diseño de muestreo antes que confiar solamente en el tamaño de la muestra.

## Parte A — Clasificación de las variables

*Completa la tabla usando el **criterio** (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?), no el ejemplo. En «verificación» anota qué mostró el código: dtype, número de valores únicos y, si declaraste el orden, cómo lo comprobaste.*

| Variable | Tipo | Justificación (criterio) | Verificación en código |
|---|---|---|---|
| `cliente_id` | Categórica nominal | Identifiqué a cada cliente con una etiqueta. No tenía sentido promediar una identificación ni existía un orden entre sus valores. | El dtype fue `str` y observé 12 valores únicos: C001 a C012. |
| `edad` | Numérica discreta en estos datos | La registré en años enteros, por lo que no observé fracciones en esta base. Aunque la edad puede medirse continuamente en el tiempo, para esta variable registrada en años no tenía sentido usar la mitad como categoría observada. | El dtype fue `int64` y observé 12 valores únicos: 34, 27, 41, 22, 36, 29, 48, 33, 25, 39, 31 y 45. |
| `numero_hijos` | Numérica discreta | Fue un conteo entero: no tenía sentido contar una fracción de hijo. | El dtype fue `int64` y observé 5 valores únicos: 0, 1, 2, 3 y 4. |
| `genero` | Categórica nominal | Sus categorías no tenían un orden natural, por lo que solo tenía sentido diferenciarlas y contarlas. | El dtype fue `str` y observé 3 valores únicos: Femenino, Masculino y Otro. |
| `nivel_educacion` | Categórica ordinal | Sus categorías sí tenían un orden educativo: Primaria, Secundaria, Universidad y Posgrado. No interpreté la distancia entre niveles como una cantidad numérica. | El dtype inicial fue `str` y observé 4 valores únicos. Declaré el orden `[Primaria, Secundaria, Universidad, Posgrado]`; el dtype quedó como `category`, con mínimo Primaria y máximo Posgrado. |
| `ciudad` | Categórica nominal | Las ciudades eran categorías sin una jerarquía natural entre ellas. | El dtype fue `str` y observé 3 valores únicos: Quito, Guayaquil y Cuenca. |
| `ingresos_mensuales` | Numérica continua | Aunque en el archivo aparecía sin decimales, el ingreso podía expresarse con centavos; por eso tenía sentido considerar valores fraccionarios y calcular promedios. | El dtype fue `int64` y observé 12 valores únicos: 1450, 980, 2200, 760, 1150, 1350, 890, 1680, 840, 2450, 1210 y 1070. |
| `satisfaccion` | Categórica ordinal | Llegó como número, pero sus valores representaban niveles ordenados de satisfacción. El 4 no significaba el doble de satisfacción que el 2, así que no la traté como una cantidad continua. | El dtype inicial fue `int64` y observé 4 valores únicos: 4, 3, 5 y 2. Declaré el orden `[2, 3, 4, 5]`; el dtype quedó como `category`, con mínimo 2 y máximo 5. |

**P1.** El dtype de `satisfaccion` fue `int64`, porque sus valores estaban escritos como números enteros. Ese dtype no bastó para clasificarla: el significado de los valores indicó que era una escala ordinal, no una medida en la que 4 fuera el doble de 2. Si una variable ordinal queda como texto sin declarar el orden, el programa no conoce su jerarquía natural y puede ordenar las categorías alfabéticamente o impedir comparaciones correctas. Por eso declaré explícitamente el `CategoricalDtype` ordenado.

## Parte B — Población vs. muestra

### La población y su parámetro

| Concepto | Valor |
|---|---|
| Población (N) | 400 clientes |
| Variable de interés | `ingresos_mensuales` |
| Parámetro poblacional (media) | 1330.72 USD |

Muestreé para simular la situación habitual en la que no se tiene acceso a todos los clientes o calcular el parámetro completo resulta costoso. En este laboratorio sí pude calcular la media poblacional porque la base completa estaba disponible, y la utilicé como referencia para evaluar las estimaciones de las muestras.

### Los tres diseños

*Corre tu script y registra las salidas. La composición por ciudad es la que delata el sesgo: anótala tal como salió.*

| Diseño | n | Media estimada | Composición por ciudad | Diferencia vs. parámetro |
|---|---|---|---|---|
| Conveniencia (`head`) | 20 | 1348.50 USD | `{'Quito': 20}` | +17.78 USD |
| Aleatorio simple (`sample`) | 20 | 1336.00 USD | `{'Cuenca': 8, 'Quito': 8, 'Guayaquil': 4}` | +5.28 USD |
| Estratificado (`groupby` + 5 %) | 20 | 1287.50 USD | `{'Quito': 10, 'Guayaquil': 6, 'Cuenca': 4}` | -43.22 USD |

*Anota también las medias de 5 sorteos distintos del aleatorio simple (semillas 1 a 5):*

| Semilla | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Media | 1336.00 USD | 1405.00 USD | 1235.00 USD | 1491.50 USD | 1288.00 USD |

**P2.** El parámetro poblacional fue 1330.72 USD. La muestra por conveniencia estimó 1348.50 USD, la aleatoria simple estimó 1336.00 USD y la estratificada estimó 1287.50 USD. En esta ejecución, la aleatoria simple quedó más cerca, con una diferencia de +5.28 USD. Sin embargo, un solo resultado no bastó para declarar un ganador general: otra selección aleatoria podía producir otra media, como mostraron las semillas 1 a 5.

**P3.** La muestra por conveniencia tuvo 20 filas, pero todas fueron de Quito: su composición fue `{'Quito': 20}`. Esto mostró un sesgo de selección sistemático, porque `head(20)` dependió del orden del archivo y dejó fuera a Guayaquil y Cuenca. Tomar más filas no corrigió necesariamente el problema si seguía tomando las primeras filas; habría sido necesario cambiar el diseño de selección.

**P4.** El sorteo aleatorio produjo medias distintas: 1336.00, 1405.00, 1235.00, 1491.50 y 1288.00 USD para las semillas 1 a 5. Esa variabilidad indicó que una sola muestra podía sobreestimar o subestimar el parámetro. Por ello, una empresa debía reconocer la incertidumbre del sorteo y no interpretar una única media como una verdad exacta.

**P5.** Usaría la conveniencia para un piloto exploratorio, cuando necesitara una primera aproximación rápida y aceptara su falta de representatividad. Usaría el aleatorio simple para una conclusión sobre toda la población cuando cada cliente tuviera la misma probabilidad de ser seleccionado. Usaría el estratificado cuando necesitara asegurar la presencia de subgrupos, como las ciudades, conservando la proporción observada de Quito, Guayaquil y Cuenca. En conjunto, concluí que el diseño decidió la representatividad, no solamente el tamaño de 20 filas.

## Conclusiones

1. Aprendí que dos muestras del mismo tamaño podían comportarse de manera diferente: la muestra de conveniencia tuvo 20 clientes, pero reunió a los 20 de Quito y produjo una media de 1348.50 USD, mientras que el aleatorio simple representó las tres ciudades y produjo 1336.00 USD.
2. La media poblacional fue 1330.72 USD, pero las medias aleatorias cambiaron entre 1235.00 y 1491.50 USD en las cinco semillas. Esto distinguió el sesgo sistemático de la conveniencia de la variabilidad propia del sorteo.
3. Recomendé a la gerencia definir primero el diseño según el objetivo: aleatorio simple para una conclusión general y estratificado cuando fuera importante representar subgrupos. El tamaño de la muestra por sí solo no garantizó representatividad; el diseño decidió la calidad de la estimación.
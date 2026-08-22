# Informe Final — Análisis de Ventas E-commerce

## 1. Resumen ejecutivo

Este informe recoge los resultados del análisis exploratorio, estadístico y
de visualización realizado sobre un dataset de comercio electrónico de
52.000 pedidos (2022-2025), procedentes de la unión de dos fuentes: datos
de clientes y datos de ventas/productos.

El hallazgo central del proyecto es que **la mayoría de las variables
categóricas disponibles no explican el comportamiento real de compra o
devolución de los clientes**, mientras que una minoría de variables —
principalmente relacionadas con el producto (margen por categoría) y con
el propio historial de compra del cliente (frecuencia vs. ticket) — sí
revelan diferencias relevantes.

## 2. Metodología

| Fase | Descripción |
|---|---|
| Carga e integración | Unión de `clientes.csv` y `ventas.xlsx` (5 hojas: productos + 4 años de pedidos) por claves comunes (`id_cliente`, `product_id`). |
| Limpieza y transformación | Corrección de tipos, normalización de texto, imputación de nulos (mediana en numéricas, moda en categóricas), eliminación de duplicados, detección y tratamiento de outliers (winsorizing). |
| Análisis exploratorio (EDA) | Análisis univariante y bivariante organizado en 5 bloques temáticos: General, Clientes, Productos, Canales/Operaciones, Temporal. |
| Contraste de hipótesis | Verificación estadística formal de los hallazgos del EDA, siguiendo el flujo normalidad → homocedasticidad → nº de grupos → test (t-test, Mann-Whitney, ANOVA+Tukey, Kruskal-Wallis, Chi-cuadrado, correlación/regresión). |
| Visualización | Dashboard interactivo en Power BI con modelo de datos en estrella (tabla de hechos `pedidos` + dimensiones `clientes`, `productos`, `Dim_Fecha`). |

## 3. Hallazgos por bloque

### 3.1 Clientes

- La distribución de gasto total por cliente está sesgada a la derecha: la
  mayoría gasta entre 300 € y 1.000 €, con una cola de clientes de alto
  valor hasta ~2.700 €.
- Frecuencia de compra y gasto total no siempre van de la mano: existen
  clientes de alta frecuencia y ticket bajo, y clientes de baja frecuencia
  con ticket alto que acumulan más gasto total.
- **`segmento_cliente` no refleja el comportamiento real**: el gasto medio
  apenas varía entre segmentos (671 €-689 €), confirmado estadísticamente
  con ANOVA (p = 0,93, sin diferencia significativa). Casos concretos lo
  ilustran: el cliente de mayor gasto está etiquetado "recurrente", no
  "vip"; varios clientes "nuevo" figuran entre los de mayor frecuencia.
- `ciudad` tampoco diferencia el gasto individual (661 €-697 €); las
  diferencias en gasto total agregado por ciudad se deben al número de
  clientes por zona, no a mayor gasto per cápita.

### 3.2 Productos

- Los productos más vendidos no son homogéneos: unos generan ventas altas
  por volumen con margen bajo, otros alcanzan ventas similares con menos
  unidades pero mayor margen.
- Las 5 categorías de producto generan un volumen de ventas muy similar
  (1,06-1,10 millones €), pero el margen medio varía notablemente:
  **electrónica es la categoría menos rentable (14,72 €)** frente a
  **hogar, la más rentable (29,29 €)** — diferencia confirmada con
  Kruskal-Wallis a nivel pedido (H = 1034,11; p = 1,45 × 10⁻²²²).
- La marca sí diferencia el volumen de ventas (a diferencia de la
  categoría): *vantia* lidera con un volumen ~3 veces superior a las
  marcas más bajas del top 10.

### 3.3 Canales y operaciones

- Web genera la mayor facturación total, pero por concentrar más pedidos,
  no por un ticket medio superior: la mediana de importe es prácticamente
  idéntica entre los 4 canales (71-74 €), confirmado con Kruskal-Wallis
  (p = 0,40).
- Contrario a lo esperado en comercio electrónico, el envío gratuito no
  está asociado a un mayor importe de compra (p = 0,96).
- La tasa de devolución global (5,88 %) se mantiene prácticamente constante
  frente a categoría de producto, canal, método de pago y envío gratuito —
  ninguna de estas variables la explica con claridad (todos los contrastes
  con p > 0,05).

### 3.4 Análisis temporal

- Las ventas se mantienen relativamente estables entre 2022 y 2025
  (variación total de solo un 3,2 % entre el año más bajo y el más alto),
  sin tendencia clara de crecimiento o decrecimiento.
- Se observa una estacionalidad moderada: febrero es sistemáticamente el
  mes más débil y marzo el más fuerte, explicada por el volumen de
  pedidos y no por el ticket medio (estable todo el año, 101-106 €).
- No se detectan picos en periodos comerciales típicos del retail
  (campañas navideñas, rebajas de verano).

## 4. Resumen del contraste estadístico (Fase 4)

| Pregunta | Test | p-valor | Resultado |
|---|---|---|---|
| Gasto ~ Segmento cliente | Kruskal-Wallis | 0,496 | Sin diferencia |
| Ventas ~ Canal | Kruskal-Wallis | 0,402 | Sin diferencia |
| Ventas ~ Envío gratis | Mann-Whitney | 0,957 | Sin diferencia |
| Margen ~ Categoría (nivel producto, n=90) | Kruskal-Wallis | 0,115 | Sin diferencia (poca potencia) |
| **Margen ~ Categoría (nivel pedido, n=52.000)** | Kruskal-Wallis | **1,45e-222** | **Diferencia significativa** |
| Gasto ~ Ciudad | Kruskal-Wallis | 0,533 | Sin diferencia |
| Devolución ~ Categoría | Chi-cuadrado | 0,620 | Sin relación |
| Gasto ~ Ingresos anuales | Correlación/regresión | 0,714 | Sin relación |

El caso del margen (nivel producto vs. nivel pedido) ilustra un principio
metodológico relevante: el mismo patrón real puede resultar "no
significativo" o "extremadamente significativo" según el tamaño de muestra
disponible en el nivel de análisis elegido. Antes de descartar un efecto,
es necesario verificar que la muestra tiene potencia estadística suficiente
para detectarlo.

## 5. Dashboard

El dashboard interactivo (`dashboard/proyecto_ecommerce.pbix`) traduce
estos hallazgos en 4 páginas:

- **Resumen** — KPIs globales (ventas, pedidos, ticket medio, tasa de
  devolución, margen medio) y evolución temporal (año y mes).
- **Clientes** — gasto por segmento, ciudad y tramo de edad; relación
  entre frecuencia de compra y ticket medio; top de clientes por gasto,
  con formato condicional que señala las incoherencias del segmento
  declarado.
- **Productos** — ventas vs. margen por categoría; ventas por marca;
  top 5 y bottom 5 productos con nombre, margen y tasa de devolución.
- **Canales y Operaciones** — volumen vs. ticket medio por canal; tasa
  de devolución por canal y método de pago; distribución de método de
  pago.

Todas las páginas incluyen filtros interactivos (año, canal, categoría,
marca, segmento, tramo de edad) que permiten explorar los hallazgos de
forma dinámica.

## 6. Limitaciones

- El análisis se limita a la información disponible en el dataset y no
  incorpora factores externos (campañas de marketing, competencia,
  eventos puntuales).
- La devolución no puede explicarse con las variables disponibles, lo que
  sugiere que su causa depende de factores no capturados (motivo
  declarado, calidad física del producto, experiencia postventa).
- Algunas variables presentan un pequeño porcentaje de valores no
  informados ("desconocido" en método de pago y marca), excluidos de las
  interpretaciones de negocio.
- Los resultados de normalidad (Shapiro-Wilk) deben interpretarse con
  cautela en las métricas de mayor tamaño muestral, dado que este test es
  muy sensible al tamaño de muestra.

## 7. Recomendaciones

1. **Revisar el criterio de asignación de `segmento_cliente`**, ya que no
   refleja el comportamiento de gasto real observado — puede estar
   basado en un criterio (p. ej. antigüedad) que no captura el valor real
   del cliente.
2. **Investigar la menor rentabilidad de la categoría electrónica**: pese
   a generar un volumen de ventas similar al resto, su margen es
   significativamente inferior — conviene revisar la estructura de costes
   o precios de esta categoría.
3. **Ampliar la captura de datos sobre devoluciones** (motivo declarado,
   estado del producto devuelto), dado que ninguna variable actual la
   explica.
4. **Explorar una segmentación de clientes basada en comportamiento real**
   (tipo RFM: recencia, frecuencia, valor monetario) como alternativa al
   segmento declarado actual.

## 8. Conclusión

El proyecto demuestra que, en este dataset, el comportamiento de compra,
gasto y devolución de los clientes no se explica por la mayoría de las
variables categóricas y demográficas disponibles. Este resultado, obtenido
mediante análisis descriptivo y confirmado con rigor estadístico, es en sí
mismo un hallazgo de negocio valioso: señala que el criterio de
segmentación actual de la empresa no captura diferencias reales de
comportamiento, y redirige la atención hacia las dos áreas donde sí se
detectaron diferencias significativas — la rentabilidad por categoría de
producto y la relación entre frecuencia de compra y valor del ticket.

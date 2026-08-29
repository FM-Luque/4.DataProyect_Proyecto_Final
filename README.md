# 4.DataProyect_Proyecto_Final

# Análisis de Ventas E-commerce: Exploración, Contraste Estadístico y Dashboard

## Descripción

Este proyecto realiza un análisis exploratorio y estadístico de los pedidos,
clientes y productos de un comercio electrónico entre 2022 y 2025. El
objetivo es identificar qué variables explican realmente el comportamiento
de compra, gasto y devolución de los clientes, y traducir esos hallazgos en
un dashboard operativo para la toma de decisiones.

El análisis combina limpieza y transformación profunda de datos, análisis
descriptivo (EDA), contraste de hipótesis (tests estadísticos: t-test,
Mann-Whitney, ANOVA+Tukey, Kruskal-Wallis, Chi-cuadrado, correlación/
regresión) y visualización interactiva en Power BI.

## Estructura del Proyecto

```
├── data/
│   ├── raw/                          # Datos originales, sin modificar
│   │   ├── clientes.csv
│   │   └── ventas.xlsx               # 5 hojas: productos + 2022/2023/2024/2025
│   └── processed/
│       ├── 01_datos_integrados.csv   # Fase 1: fuentes unidas
│       ├── 02_datos_limpios.csv      # Fase 2: limpio y transformado (52.000 x 39)
│       ├── pedidos.csv               # Exportado para Power BI
│       ├── clientes.csv              # Tabla agregada a nivel cliente
│       └── productos.csv             # Tabla agregada a nivel producto
├── notebooks/
│   ├── 00_exploracion_consultas.ipynb     # Exploración preliminar (no es entregable)
│   ├── 01_carga_integración.ipynb         # Fase 1: carga y unión de fuentes
│   ├── 02_limpieza_transformacion.ipynb   # Fase 2: limpieza y transformación
│   ├── 03_eda.ipynb                       # Fase 3: análisis exploratorio
│   └── 04_abtest.ipynb                    # Fase 4: contraste de hipótesis
├── src/
│   ├── sp_carga_integracion.py       # Funciones de exploración (Fase 1)
│   ├── sp_limpieza_trasfromacion.py  # Sin funciones activas (ver nota)
│   ├── sp_eda.py                     # Funciones de visualización y EDA
│   └── sp_abtest.py                  # Funciones de tests estadísticos
├── dashboard/
│   └── proyecto_ecommerce.pbix       # Dashboard interactivo Power BI
├── informe/
│   └── Informe.md              # Informe explicativo del análisis
├── .gitignore
└── README.md
```

> **Nota:** `sp_limpieza_trasfromacion.py` se planteó inicialmente para las
> funciones de limpieza de Fase 2, pero se decidió mantenerlas dentro del
> propio notebook (`02_limpieza_transformacion.ipynb`), al ser pasos
> específicos de un proceso lineal, no funciones reutilizables entre
> distintos análisis (a diferencia de `sp_eda.py` o `sp_abtest.py`).

## Instalación y Requisitos

Este proyecto usa Python 3.11+ y requiere las siguientes librerías:

```
pandas
numpy
matplotlib
seaborn
scipy
statsmodels
```

Instalación:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

Para el dashboard: **Power BI Desktop** (gratuito, disponible para Windows).

## Resultados y Conclusiones

**Fuentes de datos:** dos fuentes independientes — `clientes.csv` (datos
demográficos y de comportamiento) y `ventas.xlsx` (catálogo de productos +
pedidos de 4 años) — unidas en Fase 1, dando lugar a un dataset final de
**52.000 filas y 39 columnas**.

**Hallazgos principales:**

- **La mayoría de variables categóricas no diferencian el comportamiento
  real de compra.** Segmento de cliente, ciudad, canal y método de pago
  muestran gasto medio, ticket medio y tasa de devolución prácticamente
  idénticos entre sus categorías — confirmado tanto visualmente en el EDA
  como estadísticamente en el A/B testing (p > 0,05 en todos los casos).
- **`segmento_cliente` no refleja el gasto real del cliente**: el cliente
  con mayor gasto total del dataset está etiquetado como "recurrente", no
  como "vip", y varios clientes "nuevo" figuran entre los de mayor
  frecuencia de compra.
- **El margen sí varía de forma significativa por categoría de producto**,
  pese a que las ventas son similares entre categorías: electrónica es la
  menos rentable (14,72 € de margen medio) frente a hogar (29,29 €) — el
  único hallazgo del proyecto con diferencia estadísticamente significativa
  (Kruskal-Wallis, p < 0,001 a nivel pedido).
- **La devolución (5,88 % global) no se explica por ninguna variable
  disponible** en el dataset (categoría, canal, método de pago, envío
  gratis, mes del año).
- **El canal determina volumen de pedidos, no valor del ticket**: web
  genera más facturación total por concentrar más pedidos, no porque cada
  compra individual sea mayor (ticket medio prácticamente igual en los 4
  canales).

**Dashboard:** 4 páginas interactivas (Resumen, Clientes, Productos,
Canales y Operaciones) que permiten explorar estos hallazgos filtrando por
año, canal, categoría, marca, segmento y tramo de edad.

Informe completo del análisis disponible en [`informe/informe_final.md`](informe/informe_final.md).

## Próximos Pasos

- Investigar el criterio real de asignación de `segmento_cliente`, dado que
  no refleja el comportamiento de gasto observado.
- Incorporar variables adicionales sobre el motivo de devolución, para
  explicar la tasa de devolución que las variables actuales no predicen.
- Aplicar segmentación de clientes basada en comportamiento real (RFM) en
  lugar de la etiqueta declarada actual.
- Ampliar el dashboard con una página de análisis temporal detallado
  (estacionalidad mensual, comparativa año a año).

## Contribuciones

Proyecto individual desarrollado como Proyecto Final del programa. No se
aceptan contribuciones externas por el momento.

## Autores

- *Francisco Miguel Luque Gonzalez .*
- *Enlace a GitHub: [github.com/FM-Luque/4.DataProyect_Proyecto_Final.git](https://github.com/FM-Luque/4.DataProyect_Proyecto_Final.git)*

"""
sp_eda.py
===================
Caja de herramientas de Fase 3 — Análisis Descriptivo y Visualización (EDA).

Sigue el flujo: Pre-EDA -> Univariante -> Bivariante -> Global.
Solo contenido descriptivo (nada de tests de hipótesis / p-valores:
eso vive en sp_abtest_completo.py, Fase 4).

  exploracion()               -> vista rápida: sample, info, describe, nulos, duplicados
  comprobar_claves()          -> duplicados y valores únicos de columnas clave
  eda()                       -> EDA rápido automático (tipos, estadísticas, countplots,
                                  histogramas y boxplots de TODAS las columnas a la vez)
  matriz_correlacion()        -> heatmap de correlaciones + tabla de pares más correlacionados

  univariante_categorico()    -> countplot de UNA columna categórica
  univariante_numerico()      -> histplot + boxplot de UNA columna numérica

  bivariante_num_num()        -> scatterplot + correlación entre dos numéricas
  bivariante_cat_num_bar()    -> barplot de medias (categórica vs numérica)
  bivariante_cat_num_box()    -> boxplot (categórica vs numérica)
  bivariante_cat_cat_count()  -> countplot con hue (categórica vs categórica)
  bivariante_temporal()       -> lineplot de una métrica resampleada en el tiempo

Todas asumen que le pasas el DataFrame ya al nivel correcto
(df = nivel pedido / order_id, clientes = nivel cliente / id_cliente).
Repasa la Guía de claves de Fase 3 antes de decidir qué tabla usar.
"""

# Tratamiento de Datos
import pandas as pd
import numpy as np
from IPython.display import display

# Visualizaciones
import matplotlib.pyplot as plt
import seaborn as sns

# Para que se muestren todas las columnas al inspeccionar los DataFrames
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.expand_frame_repr', False)


# ============================================================================
# 0. PRE-EDA
# ============================================================================

# ============================================================================
# 1. EDA PRELIMINAR 
# ============================================================================

def eda(df, cols_excluir=None):
    """
    Funcion que proporciona un EDA rapido.

    Parameters
    ----------
    df : DataFrame
        DataFrame que queremos analizar.

    n : int
        Numero de decimales para las estadisticas numericas.

    cols_excluir : list
        Lista de columnas que no queremos analizar.
    """

    # Si no indicamos columnas a excluir,
    # creamos una lista vacia
    if cols_excluir is None:
        cols_excluir = []

    # Creamos un DataFrame sin las columnas excluidas
    df_eda = df.drop(columns=cols_excluir, errors="ignore")

    # --------------------------------------------------
    # IDENTIFICACION DE TIPOS DE COLUMNAS
    # --------------------------------------------------

    num_cols = df_eda.select_dtypes(
        include="number"
    ).columns

    cat_cols = df_eda.select_dtypes(
        include=["string", "category", "object"]
    ).columns

    date_cols = df_eda.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns

    # Mostramos las columnas encontradas
    print("VARIABLES NUMERICAS:\n\n", num_cols)
    print('=' * 100)

    print("\nVARIABLES CATEGORICAS:\n\n", cat_cols)
    print('=' * 100)

    print("\nVARIABLES DATETIME(FECHA):\n\n", date_cols)

    # --------------------------------------------------
    # ESTADISTICAS BASICAS
    # --------------------------------------------------

    print("\n========== ESTADÍSTICAS BÁSICAS ==========\n")

    # Variables numericas
    if len(num_cols) > 0:

        print("VARIABLES NUMERICAS:")

        print(
            df_eda[num_cols]
            .describe()
            .T
            .round(2)
        )

    # Variables categoricas
    if len(cat_cols) > 0:

        print("\nVARIABLES CATEGORICAS:")

        print(
            df_eda[cat_cols]
            .describe()
            .T
        )

    # Variables datetime
    if len(date_cols) > 0:

        print("\nVARIABLES DATETIME(FECHA):")

        print(
            df_eda[date_cols]
            .describe()
            .T
        )

    # --------------------------------------------------
    # ANALISIS DE VARIABLES CATEGORICAS
    # --------------------------------------------------

    if len(cat_cols) > 0:

        print(
            "\n========== ANALISIS DE VARIABLES CATEGORICAS ==========\n"
        )

        for col in cat_cols:

            print(
                f"\n----------- ESTAMOS ANALIZANDO: '{col}' ----------\n"
            )

            print("Valores únicos:")

            print(
                df_eda[col].unique()
            )

            print("\nFrecuencia de los valores:")

            print(
                df_eda[col].value_counts()
            )

    # --------------------------------------------------
    # COUNTPLOT
    # --------------------------------------------------

    if len(cat_cols) > 0:

        print(
            "\n============== COUNTPLOT ==============\n"
            "(REPRESENTACIÓN DE UNIVARIABLES CATEGÓRICAS)"
        )

        # Si tiene demasiadas categorias,
        # no hacemos el grafico
        cat_cols_plot = [
            col for col in cat_cols
            if df_eda[col].nunique() <= 200
        ]

        # Mostramos las columnas que no se van a representar
        for col in cat_cols:

            if df_eda[col].nunique() > 200:

                print(
                    f"Columna {col} tiene demasiadas "
                    f"categorias: {df_eda[col].nunique()}"
                )

        # Creamos los graficos solo si hay columnas que representar
        if len(cat_cols_plot) > 0:

            n_graficos = len(cat_cols_plot)
            ncols = 2
            nrows = (n_graficos + ncols - 1) // ncols

            fig, axes = plt.subplots(
                nrows,
                ncols,
                figsize=(8 * ncols, 5 * nrows)
            )

            axes = np.atleast_1d(axes).flatten()

            for ax, col in zip(axes, cat_cols_plot):

                sns.countplot(
                    x=df_eda[col],
                    order=df_eda[col].value_counts().index,
                    ax=ax
                )

                ax.set_title(f"Distribución de {col}")
                ax.tick_params(axis="x", rotation=90)

            # Ocultamos ejes sobrantes
            for ax in axes[n_graficos:]:
                ax.set_visible(False)

            plt.tight_layout()
            plt.show()

    # --------------------------------------------------
    # HISTOGRAMAS
    # --------------------------------------------------

    if len(num_cols) > 0:
        print(
            "\n============== HISTOGRAMAS ==============\n"
            "(REPRESENTACION DE UNIVARIABLES NUMERICAS):"
        )

        n_graficos = len(num_cols)
        ncols = 3
        nrows = (n_graficos + ncols - 1) // ncols

        fig, axes = plt.subplots(
            nrows,
            ncols,
            figsize=(5 * ncols, 3.5 * nrows)
        )

        axes = np.atleast_1d(axes).flatten()

        for ax, col in zip(axes, num_cols):

            sns.histplot(
                df_eda[col],
                bins=20,
                ax=ax
            )

            ax.set_title(col)

        # Ocultamos ejes sobrantes
        for ax in axes[n_graficos:]:
            ax.set_visible(False)

        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # BOXPLOTS
    # --------------------------------------------------

    if len(num_cols) > 0:

        print(
            "\n============== BOXPLOTS ==============\n"
            "(REPRESENTACION DE UNIVARIABLES NUMERICAS - OUTLIERS)"
        )

        n_graficos = len(num_cols)
        ncols = 1
        nrows = (n_graficos + ncols - 1) // ncols

        fig, axes = plt.subplots(
            nrows,
            ncols,
            figsize=(10 * ncols, 2 * nrows)
        )

        axes = np.atleast_1d(axes).flatten()

        for ax, col in zip(axes, num_cols):

            sns.boxplot(
                x=df_eda[col],
                ax=ax
            )

            ax.set_title(col)

        # Ocultamos ejes sobrantes
        for ax in axes[n_graficos:]:
            ax.set_visible(False)

        plt.tight_layout()
        plt.show()

# --------------------------------------------------
# EXPLORACION DEL DATA FRAME
# --------------------------------------------------

def exploracion(df,cols_excluir=None, n=3):

 # Si no indicamos columnas a excluir,
    # creamos una lista vacia
    if cols_excluir is None:
        cols_excluir = []

    # Creamos un DataFrame sin las columnas excluidas
    df_exp = df.drop(columns=cols_excluir, errors="ignore")

    print('PRIMERAS COLUMNAS')
    display(df_exp.sample(n).T)
    print(":" * 100)
    print('INFORMACIÓN BÁSICA')
    display(df_exp.info())
    print(":" * 100)
    print('ESTADISTICOS')
    display(df_exp.describe(include="all").T)
    print(":" * 100)
    print('TAMAÑO DATAFRAME')
    print(df_exp.shape)
    print(":" * 100)
    print('NULOS')
    display(df_exp.isnull().sum()[df.isnull().sum() > 0].sort_values(ascending=False))
    print(":" * 100)
    print('PORCENTAJE DE NULOS')
    display((df_exp.isna().mean()[df.isna().mean() > 0] * 100).sort_values(ascending=False).round(2))
    print(":" * 100)
    print('DUPLICADOS')
    print(df_exp.duplicated().sum())


# ============================================================================
#                ANALISIS ESPECIFICOS CON VISUALIZACIONES
# ============================================================================

# ============================================================================
# 1. UNIVARIANTE — una variable
# ============================================================================

    # --------------------------------------------------
    # COUNTPLOT
    # --------------------------------------------------

def countplot(df, col):
    """
    Distribución de una variable categórica.
    Dibuja un countplot ordenado por frecuencia.
    """
    order = df[col].value_counts().index

    sns.countplot(data=df, x=col, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel(col)
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()

    print(df[col].value_counts())
    print("."*40)
    print("PORCENTAJES")
    print(df[col].value_counts(normalize=True).mul(100).round(2))

    # --------------------------------------------------
    # HISTPLOT
    # --------------------------------------------------

def histplot(df, col, bins=30):
    """
    Distribución de una variable numérica.
    Dibuja un histograma.
    """
    sns.histplot(data=df, x=col, bins=bins)
    plt.title(f"Distribución de {col}")
    plt.xlabel(col)
    plt.ylabel("Frecuencia")

    plt.tight_layout()
    plt.show()

    print(df[col].describe().round(2))
    print("."*40)


    # --------------------------------------------------
    # BOXPLOT
    # --------------------------------------------------

def boxplot(df, col, bins=30):
    """
    Distribución de una variable numérica.
    Dibuja un boxplot.
    """
    sns.boxplot(data=df, x=col)
    plt.title(f"Boxplot de {col}")
    plt.xlabel(col)

    plt.tight_layout()
    plt.show()

    print(df[col].describe().round(2))

    # --------------------------------------------------
    # DETECTAR_OUTLIERS DATAFRAME
    # --------------------------------------------------

def detectar_outliers(df): #OJO ESTARA EN SP LIMPIEZA
    # 1. Detectar qué columnas numéricas tienen outliers, mostrando el detalle
    columnas_con_outliers = []

    for columna in df.select_dtypes(include='number').columns:
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1

        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        outliers = df[
            (df[columna] < limite_inferior) |
            (df[columna] > limite_superior)
        ]
        n_outliers = len(outliers)

        if n_outliers > 0:
            print(f"Columna: {columna}")
            print(f"Q1: {Q1:.3f}")
            print(f"Q3: {Q3:.3f}")
            print(f"IQR: {IQR:.3f}")
            print(f"Límite inferior: {limite_inferior:.3f}")
            print(f"Límite superior: {limite_superior:.3f}")
            print(f"Outliers encontrados: {n_outliers}")
            print(f"El porcentaje de Outliers en {columna} es: {n_outliers/df.shape[0]*100:.3f} %")
            print(f"\nDescribe de los outliers en {columna}:")
            print(outliers[columna].describe().round(3))
            print("-" * 50)
            columnas_con_outliers.append(columna)

    if not columnas_con_outliers:
        print("No se detectaron outliers en ninguna columna numérica.")
        return

    # --------------------------------------------------
    # DETECTAR_OUTLIERS COLUMNA
    # --------------------------------------------------

def detectar_outlier_col(columna):
    Q1 = columna.quantile(0.25)
    Q3 = columna.quantile(0.75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    print(f"Valores outiers")
    print(f"Q1: {Q1:.3f}")
    print(f"Q3: {Q3:.3f}")
    print(f"IQR: {IQR:.3f}")
    print(f"Límite inferior: {limite_inferior:.3f}")
    print(f"Límite superior: {limite_superior:.3f}")
 

# --------------------------------------------------
# MATRIZ_CORRELACION
# --------------------------------------------------

def matriz_correlacion(df, lista_cols_num=None, cols_excluir=None, top_n=10):
    """Calcula y representa la matriz de correlación
    y muestra los pares de variables más correlacionados."""

    if cols_excluir is None:
        cols_excluir = []

    # Seleccionar columnas numéricas
    if lista_cols_num is None:
        corr = df.corr(numeric_only=True)
    else:
        corr = df[lista_cols_num].corr()

    # Eliminar filas y columnas excluidas
    corr = corr.drop(
        index=cols_excluir,
        columns=cols_excluir,
        errors="ignore"
    )

    # Crear la figura
    plt.figure(
        figsize=(
            0.7 * len(corr.columns) + 2,
            0.6 * len(corr.columns) + 2
        )
    )

    # Crear máscara triangular
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Crear heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        annot_kws={"size": 7}
    )

    plt.tight_layout()
    plt.show()

    # Obtener pares de variables más correlacionados
    pares = corr.abs().unstack().sort_values(ascending=False)

    # Eliminar correlaciones de una variable consigo misma
    pares = pares[pares < 0.999].drop_duplicates()

    print(f"Top {top_n} pares con mayor correlación (valor absoluto):")
    print(pares.head(top_n))

    return corr


# ============================================================================
# 2. BIVARIANTE — dos variables
# ============================================================================

    # --------------------------------------------------
    # SCATTERPLOTS
    # --------------------------------------------------

def scatterplot(df, col_x, col_y):
    """
    Relación entre dos variables numéricas.
    Dibuja un scatterplot y calcula la correlación de Pearson.
    """
    sns.scatterplot(data=df, x=col_x, y=col_y, alpha=0.35)
    plt.title(f"{col_x} vs {col_y}")
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.tight_layout()
    plt.show()

    r = df[col_x].corr(df[col_y])
    print(f"Correlación de Pearson entre {col_x} y {col_y}: {r:.4f}")

    return r

    # --------------------------------------------------
    # BARPLOTS
    # --------------------------------------------------

def barplot(df, col_cat, col_num, estimator="mean", errorbar=None):
    """
    Estadístico (media, mediana, suma...) de una variable numérica
    según una variable categórica.
    Dibuja un barplot con ese estadístico.

    estimator: "mean", "median", "sum", etc.
    """
    sns.barplot(data=df, x=col_cat, y=col_num, estimator=estimator)
    plt.title(f"{estimator} de {col_num} por {col_cat}")
    plt.xlabel(col_cat)
    plt.ylabel(f"{estimator} de {col_num}")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

    valores = df.groupby(col_cat)[col_num].agg(estimator).round(2).sort_values(ascending=False)
    print(f"{estimator} de {col_num} por {col_cat}:")
    print(valores)

    return valores

    # --------------------------------------------------
    # BOXPLOT - VIBARIABLES
    # --------------------------------------------------

def boxplot_bivar(df, col_cat, col_num):
    """
    Distribución de una variable numérica según una variable categórica.
    Dibuja un boxplot (muestra mediana, dispersión y outliers).
    """
    sns.boxplot(data=df, x=col_cat, y=col_num)
    plt.title(f"Boxplot de {col_num} vs {col_cat}")
    plt.xlabel(col_cat)
    plt.ylabel(col_num)
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

    resumen = df.groupby(col_cat)[col_num].describe().round(2)
    print(f"Resumen de {col_num} por {col_cat}:")
    print(resumen)

    return resumen

    # --------------------------------------------------
    # COUNTPLOT - HUE
    # --------------------------------------------------

def countplot_hue(df, col_cat, hue):
    """
    Relación entre dos variables categóricas.
    Dibuja un countplot de col_cat coloreado por hue.
    """
    sns.countplot(data=df, x=col_cat, hue=hue)
    plt.title(f"Conteo de {col_cat} por {hue}")
    plt.xlabel(col_cat)
    plt.ylabel("Conteo")
    plt.xticks(rotation=20)
    plt.legend(title=hue)
    # Leyenda fuera del gráfico
    plt.legend(
        title=hue,
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )
    
    plt.tight_layout()
    plt.show()

    tabla = pd.crosstab(df[col_cat], df[hue])
    print(f"Tabla de conteos: {col_cat} vs {hue}")
    print(tabla)

    return tabla

    # --------------------------------------------------
    # LINEPLOT
    # --------------------------------------------------


def lineplot(df, col_fecha, col_num, marker='o', freq="ME", agg="sum"):
    """
    Evolución de una métrica numérica a lo largo del tiempo.

    freq: "D" diario, "W" semanal, "ME" mensual, "YE" anual
    agg: "sum", "mean", "count", etc.
    """
    datos = df[[col_fecha, col_num]].dropna()
    datos[col_fecha] = pd.to_datetime(datos[col_fecha])
    datos = datos.set_index(col_fecha)

    serie = datos[col_num].resample(freq).agg(agg)

    # Convertimos la serie en DataFrame para usar seaborn
    datos_plot = serie.reset_index()

    plt.figure(figsize=(10, 5))

    sns.lineplot(
        data=datos_plot,
        x=col_fecha,
        y=col_num
    )

    plt.title(f"Evolución de {col_num} ({agg}, freq={freq})")
    plt.xlabel("Fecha")
    plt.ylabel(col_num)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    print(f"Media: {serie.mean():.2f}   Std: {serie.std():.2f}")
    print(f"Mínimo: {serie.idxmin()} -> {serie.min():.2f}")
    print(f"Máximo: {serie.idxmax()} -> {serie.max():.2f}")

    return serie

    # --------------------------------------------------
    # BARPLOTS - SERIES
    # --------------------------------------------------

def barplot_serie(serie, titulo, kind="bar", color=None, xlabel=None, ylabel=None):
    """ Representa una Serie ya agregada (resultado de un groupby, value_counts,
    o cualquier cálculo previo), sin necesidad de volver a agregar datos.

    Útil para los casos en los que ya tienes el resultado calculado
    (ej. ventas por mes, tasa de devolución por canal) y solo
    necesitas graficarlo.

    Parameters
    ----------
    serie : pd.Series
        Serie ya agregada (el índice será el eje x, o el eje y si kind="barh").

    titulo : str
        Título del gráfico.

    kind : str
        Tipo de gráfico: "bar", "barh" o "line". Por defecto "bar".

    color : str
        Color de las barras/línea (opcional).

    xlabel : str
        Etiqueta del eje x (opcional, si no se indica usa el nombre del índice).

    ylabel : str
        Etiqueta del eje y (opcional, si no se indica usa el nombre de la serie)."""

    plt.figure(figsize=(8, 4))

    if kind == "bar":
        serie.plot(kind="bar", color=color)
        plt.xticks(rotation=30)

    elif kind == "barh":
        serie.plot(kind="barh", color=color)

    elif kind == "line":
        serie.plot(kind="line", marker="o", color=color)
        plt.xticks(rotation=30)

    else:
        raise ValueError('kind debe ser "bar", "barh" o "line"')

    plt.title(titulo)
    plt.xlabel(xlabel if xlabel else (serie.index.name or ""))
    plt.ylabel(ylabel if ylabel else (serie.name or ""))

    plt.tight_layout()
    plt.show()

    print(serie.round(2))

    return serie
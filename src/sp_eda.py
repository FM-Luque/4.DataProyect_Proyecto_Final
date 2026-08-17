"""
sp_eda_completo.py
===================
Caja de herramientas de Fase 3 — Análisis Descriptivo y Visualización (EDA).

Sigue el flujo: Pre-EDA -> Univariante -> Bivariante -> Global.
Solo contenido descriptivo (nada de tests de hipótesis / p-valores:
eso vive en sp_abtest_completo.py, Fase 4).

  pre_eda_calidad()              -> nulos + verificación order_id / id_cliente
  univariante_categorico()       -> countplot en subplots, 1 por columna
  univariante_numerico()         -> histplot + boxplot en subplots
  bivariante_num_num()           -> scatterplot + correlación
  bivariante_cat_num()           -> barplot en subplots, 1 por columna categórica
  bivariante_temporal()          -> lineplot de una métrica resampleada en el tiempo
  eda_global_heatmap()           -> heatmap de correlaciones

Todas asumen que le pasas el DataFrame ya al nivel correcto
(df = nivel pedido / order_id, clientes = nivel cliente / id_cliente).
Repasa la Guía de claves de Fase 3 antes de decidir qué tabla usar.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns






# Tratamiento de Datos
import pandas as pd
import numpy as np
from IPython.display import display

# Visualizaciones
import matplotlib.pyplot as plt
import seaborn as sns

# Para que se muestren todas las columnas al imspeccionar los DataFrames
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns',None)


# ============================================================================
# 0. PRE-EDA
# ============================================================================


def analisis_rapido(df, n=5):
    """Función que proporciona un analisis rápido del dataframe.
    parámetros:
    df : Dataframe
    n : numero de filas (por defecto 5)   
    """
    print(f"Las {n} primeras columnas son:\n {df.head(n).T}")
    print(":" * 100)
    print(f"La informacion basica es:")
    df.info()
    print(":" * 100)
    print(f"El número de duplicados es: {df.duplicated().sum()}")
    print(":" * 100)
    print(f"El procentaje de nulos es:\n{df.isna().mean().round(4)*100} ")


import matplotlib.pyplot as plt
import seaborn as sns


def eda(df, n=2, cols_excluir=None):
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

    # Identificamos los tipos de columnas
    num_cols = df_eda.select_dtypes(include="number").columns

    cat_cols = df_eda.select_dtypes(
        include=["string", "category", "object"]
    ).columns

    date_cols = df_eda.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns

    # Mostramos las columnas encontradas
    print("Variables numéricas:\n\n", num_cols)

    print("\nVariables categóricas:\n\n", cat_cols)

    print("\nVariables datetime:\n\n", date_cols)

    # --------------------------------------------------
    # ESTADISTICAS BASICAS
    # --------------------------------------------------

    print("\n========== ESTADÍSTICAS BÁSICAS ==========\n")

    # Variables numericas
    if len(num_cols) > 0:

        print("Variables numéricas:")

        print(
            df_eda[num_cols]
            .describe()
            .T
            .round(n)
        )

    # Variables categoricas
    if len(cat_cols) > 0:

        print("\nVariables categóricas:")

        print(
            df_eda[cat_cols]
            .describe()
            .T
        )

    # Variables datetime
    if len(date_cols) > 0:

        print("\nVariables datetime:")

        print(
            df_eda[date_cols]
            .describe()
            .T
        )

    # --------------------------------------------------
    # ANALISIS DE VARIABLES CATEGORICAS
    # --------------------------------------------------

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

    print("\nRepresentación de Countplot:\n")

    for col in cat_cols:

        # Si tiene demasiadas categorias,
        # no hacemos el grafico
        if df_eda[col].nunique() > 200:

            print(
                f"Columna {col} tiene demasiadas "
                f"categorias: {df_eda[col].nunique()}\n"
            )

            continue

        # Numero de categorias
        num_categorias = df_eda[col].nunique()

        # Calculamos el ancho del grafico
        width = max(7, num_categorias * 0.5)

        height = 3

        plt.figure(figsize=(width, height))

        sns.countplot(
            x=df_eda[col],
            order=df_eda[col].value_counts().index
        )

        plt.title(f"Gráfico de barras de {col}")

        plt.xlabel(col)

        plt.ylabel("Frecuencia")

        plt.xticks(rotation=90)

        plt.show()

    # --------------------------------------------------
    # HISTOGRAMAS
    # --------------------------------------------------

    print("\nRepresentación de Histplot:\n")

    for col in num_cols:

        plt.figure(figsize=(10, 4))

        sns.histplot(
            df_eda[col],
            bins=30,
            edgecolor="black"
        )

        plt.title(f"Distribución de {col}")

        plt.xlabel(col)

        plt.ylabel("Frecuencia")

        plt.show()

    # --------------------------------------------------
    # BOXPLOTS
    # --------------------------------------------------

    print("\nRepresentación de Boxplot:\n")

    for col in num_cols:

        plt.figure(figsize=(10, 2))

        sns.boxplot(
            x=df_eda[col]
        )

        plt.title(f"Distribución de {col}")

        plt.xlabel(col)

        plt.show()

def matriz_correlación(df):
    """ Función que representa la matriz de correlacion
    con un hearmap"""

    # Calcular la matriz de correlación
    corr_matrix = df.corr(numeric_only=True)

    # Crear la figura
    plt.figure(figsize=corr_matrix.shape)

    # Crear una máscara para mostrar solo la parte triangular
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # Graficar el mapa de calor
    sns.heatmap(corr_matrix,
                annot=True,
                vmin=-1,
                vmax=1,
                mask=mask,
                cmap='cool')
    plt.show()

    # ============================================================================
    #                ANALISIS ESPECIFICOS CON VUSIALIZACIONES
    # ============================================================================

# ============================================================================
# 1. UNIVARIANTE — una variable
# ============================================================================


def univariante_categorico(dataframe, lista_cols, ncols=3):
    """
    Representa la distribución de las variables categóricas
    que indiquemos en lista_cols.

    Los gráficos se organizan en 3 columnas por fila.
    """

    # Número de gráficos
    num_graph = len(lista_cols)

    # Número de filas necesarias
    num_rows = (num_graph + ncols - 1) // ncols

    # Creamos los subplots
    fig, axes = plt.subplots(
        num_rows,
        ncols,
        figsize=(6 * ncols, 4 * num_rows)
    )

    # Convertimos axes en una lista
    axes = axes.flatten()

    # Creamos un gráfico para cada columna
    for i, col in enumerate(lista_cols):

        # Ordenamos las categorías por frecuencia
        order = dataframe[col].value_counts().index

        sns.countplot(
            data=dataframe,
            x=col,
            order=order,
            ax=axes[i]
        )

        axes[i].set_title(
            f"Distribución de {col}"
        )

        axes[i].set_xlabel(col)

        axes[i].set_ylabel("Frecuencia")

        axes[i].tick_params(
            axis="x",
            rotation=30
        )

    # Eliminamos los espacios que sobren
    for j in range(num_graph, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def univariante_numerico(dataframe, lista_cols, ncols=3):
    """
    Representa la distribución de las variables numéricas
    que indiquemos en lista_cols.

    Se crean dos bloques:
    - Histogramas
    - Boxplots

    Los gráficos se organizan en 3 columnas por fila.
    """

    # Número de gráficos
    num_graph = len(lista_cols)

    # Número de filas necesarias
    num_rows = (num_graph + ncols - 1) // ncols

    # ==========================================
    # HISTOGRAMAS
    # ==========================================

    fig, axes = plt.subplots(
        num_rows,
        ncols,
        figsize=(6 * ncols, 4 * num_rows)
    )

    axes = axes.flatten()

    for i, col in enumerate(lista_cols):

        sns.histplot(
            data=dataframe,
            x=col,
            ax=axes[i],
            bins=30
        )

        axes[i].set_title(
            f"Distribución de {col}"
        )

        axes[i].set_xlabel(col)

        axes[i].set_ylabel("Frecuencia")

    # Eliminamos los espacios que sobren
    for j in range(num_graph, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

    # ==========================================
    # BOXPLOTS
    # ==========================================

    fig, axes = plt.subplots(
        num_rows,
        ncols,
        figsize=(6 * ncols, 3 * num_rows)
    )

    axes = axes.flatten()

    for i, col in enumerate(lista_cols):

        sns.boxplot(
            data=dataframe,
            x=col,
            ax=axes[i]
        )

        axes[i].set_title(
            f"Boxplot de {col}"
        )

        axes[i].set_xlabel(col)

    # Eliminamos los espacios que sobren
    for j in range(num_graph, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()



# ============================================================================
# 2. BIVARIANTE — dos variables
# ============================================================================

import matplotlib.pyplot as plt
import seaborn as sns


def bivariante_num_num(df, col_x, col_y, alpha=0.35):
    """
    Scatterplot + correlación de Pearson
    entre dos variables numéricas.
    """

    # ==========================================
    # SCATTERPLOT
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(6, 4.2)
    )

    sns.scatterplot(
        data=df,
        x=col_x,
        y=col_y,
        alpha=alpha,
        ax=ax
    )

    ax.set_title(
        f"{col_x} vs {col_y}"
    )

    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)

    plt.tight_layout()
    plt.show()

    # ==========================================
    # CORRELACIÓN DE PEARSON
    # ==========================================

    # Eliminamos filas que tengan NaN
    # en alguna de las dos columnas
    datos = df[[col_x, col_y]].dropna()

    # Calculamos la correlación
    r = datos[col_x].corr(
        datos[col_y]
    )

    print(
        f"Correlación (Pearson) "
        f"{col_x} vs {col_y}: r = {r:.4f}"
    )

    return r

# ==========================================
# BARPLOT
# ==========================================
def bivariante_cat_num(
    df,
    col_control,
    lista_metricas,
    ci=95
):
    """
    Barplot de la media de una variable numérica
    según una variable categórica.

    Se pueden indicar:

    - Una o varias variables categóricas.
    - Una o varias métricas numéricas.

    Los gráficos se organizan en
    3 columnas por fila.
    """

    # ==========================================
    # PREPARAMOS LAS VARIABLES
    # ==========================================

    # Si solo pasamos una columna como texto,
    # la convertimos en una lista
    if isinstance(col_control, str):

        col_control = [col_control]

    # Número total de gráficos
    num_graph = (
        len(col_control)
        * len(lista_metricas)
    )

    # Número de columnas por fila
    ncols = 3

    # Número de filas necesarias
    num_rows = (
        num_graph + ncols - 1
    ) // ncols

    # ==========================================
    # CREAMOS LOS SUBPLOTS
    # ==========================================

    fig, axes = plt.subplots(
        num_rows,
        ncols,
        figsize=(
            6 * ncols,
            4 * num_rows
        )
    )

    # Convertimos axes en una lista
    axes = axes.flatten()

    # Diccionario donde guardaremos
    # las medias
    medias = {}

    # Contador de gráficos
    idx = 0

    # ==========================================
    # CREAMOS LOS GRAFICOS
    # ==========================================

    for metrica in lista_metricas:

        for col in col_control:

            sns.barplot(
                data=df,
                x=col,
                y=metrica,
                ax=axes[idx],
                errorbar=("ci", ci)
            )

            axes[idx].set_title(
                f"{metrica} medio por {col}"
            )

            axes[idx].set_xlabel(col)

            axes[idx].set_ylabel(
                f"Media de {metrica}"
            )

            axes[idx].tick_params(
                axis="x",
                rotation=20
            )

            # ==================================
            # CALCULAMOS LAS MEDIAS
            # ==================================

            medias[(metrica, col)] = (
                df.groupby(col)[metrica]
                .mean()
                .round(2)
                .sort_values(
                    ascending=False
                )
            )

            idx += 1

    # ==========================================
    # ELIMINAMOS ESPACIOS SOBRANTES
    # ==========================================

    for j in range(
        num_graph,
        len(axes)
    ):

        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

    # ==========================================
    # MOSTRAMOS LAS MEDIAS
    # ==========================================

    for (metrica, col), serie in medias.items():

        print(
            f"{metrica} medio por {col}:"
        )

        print(serie)

        print()

    return medias

# ==========================================
# LINEPLOT
# ==========================================
def bivariante_temporal(
    df,
    col_fecha,
    col_metrica,
    freq="ME",
    agg="sum"
):
    """
    Lineplot de una métrica agregada a lo largo del tiempo.

    freq:
        "ME" = mensual
        "W"  = semanal
        "D"  = diario
        "YE" = anual
        etc.

    agg:
        "sum"  = suma
        "mean" = media
        "count" = número de registros
        etc.
    """

    # ==========================================
    # PREPARAMOS LOS DATOS
    # ==========================================

    # Nos quedamos con fecha y métrica
    datos = df[[col_fecha, col_metrica]].dropna()

    # Nos aseguramos de que la fecha
    # tenga formato datetime
    datos[col_fecha] = pd.to_datetime(
        datos[col_fecha]
    )

    # Ponemos la fecha como índice
    datos = datos.set_index(col_fecha)

    # Agregamos la métrica según la frecuencia
    serie = (
        datos[col_metrica]
        .resample(freq)
        .agg(agg)
    )

    # Convertimos la serie en DataFrame
    # para utilizar seaborn
    datos_grafico = serie.reset_index()

    # ==========================================
    # LINEPLOT
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(10, 4)
    )

    sns.lineplot(
        data=datos_grafico,
        x=col_fecha,
        y=col_metrica,
        ax=ax
    )

    ax.set_title(
        f"Evolución de {col_metrica} "
        f"({agg}, freq={freq})"
    )

    ax.set_xlabel("Fecha")

    ax.set_ylabel(col_metrica)

    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()

    # ==========================================
    # ESTADÍSTICAS
    # ==========================================

    media = serie.mean()

    std = serie.std()

    # Coeficiente de variación
    cv = (
        std / media * 100
        if media != 0
        else float("nan")
    )

    print(
        f"Media: {media:.2f}   "
        f"Std: {std:.2f}   "
        f"CV: {cv:.2f}%"
    )

    print(
        f"Mínimo: {serie.idxmin()} "
        f"-> {serie.min():.2f}"
    )

    print(
        f"Máximo: {serie.idxmax()} "
        f"-> {serie.max():.2f}"
    )

    return serie


# ============================================================================
# 3. GLOBAL
# ============================================================================

def eda_global_heatmap(df, lista_cols_num, top_n=8):
    """Heatmap de correlaciones + tabla de los pares más correlacionados."""

    corr = df[lista_cols_num].corr()

    fig, ax = plt.subplots(figsize=(0.7 * len(lista_cols_num) + 2, 0.6 * len(lista_cols_num) + 2))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, annot_kws={'size': 7})
    plt.tight_layout()
    plt.show()

    pares = corr.abs().unstack().sort_values(ascending=False)
    pares = pares[pares < 0.999].drop_duplicates()
    print(f'Top {top_n} pares con mayor correlación (valor absoluto):')
    print(pares.head(top_n))

    return corr



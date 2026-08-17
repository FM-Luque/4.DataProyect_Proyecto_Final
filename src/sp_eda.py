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


# ============================================================================
# 0. PRE-EDA
# ============================================================================

def pre_eda_calidad(df, col_pedido='order_id', col_cliente='id_cliente'):
    """Nulos por columna + verificación de que las claves hacen lo que deben:
    col_pedido único (una fila = un pedido), col_cliente repetido (normal)."""

    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]

    fig, ax = plt.subplots(figsize=(6, 3.2))
    if len(nulos) > 0:
        ax.bar(nulos.index, nulos.values)
    ax.set_title('Valores nulos por columna')
    ax.set_ylabel('nº de filas nulas')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

    print(f'Columnas con nulos: {len(nulos)} de {df.shape[1]}')
    print(nulos if len(nulos) else '(ninguna)')

    dup_pedido = df[col_pedido].duplicated().sum()
    dup_cliente = df[col_cliente].duplicated().sum()
    n_clientes = df[col_cliente].nunique()

    print(f'\n{col_pedido} duplicados: {dup_pedido}  (esperado: 0)')
    print(f'{col_cliente} duplicados: {dup_cliente}  (>0 es normal: varios pedidos por cliente)')
    print(f'{col_cliente} únicos: {n_clientes}')

    if dup_pedido > 0:
        print(f'⚠️  {col_pedido} tiene duplicados: revisa si hay pedidos repetidos por error.')

# ============================================================================
# 1. DETECTAR COLUMNAS UTILES 
# ============================================================================


def cols_categoricas_validas(df, max_categorias=15, min_categorias=2, excluir=None):
    """Detecta columnas categóricas 'reales': dtype object/category,
    con cardinalidad manejable (ni IDs con miles de valores únicos,
    ni columnas constantes con 1 solo valor)."""
    print("COLUMNAS CATEGORICA VALIDAS")
    print("="*50)

    excluir = set(excluir or [])
    candidatas = df.select_dtypes(include=['object', 'category']).columns

    return [
        c for c in candidatas
        if c not in excluir and min_categorias <= df[c].nunique() <= max_categorias
    ]

    print(f"las columnas categoricas validas son: {cols_numericas_validas}")

def cols_numericas_validas(df, min_categorias=5, excluir=None):
    """Detecta columnas numéricas 'reales': dtype numérico, descartando
    aquellas con muy pocos valores únicos (suelen ser categorías codificadas
    como número, ej. año_ventas, flags 0/1)."""

    print("COLUMNAS NUMERICAS VALIDAS")
    print("="*50)
    
    excluir = set(excluir or [])
    candidatas = df.select_dtypes(include='number').columns

    return [
        c for c in candidatas
        if c not in excluir and df[c].nunique() >= min_categorias
    ]


# ============================================================================
# 1. UNIVARIANTE — una variable
# ============================================================================

def univariante_categorico(dataframe, lista_cols=None, excluir=None, ncols=3):

    if lista_cols is None:
        lista_cols = cols_categoricas_validas(dataframe, excluir=excluir)

    num_graph = len(lista_cols)
    num_rows = (num_graph + ncols - 1) // ncols

    fig, axes = plt.subplots(num_rows, ncols, figsize=(6*ncols, num_rows*4))
    axes = axes.flatten()

    for i, col in enumerate(lista_cols):
        order = dataframe[col].value_counts().index
        sns.countplot(data=dataframe, x=col, order=order, ax=axes[i])
        axes[i].set_title(f'Distribución de {col}')
        axes[i].tick_params(axis='x', rotation=30)

    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def univariante_numerico(dataframe, lista_cols=None, excluir=None):

    if lista_cols is None:
        lista_cols = cols_numericas_validas(dataframe, excluir=excluir)

    num_graph = len(lista_cols)
    fig, axes = plt.subplots(num_graph, 2, figsize=(15, num_graph*5))

    for i, col in enumerate(lista_cols):

        sns.histplot(data=dataframe, x=col, ax=axes[i,0], bins=200)
        axes[i,0].set_title(f'Distribución de {col}')
        axes[i,0].set_xlabel(col)
        axes[i,0].set_ylabel('Frecuencia')

        sns.boxplot(data=dataframe, x=col, ax=axes[i,1])
        axes[i,1].set_title(f'Boxplot de {col}')

    plt.tight_layout()
    plt.show()


def resumen_numerico(dataframe, lista_cols=None, excluir=None):

    if lista_cols is None:
        lista_cols = cols_numericas_validas(dataframe, excluir=excluir)

    resumen = {}
    for col in lista_cols:
        q1, q3 = dataframe[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
        n_out = ((dataframe[col] < lo) | (dataframe[col] > hi)).sum()

        resumen[col] = {
            'media': dataframe[col].mean(),
            'mediana': dataframe[col].median(),
            'outliers_pct': round(n_out / len(dataframe) * 100, 2),
            'skew': round(dataframe[col].skew(), 2),
        }

    return pd.DataFrame(resumen).T

# ============================================================================
# 2. BIVARIANTE — dos variables
# ============================================================================

def bivariante_num_num(df, col_x, col_y, alpha=0.35):
    """scatterplot + correlación de Pearson entre dos variables numéricas."""

    fig, ax = plt.subplots(figsize=(6, 4.2))
    sns.scatterplot(data=df, x=col_x, y=col_y, alpha=alpha, ax=ax)
    ax.set_title(f'{col_x} vs {col_y}')
    plt.tight_layout()
    plt.show()

    r = df[col_x].corr(df[col_y])
    print(f'Correlación (Pearson) {col_x} vs {col_y}: r = {r:.4f}')
    return r


def bivariante_cat_num(df, col_control, lista_metricas, ci=95, figsize=None):
    """barplot (media + IC) en subplots: una métrica numérica según cada
    variable categórica de col_control (puede ser una sola columna o lista)."""

    if isinstance(col_control, str):
        col_control = [col_control]

    n = len(col_control) * len(lista_metricas)
    figsize = figsize or (5.5 * n, 4)
    fig, axes = plt.subplots(1, n, figsize=figsize)
    if n == 1:
        axes = [axes]

    idx = 0
    medias = {}
    for metrica in lista_metricas:
        for col in col_control:
            sns.barplot(data=df, x=col, y=metrica, ax=axes[idx], errorbar=('ci', ci))
            axes[idx].set_title(f'{metrica} medio por {col}')
            axes[idx].tick_params(axis='x', rotation=20)
            medias[(metrica, col)] = df.groupby(col)[metrica].mean().round(2).sort_values(ascending=False)
            idx += 1

    plt.tight_layout()
    plt.show()

    for (metrica, col), serie in medias.items():
        print(f'{metrica} medio por {col}:')
        print(serie)
        print()

    return medias


def bivariante_temporal(df, col_fecha, col_metrica, freq='ME', agg='sum'):
    """lineplot de col_metrica resampleada en el tiempo (por defecto, suma
    mensual). freq sigue la notación de pandas ('ME'=mes, 'W'=semana, ...)."""

    serie = df.set_index(col_fecha).resample(freq)[col_metrica].agg(agg)

    fig, ax = plt.subplots(figsize=(8, 3.3))
    serie.plot(ax=ax)
    ax.set_title(f'Evolución de {col_metrica} ({agg}, freq={freq})')
    plt.tight_layout()
    plt.show()

    media, std = serie.mean(), serie.std()
    cv = std / media * 100 if media else float('nan')
    print(f'Media: {media:.2f}   Std: {std:.2f}   CV: {cv:.2f}%')
    print(f'Mínimo: {serie.idxmin()} -> {serie.min():.2f}')
    print(f'Máximo: {serie.idxmax()} -> {serie.max():.2f}')
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


# ============================================================================
# EJEMPLO DE USO — con tu proyecto (02_datos_limpios.csv)
# ============================================================================

if __name__ == '__main__':

    df = pd.read_csv('02_datos_limpios.csv')
    df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])

    clientes = df.groupby('id_cliente').agg(
        n_pedidos=('order_id', 'count'),
        gasto_total=('importe_total', 'sum'),
        edad=('edad', 'first'),
        ciudad=('ciudad', 'first'),
        segmento_cliente=('segmento_cliente', 'first'),
        ingresos_anuales=('ingresos_anuales', 'first'),
    ).reset_index()

    print('#### 1. PRE-EDA ####')
    pre_eda_calidad(df)

    print('\n#### 2. UNIVARIANTE CATEGÓRICO ####')
    univariante_categorico(df, ['segmento_cliente', 'canal', 'categoria_producto'])

    print('\n#### 3. UNIVARIANTE NUMÉRICO ####')
    univariante_numerico(df, ['importe_total', 'edad', 'ingresos_anuales'])

    print('\n#### 4. BIVARIANTE NUM-NUM ####')
    bivariante_num_num(clientes, 'ingresos_anuales', 'gasto_total')

    print('\n#### 5. BIVARIANTE CAT-NUM ####')
    bivariante_cat_num(df, ['canal', 'segmento_cliente'], ['importe_total'])

    print('\n#### 6. BIVARIANTE TEMPORAL ####')
    bivariante_temporal(df, 'fecha_pedido', 'importe_total')

    print('\n#### 7. GLOBAL — HEATMAP ####')
    num_cols = ['importe_total', 'cantidad', 'precio_unitario', 'descuento', 'calificacion',
                'costo_unitario', 'precio_lista', 'peso_kg', 'stock_disponible',
                'rating_promedio_producto', 'edad', 'ingresos_anuales', 'visitas_web_mes']
    eda_global_heatmap(df, num_cols)

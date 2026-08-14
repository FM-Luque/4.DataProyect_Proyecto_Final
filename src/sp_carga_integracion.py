
# Libreria para Tratamiento de Datos
import pandas as pd
from IPython.display import display

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.expand_frame_repr', False)

pd.set_option('display.max_columns', None) 

def eda_preliminar(df):
    """
    Realiza un analisis exploratorio preliminar sobre un Dataframe dado.

    Este análisis incluye:
    - Muestra de 5 Filas Aleatorias 
    - informacion general del DataFrame (tipo datos, nulos, etc)
    - Porcentaje de valores nulos
    - Conteo de filas duplicadas
    - Distribución de valores para columnas categóricas

    Parametros:
    df (pd.DataFrame): DataFrame a analizar

    Retuns:
    None 
    """
    
    print('5 FILAS ALEATORIAS')
    display(df.sample(5).T)
    print('=' * 100)

    print('DIMENSIONES')
    print(f"El munero de filas es: {df.shape[0]} filas ")
    print(f"El munero de columnas es: {df.shape[1]} columnas")
    print('=' * 100)

    print('INFORMACION BASICA')
    print(df.info())
    print('=' * 100)

    print('COLUMNAS CON VALORES NULOS')
    print(df.isna().sum()[df.isna().sum() > 0])
    print('=' * 100)

    print('PORCENTAJES DE COLUMNAS CON VALORES NULOS')
    print(df.isna().mean()[df.isna().mean() > 0] * 100 )
    print('=' * 100)

    print('VALORES DUPLICADOS ')
    print(df.duplicated().sum())
    print('=' * 100)

    print('CONTEO COLUMNAS CATEGORIAS ')

    for col in df.select_dtypes(include='string').columns:
        print(col.upper())
        print(df[col].value_counts())
    print('=' * 100)

    print('ESTADISTICOS CATEGÓRICOS')
    estadisticos_C= df.describe(include=['string','category','object']).T
    display(estadisticos_C)

    print('ESTADISTICOS NUMÉRICAS')
    estadisticos_N= df.describe(include='number').T
    display(estadisticos_N)

    
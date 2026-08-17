import pandas as pd 

def minus(df):
    """ Funcion que convierte
    todas las variables a minusculas
    """
    for col in df.select_dtypes(include=['string','object']).columns:
        df[col]=df[col].str.lower()

def espacios(df):
    """ Funcion que reemplaza 
    todas las variables categoricas espacio
    por guión bajo
    """
    for col in df.select_dtypes(include=['string','object']).columns:
        df[col]=df[col].str.replace(' ','_')

def comas (df):
    """Funcion que reemplaza comas por puntos e
    intenta convertir a float
    """
    for col in df.select_dtypes(include=['string','object']).columns:
        df[col]=df[col].str.replace(',','.')
        try:
            df[col]=df[col].astype('float64')
        except:
            pass
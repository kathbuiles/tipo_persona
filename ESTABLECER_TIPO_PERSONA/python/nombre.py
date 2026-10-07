# nombre.py

import pandas as pd
import os
from datetime import datetime

from .metadata import (
    ruta_output_omisos
)


from ESTABLECER_TIPO_PERSONA.python.normalizado import leer_datos

def preparacion_clave_valor(runt_df, ic_df, insumo_df):
    diccionario_runt = dict(zip(runt_df["DOCUMENTO_PROPIETARIO"], runt_df["NOMBRE_PROPIETARIO"]))
    diccionario_insumo = dict(zip(insumo_df["ID_NORMALIZADO"], insumo_df["NOMBRES_APELLIDOS"]))
    diccionario_ic = dict(zip(ic_df["ID_USUARIO_IC"], ic_df["NOMBRES_APELLIDOS_IC"]))

    return diccionario_ic, diccionario_insumo, diccionario_runt


def completar_nombre_por_insumo(row, diccionario_insumo):
    if pd.isna(row["NOMBRE_COMPLETO"]) or row["NOMBRE_COMPLETO"] == "SIN_INFORMACION":
        return diccionario_insumo.get(row["ID_NORMALIZADO"], row["NOMBRE_COMPLETO"])
    return row["NOMBRE_COMPLETO"]


def completar_nombre_por_runt(row, diccionario_runt):
    if pd.isna(row["NOMBRE_COMPLETO"]) or row["NOMBRE_COMPLETO"] == "SIN_INFORMACION":
        return diccionario_runt.get(row["ID_NORMALIZADO"], row["NOMBRE_COMPLETO"])
    return row["NOMBRE_COMPLETO"]

def completar_nombre_por_ic(row, diccionario_ic):
    if pd.isna(row["NOMBRE_COMPLETO"]) or row["NOMBRE_COMPLETO"] == "SIN_INFORMACION":
        return diccionario_ic.get(row["ID_NORMALIZADO"], row["NOMBRE_COMPLETO"])
    return row["NOMBRE_COMPLETO"]

def completar_nombre_por_ic_ultima(row, diccionario_ic):
    if pd.isna(row["NOMBRE_COMPLETO"]) or row["NOMBRE_COMPLETO"] == "SIN_INFORMACION":
        return diccionario_ic.get(row["ID_NORMALIZADO"], row["NOMBRE_COMPLETO"])
    return row["NOMBRE_COMPLETO"]

def aplicar_funciones_nombre(parque_df, runt_df, ic_df, insumo_df, guardar=True):
    print("Columnas disponibles en 'parque_df':", parque_df.columns.tolist())
    print("Columnas disponibles en 'runt_df':", runt_df.columns.tolist())
    print("Columnas disponibles en 'ic_df':", ic_df.columns.tolist())
    print("Columnas disponibles en 'insumo_df':", insumo_df.columns.tolist())

    diccionario_ic, diccionario_insumo, diccionario_runt = preparacion_clave_valor(runt_df, ic_df, insumo_df)

    parque_df = parque_df.copy()
    parque_df["NOMBRE_COMPLETO"] = "SIN_INFORMACION"

    parque_df["NOMBRE_COMPLETO"] = parque_df.apply(
        lambda row: completar_nombre_por_insumo(row, diccionario_insumo), axis=1
    )

    parque_df["NOMBRE_COMPLETO"] = parque_df.apply(
        lambda row: completar_nombre_por_runt(row, diccionario_runt), axis=1
    )

    parque_df["NOMBRE_COMPLETO"] = parque_df.apply(
        lambda row: completar_nombre_por_ic(row, diccionario_ic), axis=1
    )
    
    parque_df["NOMBRE_COMPLETO"] = parque_df.apply(
        lambda row: completar_nombre_por_ic_ultima(row, diccionario_ic), axis=1
    )

    if guardar:
        fecha_actual = datetime.now().strftime('%Y%m%d')
        nombre_archivo = f"{fecha_actual}_parque_omiso_clasificacion_persona.parquet"
        parque_df.to_parquet(os.path.join(ruta_output_omisos, nombre_archivo), index=False)

    return parque_df
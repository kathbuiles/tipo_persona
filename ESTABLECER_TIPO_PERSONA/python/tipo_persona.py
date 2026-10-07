# tipo_persona.py

import pandas as pd
from ESTABLECER_TIPO_PERSONA.python.metadata import (
    ruta_persona_indeterminada, ruta_ic, ruta_runt, ruta_parque, clasificacion_tipo_persona
)
from ESTABLECER_TIPO_PERSONA.python.normalizado import (
    leer_datos, encontrar_tipo_persona_para_ic
)

# --- Preparación de diccionarios clave-valor ---
def construir_diccionarios_tipo_persona(runt, ic, insumo):
    """
    Construye los diccionarios necesarios para completar el tipo de persona
    usando distintas fuentes: IC, Insumo, RUNT.
    """
    diccionario_runt = dict(zip(runt["DOCUMENTO_PROPIETARIO"], runt["TIPO_PERSONA"]))
    diccionario_insumo = dict(zip(insumo["ID_NORMALIZADO"], insumo["TIPO_PERSONA"]))
    diccionario_ic = encontrar_tipo_persona_para_ic(ic)

    return diccionario_ic, diccionario_insumo, diccionario_runt

# --- Funciones de completado por fuente ---
def completar_por_insumo(row, diccionario_insumo):
    if pd.isna(row["TIPO_PERSONA"]) or row["TIPO_PERSONA"] == "DESCONOCIDO":
        return diccionario_insumo.get(row["ID_NORMALIZADO"])
    return row["TIPO_PERSONA"]

def completar_por_runt(row, diccionario_runt):
    if pd.isna(row["TIPO_PERSONA"]) or row["TIPO_PERSONA"] == "DESCONOCIDO":
        return diccionario_runt.get(row["ID_NORMALIZADO"])
    return row["TIPO_PERSONA"]

def completar_por_ic(row, diccionario_ic):
    if pd.isna(row["TIPO_PERSONA"]) or row["TIPO_PERSONA"] == "DESCONOCIDO":
        return diccionario_ic.get(row["ID_NORMALIZADO"])
    return row["TIPO_PERSONA"]


def completar_por_ic_ultima_opcion(row, diccionario_ic): #lo hace por ID_USUARIO
    if pd.isna(row["TIPO_PERSONA"]) or row["TIPO_PERSONA"] == "DESCONOCIDO":
        return diccionario_ic.get(row["ID_USUARIO"])
    return row["TIPO_PERSONA"]

# --- Función principal expuesta ---
def aplicar_funciones_busqueda(parque_omiso, runt, ic, insumo):
    """
    Completa el campo TIPO_PERSONA en el DataFrame 'parque_omiso'
    usando las siguientes fuentes en orden de prioridad:
    1. Insumo
    2. RUNT
    """
    dic_ic, dic_insumo, dic_runt = construir_diccionarios_tipo_persona(runt, ic, insumo)
    
    parque_omiso["TIPO_PERSONA"] = "DESCONOCIDO"
    
    parque_omiso["TIPO_PERSONA"] = parque_omiso.apply(
        lambda row: completar_por_insumo(row, dic_insumo), axis=1
    )
    parque_omiso["TIPO_PERSONA"] = parque_omiso.apply(
        lambda row: completar_por_runt(row, dic_runt), axis=1
    )
    
    parque_omiso["TIPO_PERSONA"] = parque_omiso.apply(
        lambda row: completar_por_ic(row, dic_ic), axis=1
    )
    
    parque_omiso["TIPO_PERSONA"] = parque_omiso.apply(
        lambda row: completar_por_ic_ultima_opcion(row, dic_ic), axis=1
    )
    print("Proceso de completado de tipo de persona finalizado.")

    return parque_omiso

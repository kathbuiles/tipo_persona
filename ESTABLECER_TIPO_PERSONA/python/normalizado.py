import pandas as pd
from ESTABLECER_TIPO_PERSONA.python.metadata import (
    ruta_persona_indeterminada, ruta_ic, ruta_runt,
    ruta_parque, clasificacion_tipo_persona
)


# ---------- LECTURA DE DATOS ----------
def leer_datos():
    print("Empezando lectura de datos...")
    runt = pd.read_parquet(ruta_runt)
    ic = pd.read_parquet(ruta_ic)
    persona_indeterminada = pd.read_excel(ruta_persona_indeterminada)
    insumo = pd.read_excel(clasificacion_tipo_persona)
    parque = pd.read_parquet(ruta_parque)
    print("Lectura completada.")
    return runt, ic, persona_indeterminada, insumo, parque


# ---------- UTILIDADES ----------
def calcular_digito_verificacion(nit: str) -> str | None:
    if not nit.isdigit() or len(nit) != 9:
        return None

    factores = (3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71)
    residuo = sum(int(nit[8 - i]) * factores[i] for i in range(9)) % 11
    return str(11 - residuo) if residuo > 1 else str(residuo)


def agregar_digito_verificacion(ids: pd.Series) -> pd.Series:
    ids = ids.copy().astype(str)
    cond_long = ids.str.len() == 9
    ids_validos = ids[cond_long & ids.str.isdigit()]
    digitos_verificacion = ids_validos.map(calcular_digito_verificacion)
    ids[cond_long & ids.str.isdigit()] += digitos_verificacion
    return ids


def reemplazar_ids(serie_ids: pd.Series) -> pd.Series:
    serie_ids = serie_ids.astype(str)
    ids_10 = set(serie_ids[serie_ids.str.len() == 10])
    ids_8 = set(serie_ids[serie_ids.str.len() == 8])

    reemplazos_manual = {
        "90921258": "8909212584",
        "890903407": "8909034079",
        "90903407": "8909034079",
        "16930826": "8909034079",
        "32323711": "9014222020",
        "860068200": "8600068200",
        "90905211111": "8909052111",
        "909052111111" : "8909052111",
          "90904996": "8909049961",
    "8902049966": "8909049961",
    "86005929": "8909039388",
    "8600399880": "8600399880",
    "90901533": "8909015331",
    "860068182": "8600026182",
    "8900261825": "8600026182",
    "8602261825": "8600026182",
    "90900024": "8909000248",
    "8600261875": "8608261828",
    "90922447": "8909224474",
    "90909001": "8909090011",
    "8909041815": "8908041815",
    "985457762": "9854577602",
    "8600394880": "8600399880",
    "81125328033": "8110253280",
    "8909003407": "8990903407",
    "90927913": "8909279138",
    "890903024": "8909030241",
    "90018239": "9001823973",
    "8909039383": "8909039388"
    }

    def ajustar_id(id_):
        if id_ in reemplazos_manual:
            return reemplazos_manual[id_]
        if len(id_) == 11:
            posible_id_10 = id_[:10]
            if posible_id_10 in ids_10:
                return posible_id_10
        elif len(id_) == 10 and id_[0] in ['8', '9']:
            posible_id_8 = id_[1:9]
            if posible_id_8 in ids_8:
                return id_
        return id_

    return serie_ids.map(ajustar_id)


# ---------- PROCESAMIENTO ----------
def establecer_tipo_persona_datos_faltantes(row):
    if row["TIPO_DOCUMENTO_IC"] in ["PASAP", "CC", "NUIP", "CE", "NREXT", "PPT", "RC", "CD", "TI", "C","P","T","E"]:
        return "PERSONA NATURAL"
    elif row["TIPO_DOCUMENTO_IC"] in ["NIT","N"]:
        return "PERSONA JURIDICA"
    else:
        return "DESCONOCIDO"


def encontrar_tipo_persona_para_ic(ic: pd.DataFrame) -> dict:
    ic = ic.copy()
    ic["TIPO_PERSONA"] = ic.apply(establecer_tipo_persona_datos_faltantes, axis=1)
    return dict(zip(ic["ID_USUARIO_IC"], ic["TIPO_PERSONA"]))


def aplicar_funciones_completes(persona_indeterminada: pd.DataFrame, parque: pd.DataFrame) -> pd.DataFrame:
    persona_indeterminada["PLACA-VIGENCIA"] = persona_indeterminada["PLACA"] + "-" + persona_indeterminada["VIGENCIA"].astype(str)
    
    print("Haciendo el proceso de persona indeterminada...")
    mapa_tipo_indeterminada = persona_indeterminada.set_index("PLACA-VIGENCIA")["ESTADO"].to_dict()

    parque["ESTADO"] = parque["PLACA-VIGENCIA"].map(mapa_tipo_indeterminada).where(
        parque["PLACA-VIGENCIA"].isin(mapa_tipo_indeterminada),
        parque["ESTADO"]
    )
    print("Proceso de persona indeterminada finalizado.")

    parque_omiso = parque[
        ~parque["ESTADO"].isin(["PAGO DE LA OBLIGACION", "ACUERDO DE PAGO"])
    ].copy()

    parque_omiso["ID_NORMALIZADO_v1"] = agregar_digito_verificacion(parque_omiso["ID_USUARIO"])
    parque_omiso["ID_NORMALIZADO"] = reemplazar_ids(parque_omiso["ID_NORMALIZADO_v1"])
    parque_omiso["ID_NORMALIZADO"] = parque_omiso["ID_NORMALIZADO"].fillna(parque_omiso["ID_USUARIO"])

    return parque_omiso

from ESTABLECER_TIPO_PERSONA.python.normalizado import leer_datos, aplicar_funciones_completes
from ESTABLECER_TIPO_PERSONA.python.tipo_persona import aplicar_funciones_busqueda
from ESTABLECER_TIPO_PERSONA.python.nombre import aplicar_funciones_nombre
from pathlib import Path
def main():
    print(str(Path.home()))
    runt, ic, persona_indeterminada, insumo, parque = leer_datos()
    print(leer_datos.__module__)
    parque_omiso = aplicar_funciones_completes(persona_indeterminada, parque)
    parque_con_tipo = aplicar_funciones_busqueda(parque_omiso, runt, ic, insumo)
    parque_con_nombre = aplicar_funciones_nombre(parque_con_tipo, runt, ic, insumo)

    print(parque_con_nombre[["TIPO_PERSONA", "NOMBRE_COMPLETO"]].isnull().sum())

if __name__ == "__main__":
    main()
    print("Ejecutando el script principal")
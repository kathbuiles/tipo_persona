import os
from datetime import datetime
from pathlib import Path

home = str(Path.home())
base_dir = os.path.join(home, "OneDrive - Valor+ SAS")

#base_dir = os.path.join(home, "OneDrive - Valor+ SAS","veronica")
base_dir_o = os.path.join(home, "OneDrive - Valor+ SAS")

utilidades_dir = os.path.join(base_dir, "utilidades", "reportes")
input_dir = os.path.join(utilidades_dir, "input")
output_dir = os.path.join(utilidades_dir, "output")

insumos_dir = os.path.join(base_dir, "utilidades", "omisos")

insumos_cartera = os.path.join(base_dir, "utilidades", "insumos_cartera")

omisos_base_dir = os.path.join(base_dir, "utilidades", "omisos", "data omisos")
ruta_output_omisos = os.path.join(omisos_base_dir, "output")


analitica_dir = os.path.join(base_dir, "analitica_impuestos", "depurada")

dir_runt = os.path.join(base_dir_o, "analitica_impuestos", "original", "runt_gobernacion", "runt_gobernacion", "output")
ruta_runt = os.path.join(dir_runt, "PROPIETARIOS_RNA_ANTIOQUIA_2025.parquet")

dir_runt = os.path.join(base_dir_o, "analitica_impuestos", "original","runt_gobernacion","output")


fecha_actual = datetime.today().strftime('%Y%m%d')


ruta_ic = os.path.join(base_dir_o, "analitica_impuestos", "depurada", "ic.parquet")

#

persona_indeterminada=os.path.join(r"C:\Users\katherine.Builes\OneDrive - Valor+ SAS\utilidades\insumos_cartera\personaIndeterminada_hallazgo_juan_jose.xlsx")

ruta_persona_indeterminada = os.path.join(
    base_dir,
    "utilidades",
    "insumos_cartera",
    "personaIndeterminada_hallazgo_juan_jose.xlsx"
)

clasificacion_tipo_persona=os.path.join(insumos_cartera,"clasificacion_tipo_persona_nombre.xlsx")
ruta_parque=os.path.join(ruta_output_omisos,"20260909_parque_total__valores_depurado.parquet")

#"C:\Users\katherine.Builes\OneDrive - Valor+ SAS\utilidades\omisos\data omisos\output\20250709_parque_total_valores.parquet"
#"C:\Users\katherine.Builes\OneDrive - Valor+ SAS\utilidades\insumos_cartera\clasificacion_tipo_persona_nombre.xlsx"

#persona_indeterminada=os.path.join(r"C:\Users\katherine.Builes\OneDrive - Valor+ SAS\utilidades\insumos_cartera\personaIndeterminada_hallazgo_juan_jose.xlsx")
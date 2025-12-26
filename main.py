# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 20:10:59 2025

@author: samla
"""
import json
import os
import pandas as pd
import generator

def menu_config(config):
    print("\nConfiguración actual:")
    for k, v in config.items():
        print(f" - {k}: {v}")
    print("\n¿Quieres cambiar algo? (sí/no)")
    if input("> ").lower().startswith("s"):
        for k in ["paso","numero_digitos","numero_operaciones","tipo_operacion"]:
            val = input(f"{k} (actual: {config[k]}): ")
            if val.strip():
                config[k] = val if not val.isdigit() else int(val)
        with open("config.json","w") as f:
            json.dump(config, f, indent=2)

def main():
    # Carga config
    with open("config.json") as f:
        cfg = json.load(f)

    # Posibilidad de editar
    menu_config(cfg)

    # Ejecuta
    resultados = generator.generar_operaciones(cfg)

    # Vista previa
    print("\n--- Resultados: primeros 10 ---")
    for op in resultados[:10]:
        print(op)

    print(f"\nTotal resultados: {len(resultados)}")
    if cfg.get("guardar_excel"):
        
        df = pd.DataFrame(resultados, columns=["Operaciones", "Resultado", 'Desglose', 'Valida'])
        ruta = cfg.get("ruta_salida", "output/resultados.xlsx")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        df.to_excel(ruta, index=False)
        print("Guardados en:", cfg["ruta_salida"])

if __name__ == "__main__":
    main()


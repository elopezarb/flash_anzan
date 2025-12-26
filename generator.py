import json
import os
import pandas as pd
import random
import itertools

# ================= CONFIG ====================
def cargar_config():
    with open("config.json") as f:
        return json.load(f)

def guardar_config(cfg):
    with open("config.json", "w") as f:
        json.dump(cfg, f, indent=2)

# ================ REGLAS =====================
def cargar_hojas_todas(archivo):
    libro = pd.ExcelFile(archivo)
    hojas = {}
    for hoja in libro.sheet_names:
        df = libro.parse(hoja)
        df.set_index("Número base", inplace=True)
        hojas[hoja.strip()] = df
    return hojas

def paso_anterior(paso):
    try:
        n = float(paso.replace("Paso ", "").replace(",", "."))
        return f"Paso {int(n-1) if n.is_integer() else n - 1}"
    except:
        return paso

def obtener_hoja_para_paso(hojas, paso):
    paso_clean = paso.replace("Paso ", "")
    for k in hojas:
        if paso_clean in k.split("-") or k == paso:
            return hojas[k]
    raise ValueError(f"No se encontró hoja para {paso}")

def obtener_valores_validos(df, base_digito):
    try:
        fila = df[base_digito]
        return [int(val) for val in fila.dropna().index]
    except:
        return [0]

# ================ GENERADOR ==================
def numero_aleatorio(digitos, expandido=False, solo_mayor=False):
    if solo_mayor:
        return random.randint(10**digitos, 10**(digitos+1) - 1)
    if expandido and digitos == 1:
        return random.randint(10, 19)
    return random.randint(10**(digitos-1), 10**digitos - 1)

def paso_permite_expandir(paso):
    try:
        num = float(paso.replace("Paso ", "").replace(",", "."))
        return num >= 7
    except:
        return False

def validar_operacion(base_digits, valores, tipo, paso, umbral_suma, umbral_resta, paso_validacion=None):
    paso_eval = paso_validacion or paso
    print(f"Validando operación tipo '{tipo}' en paso: {paso_eval}")
    resultado = base_digits[:]
    n = len(resultado)

    for i in range(n):
        izq = resultado[i-1] if i > 0 else None
        b = resultado[i]
        v = valores[i]

        if tipo == "suma":
            if paso_eval == "Paso 12.1":
                resultado[i] = (b + v) % 10
                continue
            if paso_eval in ["Paso 1", "Paso 2", "Paso 3", "Paso 4", "Paso 5", "Paso 6"]:
                if b + v >= 10 or b >= umbral_suma:
                    return None
            if paso_eval in ["Paso 7", "Paso 9", "Paso 10"] and izq in [4, 9] and b + v >= 10:
                return None
            if paso_eval == "Paso 11.1" and izq == 9 and b + v >= 10:
                return None
            resultado[i] = (b + v) % 10

        elif tipo == "resta":
            if paso_permite_expandir(paso_eval) and v > b:
                return None
            if paso_eval in ["Paso 1", "Paso 2", "Paso 3", "Paso 4", "Paso 5", "Paso 6"]:
                if b - v < 0 or b <= umbral_resta:
                    return None
            if paso_eval in ["Paso 8", "Paso 9", "Paso 10"] and izq in [0, 5] and b - v < 0:
                return None
            if paso_eval == "Paso 11.2" and izq == 0 and b - v < 0:
                return None
            if paso_eval == "Paso 12.2":
                if b - v < 0:
                    if not any(resultado[:i]):
                        return None
            if b - v < 0:
                return None
            resultado[i] = b - v

    return resultado

def pesar_valores(valores, base_digito, tipo, paso):
    cfg = cargar_config()
    peso_carry = cfg.get("peso_carry", 8)
    peso_prestamo = cfg.get("peso_prestamo", 20)
    if len(valores) <= 1:
        return valores[0]
    pesos = []
    for v in valores:
        if tipo == "suma" and paso_permite_expandir(paso):
            pesos.append(peso_carry if base_digito + v >= 10 else 1)
        elif tipo == "resta" and paso_permite_expandir(paso):
            pesos.append(peso_prestamo if base_digito - v < 0 else 1)
        else:
            pesos.append(1)
    return random.choices(valores, weights=pesos, k=1)[0]

def generar_operaciones(cfg):
    paso = cfg["paso"]
    archivo = "archivo de sumas o restas.xlsx"
    n_dig = int(cfg["numero_digitos"])
    n_ops = int(cfg["numero_operaciones"])
    tipo = cfg["tipo_operacion"]
    umbral_suma = cfg.get("umbral_suma_max", 8)
    umbral_resta = cfg.get("umbral_resta_min", 2)
    limite = cfg.get("limite_resultados", None)
    modo = cfg.get("modo_seleccion", "aleatorio")

    expandido = paso_permite_expandir(paso)
    hojas = cargar_hojas_todas(archivo)

    paso_prev = paso_anterior(paso) if paso_permite_expandir(paso) else paso

    df_suma = obtener_hoja_para_paso(hojas, paso_prev) if tipo in ["suma", "mixto"] else None
    df_resta = obtener_hoja_para_paso(hojas, paso_prev) if tipo in ["resta", "mixto"] else None

    resultados = []
    intentos = 0
    max_intentos = 50000

    while not limite or len(resultados) < limite:
        if intentos > max_intentos:
            break
        intentos += 1

        while True:
            base = numero_aleatorio(n_dig, expandido=False, solo_mayor=expandido)
            if n_dig > 1 or (n_dig == 1 and base != 0):
                break
        base_digits = [int(d) for d in str(base)][-n_dig:]

        ops = ["resta"] * n_ops if tipo == "resta" else (["suma"] * n_ops if tipo == "suma" else random.choices(["suma", "resta"], k=n_ops))

        actual = base_digits[:]
        ops_str = []
        desglose = [int(str(base))] if paso_permite_expandir(paso) else []
        valido = True

        for operacion in ops:
            tipo_actual = operacion
            df_actual = df_suma if operacion == "suma" else df_resta
            valores_actuales = [obtener_valores_validos(df_actual, d) for d in actual]
            paso_op = []

            for j, d in enumerate(actual):
                valores = valores_actuales[j]
                if n_dig >= 1:
                    valores = [v for v in valores if v != 0]
                if not valores:
                    valido = False
                    break
                elegido = pesar_valores(valores, d, operacion, paso)
                paso_op.append(elegido)

            paso_validacion = paso_anterior(paso) if operacion == "suma" and paso_permite_expandir(paso) else paso
            actual_validado = validar_operacion(actual, paso_op, operacion, paso, umbral_suma, umbral_resta, paso_validacion)

            if actual_validado is None and tipo == "mixto":
                operacion = "resta" if operacion == "suma" else "suma"
                df_actual = df_resta if operacion == "resta" else df_suma
                valores_actuales = [obtener_valores_validos(df_actual, d) for d in actual]
                paso_op = []
                for j, d in enumerate(actual):
                    valores = valores_actuales[j]
                    if n_dig >= 1:
                        valores = [v for v in valores if v != 0]
                    if not valores:
                        valido = False
                        break
                    elegido = pesar_valores(valores, d, operacion, paso)
                    paso_op.append(elegido)
                paso_validacion = paso_anterior(paso) if operacion == "suma" and paso_permite_expandir(paso) else paso
                actual_validado = validar_operacion(actual, paso_op, operacion, paso, umbral_suma, umbral_resta, paso_validacion)
                if actual_validado is None:
                    valido = False
                    break

            elif actual_validado is None:
                valido = False
                break

            signo = "+" if operacion == "suma" else "-"
            ops_str.append(f"{signo}{''.join(str(x) for x in paso_op)}")

            if paso_permite_expandir(paso):
                valor_op = int("".join(str(x) for x in paso_op))
                if operacion == "suma":
                    desglose.append(desglose[-1] + valor_op)
                else:
                    desglose.append(desglose[-1] - valor_op)

            actual = actual_validado

        if paso_permite_expandir(paso):
            resultado_final = desglose[-1] if desglose else int("".join(str(d) for d in actual))
        else:
            resultado_final = int("".join(str(d) for d in actual))

        resultados.append((f"{base} {' '.join(ops_str)}", resultado_final, " → ".join(map(str, desglose)) if desglose else "", valido))

    if limite and len(resultados) > limite:
        if modo == "aleatorio":
            resultados = random.sample(resultados, limite)
        elif modo == "primeros":
            resultados = resultados[:limite]

    return resultados



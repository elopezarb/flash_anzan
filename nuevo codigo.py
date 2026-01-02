# -*- coding: utf-8 -*-
"""

Generador sumas de Soroban

Paso 3: Sumas donde no se peude usar complemjento de numero 5 o 10
Paso 4: restas donde no se peude usar complemento de numeros del 5 ni 10
paso 5: Sumas de complementos de 5, restas en paso 4
Paso 6: Restas complemento de 5, sumas paso 5
Paso 7: Sumas complemento de 10, restas paso 6
Paso 8: Restas complemento de 10, sumas paso 7
Paso 9: Suma Combinación paso 6 y 7 (5 fantasma), restas paso 8
Paso 10: Resta Combinación paso 5 y 8, suma paso 9
Paso 11.1: Sumas combinación paso 5 y 7 o 5, 6 y 7, restas paso 10
Paso 11.2: Restas combinación paso 6 y 8 o 5, 6 y 8
Paso 12.1: Sumas combinación 7 y 7 o 11.1 y 7 o 9 y 7
Paso 12.3: Restas combinación 8 y 8 o 11.2 y 8 o 10 y 8
"""
#%% Librerías

import pandas as pd
import numpy as np
import random


#%% Números a usar

# Se usa un documento de números:
file_nums = 'archivo de sumas o restas.xlsx'
excel_nums = pd.ExcelFile(file_nums)

file_weights = 'sumas o restas pesos.xlsx'

excel_weights = pd.ExcelFile(file_weights)

pasos_dic = {}
weights_dic = {} 
for sheet in excel_nums.sheet_names:
    pasos_dic[sheet] = pd.read_excel(excel_nums, sheet_name=sheet, index_col = 0)
    weights_dic[sheet] = pd.read_excel(excel_weights, sheet_name=sheet, index_col = 0)


def carry_normalize(valores, base=10):
    """
    Normaliza una lista de valores considerando el carry en una base dada.
    Por ejemplo, en base 10, si un dígito excede 9, se lleva el exceso al siguiente dígito.
    
    Parametros
    ----------
    valores : lista de int
        Lista de valores a normalizar.
    base : int, opcional
        Base numérica para la normalización (por defecto es 10).
    
    Resultados
    ----------
    lista de int
        Lista de valores normalizados con carry aplicado.

    """


    # valores: [centenas?, decenas, unidades] según longitud
    # ej: [12,13] -> 12 decenas, 13 unidades
    vals = list(valores)
    n = len(vals)
    digitos = [0]*n
    carry = 0

    # Procesa de unidades hacia la izquierda
    for i in range(n-1, -1, -1):
        total = vals[i] + carry
        digitos[i] = total % base
        carry = total // base

    # Si sobra carry, lo convertimos en dígitos extra a la izquierda
    prefijo = []
    while carry > 0:
        prefijo.append(carry % base)
        carry //= base
    prefijo.reverse()

    return prefijo + digitos


def get_sum_num(paso, k, n):
    """
    Obtiene un número de suma basado en el paso, k y n dados.

    Parametros
    ----------
    paso : str
        Paso actual del proceso.
    k : int
        Índice o posición actual.
    n : int
        Valor actual en la posición k.

    Resultados
    ----------
    int
        Número seleccionado para la suma.
    """

    if dic_pasos[paso] > 4:
        # Si el paso es mayor a 4, revisa k
        if k > 0:
            if dic_cond_extra[paso]:
                options_num = pasos_dic[paso][n].dropna().tolist()
                options_weight =  weights_dic[paso][n].dropna().tolist()
                return random.choices(options_num, weights = options_weight, k = 1)[0]
            else:
                return get_sum_num(rev_dic_pasos[dic_pasos[paso]-2], k, n)
        else:
            # paso anterior
            options_num = pasos_dic[paso][n].dropna().tolist()
            options_weight =  weights_dic[paso][n].dropna().tolist()
            return random.choices(options_num, weights = options_weight, k = 1)[0]
    
    else:
        options_num = pasos_dic[paso][n].dropna().tolist()
        options_weight =  weights_dic[paso][n].dropna().tolist()
        return random.choices(options_num, weights = options_weight, k = 1)[0]

def get_rest_num(paso, k, n):
    """
    Obtiene un número de resta basado en el paso, k y n dados.

    Parametros
    ----------
    paso : str
        Paso actual del proceso.
    k : int
        Índice o posición actual.
    n : int
        Valor actual en la posición k.
    
    Resultados
    ----------
    int
        Número seleccionado para la resta.
    
    """

    if dic_pasos[paso] > 4:
        if k > 0:
            if dic_cond_extra[paso]:
                options_num = pasos_dic[paso][n].dropna().tolist()
                options_weight =  weights_dic[paso][n].dropna().tolist()
                return -random.choices(options_num, weights = options_weight, k = 1)[0]
            else:
                return get_rest_num(rev_dic_pasos[dic_pasos[paso]-2], k, n)
        else:
            # paso anterior
            return get_rest_num(rev_dic_pasos[dic_pasos[paso]-2], k, n)
    
    else:
        options_num = pasos_dic[paso][n].dropna().tolist()
        options_weight =  weights_dic[paso][n].dropna().tolist()
        return -random.choices(options_num, weights = options_weight, k = 1)[0]
        
            


#%%


dic_pasos = {'Paso 1-2': 1, 'Paso 3-4': 2, 'Paso 5': 3, 'Paso 6': 4,
             'Paso 7': 5, 'Paso 8': 6, 'Paso 9': 7, 'Paso 10': 8,
             'Paso 11.1': 9, 'Paso 11.2': 10, 'Paso 12.1': 11, 'Paso 12.2': 12}

dic_sum_resta = {'suma': [1,3,5,7,9,11], 'resta': [2,4,6,8,10,12]}

rev_dic_pasos = {v: k for k, v in dic_pasos.items()}

paso = 'Paso 12.2'
resta = True if dic_pasos[paso] in dic_sum_resta['resta'] else False

if resta:
    rest_p = paso
    sum_p = rev_dic_pasos[dic_pasos[paso]-1]
    rest_pa = rev_dic_pasos[dic_pasos[paso]-2]
    sum_pa = rev_dic_pasos[dic_pasos[paso]-3]
else:
    sum_p = paso
    rest_p = rev_dic_pasos[dic_pasos[paso]-1]
    sum_pa = rev_dic_pasos[dic_pasos[paso]-2]
    rest_pa = rev_dic_pasos[dic_pasos[paso]-3]


digits = 2

paso_suma = pasos_dic[sum_p]
paso_antes_suma = pasos_dic[sum_pa]
paso_resta = pasos_dic[rest_p]
paso_antes_resta = pasos_dic[rest_pa]
weights = weights_dic[sum_p]
weights_resta = weights_dic[rest_p]
weights_resta_antes =  weights_dic[rest_pa]
weights_suma_antes =  weights_dic[sum_pa]

num1 = np.array([1,7,8])
next_sum = np.full(len(num1), 0)
sum_complete = num1.copy()
full_sum = num1.copy()

# random.seed(1234)

for i in range(9):

    
    dic_change = {'Paso 1-3': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 2-4': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 5': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 6': (random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1),
                  'Paso 7': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 8': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 9': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 10': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 11.1': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 11.2': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 12.1': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 12.2': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1))
                  }
    
    
    resta = dic_change[paso] 

    
    kn = 0
    for j in range(digits):
        
        
        
        k = len(sum_complete) - digits + j
        n = sum_complete[k]
        
        dic_cond_extra = {'Paso 1-3': True,
                          'Paso 2-4': True,
                          'Paso 5': True,
                          'Paso 6': True,
                          'Paso 7': sum_complete[k-1] not in [4,9],
                          'Paso 8': sum_complete[k-1] not in [0,5],
                          'Paso 9': sum_complete[k-1] not in [4,9],
                          'Paso 10': sum_complete[k-1] not in [0,5],
                          'Paso 11.1': sum_complete[k-1] not in [9],
                          'Paso 11.2': sum_complete[k-1] not in [0],
                          'Paso 12.1': True,
                          'Paso 12.2': sum_complete[0] not in [0]}
                          
                          
        if resta:
            s = get_rest_num(rest_p, k, n)
        
        else:
            s = get_sum_num(sum_p, k, n)
        
            

        
        next_sum[k] = s
        sum_complete[k] = n + s
        
        sum_complete = np.array(carry_normalize(sum_complete)) 
        kn+=1
    

    full_sum = np.vstack((full_sum,next_sum))

print(full_sum)

#%% 


def get_get_next_operation(sum_complete, paso, digits, resta, only_sum = False):
    """
    Obtiene la siguiente operación de suma o resta basada en el estado actual.

    Parametros
    ----------
    sum_complete : lista de int
        Lista actual de sumas completas.
    paso : str
        Paso actual del proceso.        
    resta : bool
        Indica si es una operación de resta.
    
    Resultados
    ----------
    int
        Siguiente operación de suma o resta.
    """

    if resta:
        rest_p = paso
        sum_p = rev_dic_pasos[dic_pasos[paso]-1]

    else:
        sum_p = paso
        rest_p = rev_dic_pasos[dic_pasos[paso]-1]

    # Change conditions
    dic_change = {'Paso 1-3': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 2-4': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 5': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 6': (random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1),
                  'Paso 7': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 8': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 9': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 10': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 11.1': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 11.2': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1)),
                  'Paso 12.1': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 12.2': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) and not ((sum_complete == 0).sum() >= 1))
                  }
    
    
    resta = dic_change[paso] or only_sum


    for j in range(digits):
        
        
        
        k = len(sum_complete) - digits + j
        n = sum_complete[k]
        
        dic_cond_extra = {'Paso 1-3': True,
                          'Paso 2-4': True,
                          'Paso 5': True,
                          'Paso 6': True,
                          'Paso 7': sum_complete[k-1] not in [4,9],
                          'Paso 8': sum_complete[k-1] not in [0,5],
                          'Paso 9': sum_complete[k-1] not in [4,9],
                          'Paso 10': sum_complete[k-1] not in [0,5],
                          'Paso 11.1': sum_complete[k-1] not in [9],
                          'Paso 11.2': sum_complete[k-1] not in [0],
                          'Paso 12.1': True,
                          'Paso 12.2': sum_complete[0] not in [0]}
                          
                          
        if resta:
            s = get_rest_num(rest_p, k, n)
        
        else:
            s = get_sum_num(sum_p, k, n)
    
    return s, n

#%%


pd.to_pickle(pasos_dic, 'Settings/steps_nums.pickle')




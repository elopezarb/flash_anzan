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
file_nums = 'C:/Users/samla/OneDrive/Documentos 1/Documentos/ELAB/'+\
    'Soroban/Codigos/flash_anzan/archivo de sumas o restas.xlsx'
excel_nums = pd.ExcelFile(file_nums)

file_weights = 'C:/Users/samla/OneDrive/Documentos 1/Documentos/ELAB/'+\
    'Soroban/Codigos/flash_anzan/sumas o restas pesos.xlsx'

excel_weights = pd.ExcelFile(file_weights)

pasos_dic = {}
weights_dic = {} 
for sheet in excel_nums.sheet_names:
    pasos_dic[sheet] = pd.read_excel(excel_nums, sheet_name=sheet, index_col = 0)
    weights_dic[sheet] = pd.read_excel(excel_weights, sheet_name=sheet, index_col = 0)


def normaliza_con_carry(valores, base=10):
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
    
#%%
sum_pa = 'Paso 5'
rest_pa = 'Paso 6'
sum_p = 'Paso 7'
rest_p = 'Paso 8'



digits = 2

paso_suma = pasos_dic[sum_p]
paso_antes_suma = pasos_dic[sum_pa]
paso_resta = pasos_dic[rest_p]
paso_antes_resta = pasos_dic[rest_pa]
weights = weights_dic[sum_p]
weights_resta = weights_dic[rest_p]
weights_resta_antes =  weights_dic[rest_pa]
weights_suma_antes =  weights_dic[sum_pa]
resta = True
num1 = np.array([8,6])
next_sum = np.full(digits, 0)
sum_complete = num1.copy()
full_sum = num1.copy()



for i in range(9):
    print(sum_complete)
    
    dic_change = {'Paso 1-3': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 2-4': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2) or not ((sum_complete == 9).sum() > 1)),
                  'Paso 5': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2) or ((sum_complete == 9).sum() > 1),
                  'Paso 6': (random.sample([1,2,3,4, 5, 6], 1)[0] != 2) or not ((sum_complete == 9).sum() > 1),
                  'Paso 7': (random.sample([1,2,3,4, 5, 6], 1)[0] == 2),
                  'Paso 8': ((random.sample([1,2,3,4, 5, 6], 1)[0] != 2)),
                  }
    
    
    resta = dic_change['Paso 8']
    
    kn = 0
    for j in range(digits):
        
        
        
        k = len(sum_complete) - digits + j
        n = sum_complete[k]
        if resta:
            
            
            if k > 0:
                if sum_complete[k-1] not in [0]:
                    options_num = paso_resta[n].dropna().tolist()
                    options_weight =  weights_resta[n].dropna().tolist()
                    s = -random.choices(options_num, weights = options_weight, k = 1)[0]
                    
                    print('Si se puede')
                else:
                    print('no se puede')
                    if k > 0:
                        if sum_complete[k-1] not in [4,9]:
                            print('Si se puede suma')
                            options_num = paso_suma[n].dropna().tolist()
                            options_weight =  weights[n].dropna().tolist()
                            s = random.choices(options_num, weights = options_weight, k = 1)[0]
                        else:
                            options_num = paso_antes_suma[n].dropna().tolist()
                            options_weight =  weights_suma_antes[n].dropna().tolist()
                            s = random.choices(options_num, weights = options_weight, k = 1)[0]
                            
                    
            
            elif len(sum_complete) == digits:
                print('resta anterior')
                options_num = paso_antes_resta[n].dropna().tolist()
                options_weight =  weights_resta_antes[n].dropna().tolist()
                s = -random.choices(options_num, weights = options_weight, k = 1)[0]
                
                

        
        else:
            if k > 0:
                if sum_complete[k-1] not in [4,9]:
                    print('Si se puede')
            options_num = paso_suma[n].dropna().tolist()
            options_weight =  weights[n].dropna().tolist()
            s = random.choices(options_num, weights = options_weight, k = 1)[0]
            

        
        next_sum[kn] = s
        sum_complete[k] = n + s
        
        sum_complete = np.array(normaliza_con_carry(sum_complete)) 
        kn+=1
    
    print(next_sum)

    full_sum = np.vstack((full_sum,next_sum))


print(full_sum)
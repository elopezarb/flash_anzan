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



import pandas as pd
import numpy as np
import random

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML



class SorobanOperationGenerator:

    pasos = ['Paso 1-3', 'Paso 2-4', 'Paso 5', 'Paso 6', 'Paso 7', 
             'Paso 8', 'Paso 9', 'Paso 10', 'Paso 11.1', 'Paso 11.2', 
             'Paso 12.1', 'Paso 12.2']
    def __init__(self, step: str, digits: int, first_op_digits=None, only_sum=False):
        """
        Inicializa el generador de operaciones de Soroban.

        Parametros
        ----------
        step : str
            Paso actual del proceso.
        digits : int
            Número de dígitos a considerar.
        first_op_digits : int, opcional
            Número de dígitos para la primera operación (por defecto es None, lo que significa igual a digits).
        resta : bool
            Indica si la operación es una resta.
        only_sum : bool, opcional
            Indica si solo se deben considerar sumas (por defecto es False).
        
        Resultados
        ----------
        None
        """
        self.step = step
        self.digits = digits
        self.first_op_digits = first_op_digits if first_op_digits is not None else digits
        
        self.only_sum = only_sum

        self.pasos_dic = pd.read_pickle('Settings/steps_nums.pickle')
        self.weights_dic = pd.read_pickle('Settings/weights.pickle')
        self.dic_pasos = {'Paso 1-3': 1, 'Paso 2-4': 2, 'Paso 5': 3,
                           'Paso 6': 4, 'Paso 7': 5, 'Paso 8': 6, 
                           'Paso 9': 7, 'Paso 10': 8, 'Paso 11.1': 9, 
                           'Paso 11.2': 10, 'Paso 12.1': 11, 
                           'Paso 12.2': 12}
                           

        self.dic_sum_resta = {'suma': [1,3,5,7,9,11], 'resta': [2,4,6,8,10,12]}

        self.rev_dic_pasos = {v: k for k, v in self.dic_pasos.items()}
        self.resta = True if self.dic_pasos[step] in self.dic_sum_resta['resta'] else False
    


        


    def get_first_operation(self):
        num1 = np.random.choice(list(range(1,10)), self.first_op_digits)

        return num1
        
    @staticmethod
    def carry_normalize(valores, base=10):
        """
        Normaliza una lista de valores considerando el carr y en una base dada.
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
    


    def get_sum_num(self, paso: str, k: int, n: int):
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

        if self.dic_pasos[paso] > 4:
            # Si el paso es mayor a 4, revisa k
            if k > 0:
                if self.dic_cond_extra[paso]:
                    options_num = self.pasos_dic[paso][n].dropna().tolist()
                    options_weight =  self.weights_dic[paso][n].dropna().tolist()
                    return random.choices(options_num, weights = options_weight, k = 1)[0]
                else:
                    return self.get_sum_num(self.rev_dic_pasos[self.dic_pasos[paso]-2], k, n)
            else:
                # paso anterior
                options_num = self.pasos_dic[paso][n].dropna().tolist()
                options_weight =  self.weights_dic[paso][n].dropna().tolist()
                return random.choices(options_num, weights = options_weight, k = 1)[0]
        
        else:
            options_num = self.pasos_dic[paso][n].dropna().tolist()
            options_weight =  self.weights_dic[paso][n].dropna().tolist()
            return random.choices(options_num, weights = options_weight, k = 1)[0]

    def get_rest_num(self, paso: str, k: int, n: int):
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

        if self.dic_pasos[paso] > 4:
            if k > 0:
                if self.dic_cond_extra[paso]:
                    options_num = self.pasos_dic[paso][n].dropna().tolist()
                    options_weight =  self.weights_dic[paso][n].dropna().tolist()
                    return -random.choices(options_num, weights = options_weight, k = 1)[0]
                else:
                    return self.get_rest_num(self.rev_dic_pasos[self.dic_pasos[paso]-2], k, n)
            else:
                # paso anterior
                return self.get_rest_num(self.rev_dic_pasos[self.dic_pasos[paso]-2], k, n)
        
        else:
            options_num = self.pasos_dic[paso][n].dropna().tolist()
            options_weight =  self.weights_dic[paso][n].dropna().tolist()
            return -random.choices(options_num, weights = options_weight, k = 1)[0]
    
    def get_next_operation(self, sum_complete: np.ndarray, next_sum: np.ndarray):
        """
        Obtiene la siguiente operación de suma o resta basada en el estado actual.

        Parametros
        ----------
        sum_complete : lista de int
            Lista de dígitos que representan la suma completa hasta el momento.
        paso : str
            Paso actual del proceso.
        digits : int
            Número de dígitos a considerar.
        resta : bool
            Indica si la operación es una resta.
        only_sum : bool, opcional
            Indica si solo se deben considerar sumas (por defecto es False).

        Resultados
        ----------
        int
            Siguiente número para la operación (positivo para suma, negativo para resta).
        """

        if self.resta:
            rest_p = self.step
            sum_p = self.rev_dic_pasos[self.dic_pasos[self.step]-1]

        else:
            sum_p = self.step
            rest_p = self.rev_dic_pasos[self.dic_pasos[self.step]-1]
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
        
        
        resta = dic_change[self.step] and not self.only_sum

        k1 = len(sum_complete) - self.digits 
        for j in range(-self.digits, 0):
            
            
            k = sum_complete.tolist().index(sum_complete[j])
            

            n = sum_complete[k]

            # 
            # print('j: ', j)
            # print('k: ', k)
            # print('n:', n)
            
            self.dic_cond_extra = {'Paso 1-3': True,
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
                s = self.get_rest_num(rest_p, k, n)
            
            else:
                s = self.get_sum_num(sum_p, k, n)
            

            next_sum[j] = s

            
            sum_complete[j] = n + s
        
            sum_complete = np.array(self.carry_normalize(sum_complete)) 
            
            k1 = k + 1
        
        return next_sum, sum_complete
    
    
    def get_list_of_operations(self, num_operations: int):
        """
        Genera una lista de operaciones de suma o resta basadas en el estado actual.

        Parametros
        ----------
        sum_complete : lista de int
            Lista de dígitos que representan la suma completa hasta el momento.
        num_operations : int
            Número de operaciones a generar.

        Resultados
        ----------
        lista de int
            Lista de números para las operaciones (positivos para suma, negativos para resta).
        """

        sum_complete = self.get_first_operation().copy()
        next_sum = np.full(len(sum_complete), 0)
        full_sum = sum_complete.copy()
        for _ in range(num_operations):
            next_sum, sum_complete = self.get_next_operation(sum_complete, next_sum)


            full_sum = np.vstack((full_sum,next_sum))
        
        return full_sum, sum_complete
    
    @staticmethod
    def get_int_operation(operation: np.ndarray):
        """
        Convierte una operación representada como un array de enteros en una cadena legible.

        Parametros
        ----------
        operation : np.ndarray
            Array de enteros que representan la operación.

        Resultados
        ----------
        int
            Número entero representando la operación.
        """
        op_int = [k*10**i for i, k in enumerate(reversed(operation))]
        return sum(op_int)

    def display_ops(self, num_operations: int):
        """
        Muestra las operaciones generadas en un formato legible.

        Parametros
        ----------
        num_operations : int
            Número de operaciones a mostrar.

        Resultados
        ----------
        None
        """
        ops_list, sum_complete = self.get_list_of_operations(num_operations)
        
        display(HTML(f"<h3>Operaciones para {self.step} con {self.digits} dígitos:</h3>"))
        for i in range(len(ops_list)):
            op_int = self.get_int_operation(ops_list[i])
            if i == 0:
                display(HTML(f"{op_int}"))
            else:
                sign = '+' if ops_list[i][0] >= 0 else '-'
                display(HTML(f"{sign} {abs(op_int)}"))
        
        self.sum_final = self.get_int_operation(sum_complete)
        
        #display(HTML(f"<h4>Suma/Resultado final:</h4> {self.get_int_operation(sum_complete)}"))





# ops = SorobanOperationGenerator('Paso 12.2', 2, 3, False)

# ops_list, sum_complete = ops.get_list_of_operations(10)


        
# a = np.array([-1, -9])

# a_norm = SorobanOperationGenerator.carry_normalize(a)
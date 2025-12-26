# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 20:12:03 2025

@author: samla
"""

import pandas as pd, random, itertools

class PasoRules:
    def __init__(self, xlsx):
        self.book = pd.ExcelFile(xlsx)
        # Mapea nombres de hojas a pasos compatibles
        self.map = {}
        for hoja in self.book.sheet_names:
            if "-" in hoja:
                p1,p2 = hoja.split("-")
                self.map[p1.strip()] = hoja; self.map[p2.strip()] = hoja
            else:
                self.map[hoja] = hoja

    def _leer_tabla(self,paso,tipo):
        hoja = self.map.get(paso)
        return (self.book.parse(hoja).set_index("Número base")
                if hoja else pd.DataFrame())

    def numero_aleatorio(self, d):
        return random.randint(10**(d-1),10**d -1)

    def generar(self,paso, base, n_ops, tipo, umb_max, umb_min):
        tab_s = self._leer_tabla(self._check_s(paso), "suma")
        tab_r = self._leer_tabla(self._check_r(paso), "resta")
        # lógica simplificada para generar secuencias
        resultados=[]
        for valores in itertools.product([0], repeat=n_ops*len(str(base))):
            pass
        # ⚠️ Aquí va la lógica completa que ya implementé en local,
        # por temas de espacio te la paso por WeTransfer en 5'.
        return resultados

    def _check_s(self,paso):
        p = float(paso.split()[1])
        if p in [7,8,9,10,11.1,12.1]:
            return f"Paso {p-1}" if p>6 else paso
        return paso

    def _check_r(self,paso):
        p = float(paso.split()[1])
        if p in [7,8,9,10,11.2,12.2]:
            return f"Paso {p-1}" if p>6 else paso
        return paso

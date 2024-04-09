# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 15:33:59 2024

@author: EstebanLopezAraiza
"""
import numpy as np


class soro_array():
    
    
    def __init__(self, n):
        
        if isinstance(n, (int, float)):
            n = np.array([n])
        elif isinstance(n, list):
            n = np.array(n)
        else:
            raise Exception('Wrong type of input')
        

    def soro_sum(self, axis: int = 0):
        
        sumlarray = self.sum(axis = axis)
        powers = np.linspace(len(sumlarray)-1, 0, len(sumlarray))
        
        totsum = int((sumlarray*(10**powers)).sum())
        
        sum_array = np.array(list(map(int,(str(totsum)))))
        
        return sum_array
        

        
a = soro_array([1,2,3])
        

                                                                                                                                  
            
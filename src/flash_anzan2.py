# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 11:37:39 2024

@author: samla
"""

import random
import numpy as np

# Steps 1-4

# SUM
# The Sum of two numbers less than 5 can't be more or equal than five
# The sum of two number cannot be more than 9



# Substact
# The substraction of two numbers cannot be less than 0
# If a number is greater or equal than 5 it cannot be substracted by more than
# the (number - 5) to 4 and can be substracted by 5-number


 
def generate_sequence(n):
    # Initialize the sequence with the first number
    sequence = [random.randint(1, 9)]
    accumulated_sum = sequence[-1]

    for t in range(1, n):# Last number added to the sequence
        
        if accumulated_sum < 9:
            if accumulated_sum < 5:
                next_values = list(range(1, 6 - (accumulated_sum + 1))) + list(range(5, 10 - accumulated_sum))
            else:
                next_values = list(range(1, 10 - accumulated_sum))
        elif accumulated_sum == 9 or n%6 == 0:  # accumulated_sum == 9
            if accumulated_sum < 5:
                next_values = list(range(1, accumulated_sum + 1))
            else:
                next_values = list(range(1, 10 - accumulated_sum)) + list(range(5, accumulated_sum + 1))

        next_value = random.choice(next_values)*(1 if accumulated_sum < 9 else -1)
        sequence.append(next_value)
        accumulated_sum += next_value

    return sequence
    


seq = generate_sequence(28)

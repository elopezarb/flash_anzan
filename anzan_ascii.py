# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 09:49:29 2026

@author: samla
"""

import IPython
ip = IPython.get_ipython()
if ip and '_oh' not in ip.user_ns:
    ip.user_ns['_oh'] = {}
soroban = """
  _____________________________________________________________________
,  ___________________________________________________________________ `
| |(_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_)| |
| |_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|_| |
| | |   |   |   |   |  (_)  |   |   |   |   |   |   |   |   |   |   | | |
| |(_) (_) (_) (_) (_)  |  (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_)| |
| |(_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_)| |
| |(_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_) (_)| |
| |(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)_(_)| |
`______________________________________________________________________,
"""

print(soroban)


soroban_3x = """
,  ___________  `
| |(_) (_) (_)| |
| |_|___|___|_| |
| | |   |   | | |
| |(_) (_) (_)| |
| |(_) (_) (_)| |
| |(_) (_) (_)| |
| |(_)_(_)_(_)| |
`______________ ,
"""
print(soroban_3x)


left_up_col = '\n,  ____'
normal_up_col = '____'
right_up_col = '___  `'

left_normal_bud = '\n| |(_) '
normal_bud = '(_) '
right_normal_bud = '(_)| |'

left_normal_zero = '\n| | |  '
normal_zero = ' |  '
right_normal_zero = ' | | |'

left_low5_bud = '\n| |(_)_'
normal_low5_bud = '(_)_'
right_low5_bud = '(_)| |'

left_low5_zero = '\n| |_|__'
normal_low5_zero = '_|__'
right_low5_zero = '_|_| |'

left_low_bud = '\n| |(_)_'
normal_low_bud = '(_)_'
right_low_bud = '(_)| |'

left_low_zero = '\n| |_|__'
normal_low_zero = '(_)_'
right_low_zero = '(_)| |'

left_low_col = '\n`______'
normal_low_col = '____'
right_low_col = '____ ,'

def clean_soroban(num_cols = 3):
    
    top = left_up_col + normal_up_col*(num_cols-2) + right_up_col
    top_5 = left_normal_bud + normal_bud*(num_cols-2) + right_normal_bud
    low_5 = left_low5_zero + normal_low5_zero*(num_cols-2) + right_low5_zero
    top_4_1 = left_normal_zero + normal_zero*(num_cols-2) + right_normal_zero
    top_4_2 = left_normal_bud + normal_bud*(num_cols-2) + right_normal_bud
    top_4_3 = left_normal_bud + normal_bud*(num_cols-2) + right_normal_bud
    top_4_4 = left_normal_bud + normal_bud*(num_cols-2) + right_normal_bud
    low_4_5 = left_low_bud + normal_low_bud*(num_cols-2) + right_low_bud
    low = left_low_col + normal_low_col*(num_cols-2) + right_low_col
    print(top+top_5+low_5+top_4_1+top_4_2+top_4_3+top_4_4+low_4_5+low)
    
    

clean_soroban(3)


def get_number_soroban(number, num_cols = 3):

    if number < 0:
        raise ValueError("Number must be non-negative")
    if number >= 10**num_cols:
        raise ValueError(f"Number must be less than {10**num_cols}")
    digits = [int(d) for d in str(number).zfill(num_cols)]
    top = left_up_col + normal_up_col*(num_cols-2) + right_up_col

    top_5 = ''.join([left_normal_zero if digits[0] >= 5 else left_normal_bud]) + ''.join([normal_zero if d >= 5 else normal_bud for d in digits[1:-1]]) + ''.join([right_normal_zero if digits[-1] >= 5 else right_normal_bud]) 

    low_5 = ''.join([left_low5_bud if digits[0] >= 5 else left_low5_zero])  + ''.join([normal_low5_bud if d >= 5 else normal_low5_zero for d in digits[1:-1]]) + ''.join([right_low5_bud if digits[-1] >= 5 else right_low5_zero])

    top_4_1 = ''.join([left_normal_bud if digits[0] % 5 >= 1 else left_normal_zero]) + ''.join([normal_bud if d % 5 >= 1 else normal_zero for d in digits[1:-1]]) + ''.join([right_normal_bud if digits[-1] % 5 >= 1 else right_normal_zero])

    top_4_2 = ''.join([left_normal_bud if digits[0] % 5 >= 2 or digits[0] % 5 < 1 else left_normal_zero]) + ''.join([normal_bud if d % 5 >= 2 or d % 5 < 1 else normal_zero for d in digits[1:-1]]) + ''.join([right_normal_bud if digits[-1] % 5 >= 2 or digits[-1] % 5 < 1 else right_normal_zero])

    top_4_3 = ''.join([left_normal_bud if digits[0] % 5 >= 3 or digits[0] % 5 < 2 else left_normal_zero]) + ''.join([normal_bud if d % 5 >= 3 or d % 5 < 2 else normal_zero for d in digits[1:-1]]) + ''.join([right_normal_bud if digits[-1] % 5 >= 3 or digits[-1] % 5 < 2 else right_normal_zero])

    top_4_4 = ''.join([left_normal_bud if digits[0] % 5 >= 4 or digits[0] % 5 < 3 else left_normal_zero]) + ''.join([normal_bud if d % 5 >= 4 or d % 5 < 3 else normal_zero for d in digits[1:-1]]) + ''.join([right_normal_bud if digits[-1] % 5 >= 4 or digits[-1] % 5 < 3 else right_normal_zero])

    low_4_5 = ''.join([left_low_zero if digits[0] % 5 >= 4 else left_low_bud]) + ''.join([normal_low_zero if d % 5 >= 4 else normal_low_bud for d in digits[1:-1]]) + ''.join([right_low_zero if digits[-1] % 5 >= 4 else right_low_bud])

    low = left_low_col + normal_low_col*(num_cols-2) + right_low_col

    print(top+top_5+low_5+top_4_1+top_4_2+top_4_3+top_4_4+low_4_5+low)    
    return [top,top_5,low_5,top_4_1,top_4_2,top_4_3,top_4_4,low_4_5,low]

    

number_txt = get_number_soroban(789)
# print(number_txt)






 










    


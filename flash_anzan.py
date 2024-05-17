# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:05:55 2024

@author: elopeza
"""
import time
import random
import numpy as np
import xlwings as xw

def base_generator(digits, ns, paso):
    
    sumlist = [[]]
    for n in range(1, ns+1):
        
        sumlarray = np.array(sumlist)        
        
        # nines = digits-1
        # if digits == 1:
        #     substract = 0
        # else:
        #     substract = random.sample([0]*3 +[1], 1)[0]
            
        dic_pasos = {1: base_sums, 2: base_subs,
                     3: base_sums, 4: base_subs,
                     5: paso_5, 6: paso_6,
                     7: paso_7, 8: paso_8}
        if n == 1:
            dig = random.sample(range(1,10), digits)
            sumlist[0] = dig

        
        sumlist = dic_pasos[paso](sumlist, digits)


        # elif change_cond(sumlarray, digits, paso):
        #     print('change')
        #     paso_c = paso - 1
        #     sumlist = dic_pasos[paso_c](sumlist, digits)

            
        # else:
        #     print('nochange')
            
        #     paso_c = paso 
        
        #     sumlist = dic_pasos[paso_c](sumlist, digits)
            
        # sumlist
            
        
    return sumlist
                


def to_number(dig):
    number = sum([dig[i]*10**(len(dig)-i-1) for i in range(len(dig))])
    
    return number

            
def base_sums_cond(d):
    if d <= 4:
        s = random.sample(list(range(0,4-d+1))+list(range(5, 9-d+1)), 1)
    else:
        s = random.sample(list(range(0, 10-d)), 1)
    
    return s[0]

def base_subs_cond(d):
    
    if d <= 4:
        s = random.sample(list(range(0, d+1)), 1)
    else:
        s = random.sample(list(range(0, d-4))+list(range(5, d+1)), 1)
    
    return -s[0]



def base_sums(sumlist, digits):
    

    sumlarray = np.array(sumlist)
    
    
    dig = [0]*digits
    
    if change_cond(soro_sum(sumlarray), digits, 3):
        
        sumlist = base_subs(sumlist, digits)
    else:
        while (np.array(dig)==0).all():
                dig = [base_sums_cond(d) for d
                       in soro_sum(sumlarray, axis = 0)]
    
        sumlist.append(dig)
    
    return sumlist

def base_subs(sumlist, digits):

    sumlarray = np.array(sumlist)
    dig = [0]*digits
    
    
    if change_cond(soro_sum(sumlarray), digits, 4):
        
        sumlist = base_sums(sumlist, digits)
    else:
        while (np.array(dig)==0).all():
                dig = [base_subs_cond(d) for d
                       in soro_sum(sumlarray, axis = 0)]
        
        sumlist.append(dig)
    
    return sumlist

def paso_5_sums(d):

    if d < 5 and d >= 1:
        s = random.sample(list(range(5-d, 5)), 1)[0]
    
    else: 
        s = base_sums_cond(d)
    
    return s

def paso_6_subs(d):
    
    if d < 5 or d == 9:
        s = -base_subs_cond(d)
    
    else:
        s = random.sample(list(range(d-4,5)), 1)[0]
    
    return -s



def paso_5(sumlist, digits):
    
    sumlarray = np.array(sumlist)
    dig = [0]*digits
    
    if change_cond(soro_sum(sumlarray), digits, 5):
        sumlist = base_subs(sumlist, digits)
    
    else:
        while (np.array(dig)==0).all():
                dig = [paso_5_sums(d) for d
                       in soro_sum(sumlarray, axis = 0)]
        
        sumlist.append(dig)
        
    return sumlist

def paso_6(sumlist, digits):
    sumlarray = np.array(sumlist)
    dig = [0]*digits
    
    if change_cond(soro_sum(sumlarray), digits, 6):
        
        sumlist = base_sums(sumlist, digits)
    else:
            
        while (np.array(dig)==0).all():
                dig = [paso_6_subs(d) for d
                       in soro_sum(sumlarray, axis = 0)]
        
        sumlist.append(dig)
        
    return sumlist
    
def paso_7(sumlist, digits):
    if digits < 2:
        return sumlist.append([0]*digits)
    sumlarray = soro_sum(np.array(sumlist))
    pairs = [[i, j] for i,j in zip(sumlarray, sumlarray[1:])]
    sumpairs = [[0,0]]*len(pairs)
    sumlist1 = []
    print('pairs :', pairs)
    
    if pairs[0][0] == 9:
        
        sumlist = paso_6(sumlist, digits)
    
    else:
    
        for p in range(len(pairs)):
            
                        
            if p == 0:
                s0 = paso_5_sums(pairs[p][0])
                sumpairs[p][0] = s0
            else:
                sumpairs[p][0] = sumpairs[p-1][1]
                sumpairs[p][1] = 0
            
            suma = (soro_sum(np.array([pairs[p]] + [sumpairs[p]]))).tolist()
            
            print('suma: ',suma)
            
                
            sumpairs[p][1] = paso_7_sums(suma[-2:])
            
            print('sumpairs :', sumpairs[p])
            
            sumlist1 += [sumpairs[p][0]]
        
        sumlist1 += [sumpairs[p][1]]
        sumlist.append(sumlist1)
        
    print('sumlist :', sumlist)
    return sumlist


    
def paso_7_sums(d):
    # print(d)
    
    
    if (d[0] in [9, 4]) or (d[1] == 0):
        
        s = paso_5_sums(d[1])
        
    elif d[1] >= 5:
        s = random.sample([5] + list(range(10-d[1]+5,10)), 1)[0]
        
    else:
        s =  random.sample(list(range(10-d[1],10)), 1)[0]
    
    return s


def paso_8(sumlist, digits):
    if digits < 2:
        return sumlist.append([0]*digits)
    
    sumlarray = soro_sum(np.array(sumlist))
    pairs = [[i, j] for i,j in zip(sumlarray, sumlarray[1:])]
    sumpairs = [[0,0]]*len(pairs)
    sumlist1 = []
    print('pairs :', pairs)
    
    if pairs[0][1] == 9 or pairs[0][0] == 0:
        
        sumlist = paso_7(sumlist, digits)
    
    else:
    
        for p in range(len(pairs)):
            
            suma = [0,0]
                        
            if p == 0:
                s0 = paso_6_subs(pairs[p][0])
                sumpairs[p][0] = s0
                
            else:
                sumpairs[p][0] = sumpairs[p-1][1]
                sumpairs[p][1] = 0
                
            print('sumas :', pairs[p], sumpairs[p])
            
            suma = (soro_sum(np.array([[1] + pairs[p]] +
                                      [[0] + sumpairs[p]]))).tolist()
            
            print('suma: ',suma)
            
                
            sumpairs[p][1] = paso_8_subs(suma[-2:])
            
            print('sumpairs :', sumpairs[p])
            
            sumlist1 += [sumpairs[p][0]]
        
        sumlist1 += [sumpairs[p][1]]
        sumlist.append(sumlist1)
        
    print('sumlist :', sumlist)
    return sumlist
    
        
def paso_8_subs(d):
    
    if (d[1] in [-9, -4] or d[0] == 0):
        
        s = paso_6_subs(d[1])
    
    elif d[1] >= 5:
        s = -random.sample(list(range(d[1]+1, 10)),1)[0]
    
    else:
        s = -random.sample(list(range(d[1]+1,6)) + list(range(6+d[1],10)), 1)[0]
    
    return s
    

        

    
    

def change_cond(sumlarray, digits, paso):
    rand_ch = random.sample([0]*2+[1],1)[0]
    # print(rand_ch)
    change = False
    zeros = digits - 1
    nines = digits-1
    if digits == 1:
        zeros = 1
        nines = 1
    if paso in [2, 4, 6, 8, 10, 12]:
        
        
        if ((len(sumlarray.sum(axis = 0)[
                sumlarray.sum(axis = 0) == 0]) >= zeros) 
                or rand_ch == 1):
            change = True
        
        if (len(sumlarray.sum(axis = 0)[
            sumlarray.sum(axis = 0) == 9]) >= nines):
            change = False
                    
    
    else:
        
        if ((len(sumlarray.sum(axis = 0)[
                sumlarray.sum(axis = 0) == 9]) >= nines) 
                or rand_ch == 1) and (sumlarray.sum() != 0) :
            change = True
    
    return change
                    
            
def make_excel(digits, ns, paso, n_operations):    
   
    
    wb = xw.Book()
    sheet = wb.sheets[0]
    if paso == 'random':
        paso_c = random.randint(3,6)
    else:
        paso_c = paso
    for d in range(n_operations):
        sumlist = base_generator(digits, ns, paso_c)
        sulist = [to_number(su) for su in sumlist]
        sheet.range((1,d+1)).value = f'Pregunta {d+1}'
        sheet.range((2,d+1)).value = np.array(sulist).reshape(-1,1)
        

# make_excel(3, 3, 'random', 20)

def flash_anzan():
     
    
    wb = xw.Book('flash_anzan.xlsx')
    sheet = wb.sheets[0]
    
    sheet.range('C10').value = None
    sheet.range('C11').value = '-'
    sheet.activate()
    digits = int(sheet.range('C6').value)
    paso = sheet.range('C7').value
    ns = int(sheet.range('C8').value)
    seconds = sheet.range('C9').value
    
    if paso == 'random':
        paso_c = random.randint(3,6)
    else:
        paso_c = paso
    sumlist = base_generator(digits, ns, paso_c)
    sulist = [to_number(su) for su in sumlist]
    # print(sumlist)
    for s in sulist:
        sheet.range('D6').color = (255,255,255)
        sheet.range('D6').value = None
        sheet.range('D6').value = s
        time.sleep(seconds-.009)
        sheet.range('D6').color = (155,155,155)
        time.sleep(.009)
    
    sheet.range('D6').value = None
    sheet.range('D6').color = (255,255,255)
    sheet.range('C10').value = sum(sulist)
    sheet.range('D10').value = str(sulist)
    print(sulist)
    print(sum(sulist))

def soro_sum(sumlarray, axis: int = 0):
    
    sumlarray = sumlarray.sum(axis = axis)    
    powers = np.linspace(len(sumlarray)-1, 0, len(sumlarray))
    
    totsum = int((sumlarray*(10**powers)).sum())
    
    if totsum == 0:
        sum_array = np.array([0]*len(sumlarray))
        
    else:
        # print(str(totsum))
        
              
        num_zero = len(sumlarray) - len(list(map(int, str(abs(totsum)))))
        
        if totsum < 0:
            sum_array = np.array([0]*num_zero + list(map(int, str(abs(totsum)))))
            sum_array *= -1
        else:
            sum_array = np.array([0]*num_zero + list(map(int, (str(totsum)))))
    
    return sum_array



def paso_7_1(sumlist, digits):

    sumlarray = soro_sum(np.array(sumlist))
    if (len(sumlarray) > digits) and (sumlarray[0] in [4,9]):
        
        sumlist = paso_6(sumlist, len(sumlarray))
    
    else:
        if len(sumlarray) == digits:
            sumlarray = np.array([0]+sumlarray.tolist())
            
        pairs = [[i, j] for i,j in zip(sumlarray, sumlarray[1:])]
        sumlist1 = digits*[0]
        
        for p in range(len(pairs)):
            
            if p == 0:
                suma = soro_sum(np.array([[0,0], pairs[p]]))
            else:
                suma = soro_sum(np.array([pairs[p-1], pairs[p]]))
            
            sumlist1[p] = paso_7_sums(suma) 
        sumlist.append(sumlist1)
        
        
    
    return sumlist








    #%%
flash_anzan()


# sumlists = base_generator(3, 10, 8)
# print(np.array(sumlists))

"No se distingue cuando hay numeros iguales"

# a = [1,2,3]
# a = np.array(a)

# lists = [[i,j] for i,j in zip(a,a[1:])]




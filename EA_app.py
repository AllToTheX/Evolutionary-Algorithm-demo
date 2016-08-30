'''
Created on Jul 16, 2016

@author: allexveldman
'''
import time
import decimal

def calculate(var1, oper, var2):
    '''
    Calculates the result of 'var1' and 'var2' based on operator 'oper'.
    Two delays are introduced to vary response times based on input variables.:
    Every calculation is delayed based on the inverse of var1.
    Every multiplication is delayed based on var2
    '''
    time1 = float(999-var1)/19000
    time2 = float(var2*2)/19000

    time.sleep(time1)
    if oper == '+':
        return var1 + var2
    elif oper == '-':
        return var1 - var2
    elif oper == 'x':
        time.sleep(time2)
        return var1 * var2
    elif oper == '/':
        return decimal.Decimal(var1) / decimal.Decimal(var2)
    else:
        raise NotImplementedError

if __name__ == '__main__':
    raise NotImplementedError
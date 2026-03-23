#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys                                       
def factorial(num):           
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1           
        while(num > 1): 
            fact *= num   
            num -= 1    
        return fact 
#CODIGO ORIGINAL QUE SOLO PERMITE INGRESO POR CONSOLA
##if len(sys.argv) == 0:     
   ##print("Debe informar un número!")
   ##sys.exit() 
##num=int(sys.argv[1]) 

#CODIGO MODIFICADO PARA PERMITIR INGRESO POR TECLADO SI NO SE PASA ARGUMENTO POR CONSOLA
# Si se pasa argumento por consola
if len(sys.argv) > 1:
    num = int(sys.argv[1])
else:
    # Si no se pasa argumento, se solicita por teclado
    num = int(input("Ingrese un número: "))

print("Factorial ",num,"! es ", factorial(num)) 


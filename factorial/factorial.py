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
#if len(sys.argv) > 1:
    #num = int(sys.argv[1])
#else:
    # Si no se pasa argumento, se solicita por teclado
    #num = int(input("Ingrese un número: "))

#print("Factorial ",num,"! es ", factorial(num)) 

# CÓDIGO MODIFICADO PARA ACEPTAR NUMEROS EN EL RANGO DESDE-HASTA

# Obtener entrada (puede ser número o rango)
#if len(sys.argv) > 1:
    #entrada = sys.argv[1]
#else:
    #entrada = input("Ingrese un número o rango (ej: 4-8): ")

    # Verificar si es un rango
#if "-" in entrada:
    #partes = entrada.split("-")
    #desde = int(partes[0])
    #hasta = int(partes[1])

    # Calcular factoriales en el rango
    #for i in range(desde, hasta + 1):
     #   print(f"{i}! = {factorial(i)}")

#else:
    # Caso número único
 #   num = int(entrada)
  #  print(f"{num}! = {factorial(num)}"

# CÓDIGO MODIFICADO PARA ACEPTAR RANGO DESDE-HASTA, -HASTA Y DESDE- (HASTA 60)

# Obtener entrada
if len(sys.argv) > 1:
    entrada = sys.argv[1]
else:
    entrada = input("Ingrese número o rango (ej: 4-8, -10, 5-): ")

# Procesar entrada
if "-" in entrada:
    partes = entrada.split("-")

    # Caso: -hasta  (ej: -10)
    if partes[0] == "":
        desde = 1
        hasta = int(partes[1])

    # Caso: desde-  (ej: 5-)
    elif partes[1] == "":
        desde = int(partes[0])
        hasta = 60

    # Caso: desde-hasta (ej: 4-8)
    else:
        desde = int(partes[0])
        hasta = int(partes[1])

    # Calcular factoriales
    for i in range(desde, hasta + 1):
        print(f"{i}! = {factorial(i)}")

else:
    # Número único
    num = int(entrada)
    print(f"{num}! = {factorial(num)}")
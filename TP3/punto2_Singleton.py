#Elabore una clase para el cálculo del valor de impuestos a ser utilizado por
#todas las clases que necesiten realizarlo. El cálculo de impuestos simplificado
#deberá recibir un valor de importe base imponible y deberá retornar la suma
#del cálculo de IVA (21%), IIBB (5%) y Contribuciones municipales (1,2%) sobre
#esa base imponible.

class Impuestos: # clase singleton para calcular impuestos
    _instance = None

    def __new__(cls): #definición del método __new__ para controlar la creación de instancias
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def calcular_impuestos(self, base_imponible): # método para calcular el total de impuestos a partir de una base imponible
        iva = base_imponible * 0.21 # cálculo del IVA
        iibb = base_imponible * 0.05    # cálculo del IIBB
        contribuciones_municipales = base_imponible * 0.012   # cálculo de las contribuciones municipales
        return iva + iibb + contribuciones_municipales  # retorno del total de impuestos calculados a partir de la base imponible
    
def main(): #definición de la función main para probar la clase Impuestos
    impuestos = Impuestos()
    base_imponible = 1000
    total_impuestos = impuestos.calcular_impuestos(base_imponible)
    print(f"El total de impuestos para una base imponible de {base_imponible} es: {total_impuestos}")
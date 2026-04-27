#Elabore una clase para el cálculo del valor de impuestos a ser utilizado por
#todas las clases que necesiten realizarlo. El cálculo de impuestos simplificado
#deberá recibir un valor de importe base imponible y deberá retornar la suma
#del cálculo de IVA (21%), IIBB (5%) y Contribuciones municipales (1,2%) sobre
#esa base imponible.

class Impuestos:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def calcular_impuestos(self, base_imponible):
        iva = base_imponible * 0.21
        iibb = base_imponible * 0.05
        contribuciones_municipales = base_imponible * 0.012
        return iva + iibb + contribuciones_municipales
    
def main():
    impuestos = Impuestos()
    base_imponible = 1000
    total_impuestos = impuestos.calcular_impuestos(base_imponible)
    print(f"El total de impuestos para una base imponible de {base_imponible} es: {total_impuestos}")
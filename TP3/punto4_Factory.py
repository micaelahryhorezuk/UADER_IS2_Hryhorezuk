#Implemente una clase “factura” que tenga un importe correspondiente al total
#de la factura pero de acuerdo a la condición impositiva del cliente (IVA
#Responsable, IVA No Inscripto, IVA Exento) genere facturas que indiquen tal
#condición

from abc import ABC, abstractmethod
class Factura(ABC): # clase abstracta para representar una factura con un método de generación
    def __init__(self, importe):
        self.importe = importe

    @abstractmethod
    def generar_factura(self):
        pass                            
class FacturaIVAResponsable(Factura): # clase concreta que representa una factura para un cliente IVA Responsable
    def generar_factura(self):
        iva = self.importe * 0.21
        total = self.importe + iva
        print(f"Factura IVA Responsable: Importe: {self.importe}, IVA: {iva}, Total: {total}")
class FacturaIVANoInscripto(Factura): # clase concreta que representa una factura para un cliente IVA No Inscripto
    def generar_factura(self):
        print(f"Factura IVA No Inscripto: Importe: {self.importe}, Total: {self.importe}")
class FacturaIVAExento(Factura): # clase concreta que representa una factura para un cliente IVA Exento
    def generar_factura(self):
        print(f"Factura IVA Exento: Importe: {self.importe}, Total: {self.importe}")
class FacturaFactory:   # clase factory para crear instancias de facturas según la condición impositiva del cliente
    @staticmethod
    def crear_factura(importe, condicion_impositiva):
        if condicion_impositiva == "IVA Responsable":
            return FacturaIVAResponsable(importe)
        elif condicion_impositiva == "IVA No Inscripto":
            return FacturaIVANoInscripto(importe)
        elif condicion_impositiva == "IVA Exento":
            return FacturaIVAExento(importe)
        else:
            raise ValueError("Condición impositiva no válida")
# Ejemplo de uso
if __name__ == "__main__":  
    importe = 1000
    condicion_impositiva = "IVA Responsable"
    factura = FacturaFactory.crear_factura(importe, condicion_impositiva)
    factura.generar_factura()   
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Flyweight - TP4 Ejercicio 5
#*------------------------------------------------------------------------
#Imagine una situación donde pueda ser de utilidad el patrón “flyweight”.

class EstiloFuente:
    """
    Flyweight.
    __new__ garantiza que solo existe una instancia por combinacion de atributos.
    """

    _estilos = {}

    def __new__(cls, fuente, tamanio, color, negrita=False, cursiva=False):
        clave = (fuente, tamanio, color, negrita, cursiva)
        try:
            instancia = cls._estilos[clave]
        except KeyError:
            instancia = object.__new__(cls)
            cls._estilos[clave] = instancia
            print(f"  [Flyweight] Nuevo estilo creado: {fuente} {tamanio}pt {color} "
                  f"{'bold' if negrita else ''} {'italic' if cursiva else ''}")
        return instancia

    def set_estilo(self, fuente, tamanio, color, negrita=False, cursiva=False):
        self.fuente  = fuente
        self.tamanio = tamanio
        self.color   = color
        self.negrita = negrita
        self.cursiva = cursiva

    def renderizar(self, caracter, fila, col):
        bold = "bold" if self.negrita else "normal"
        ital = "italic" if self.cursiva else "upright"
        print(f"  '{caracter}' en ({fila},{col:3d}) | "
              f"{self.fuente} {self.tamanio}pt {self.color} {bold} {ital}")


class CaracterEnDocumento:
    def __init__(self, caracter, fila, col, estilo):
        self.caracter = caracter
        self.fila     = fila
        self.col      = col
        self.estilo   = estilo

    def renderizar(self):
        self.estilo.renderizar(self.caracter, self.fila, self.col)


if __name__ == "__main__":
    import os
    os.system('clear')

    print("Creando estilos:")

    est_normal = EstiloFuente("Arial", 12, "negro")
    est_normal.set_estilo("Arial", 12, "negro")

    est_titulo = EstiloFuente("Arial", 18, "negro", negrita=True)
    est_titulo.set_estilo("Arial", 18, "negro", negrita=True)

    est_acento = EstiloFuente("Arial", 12, "azul", cursiva=True)
    est_acento.set_estilo("Arial", 12, "azul", cursiva=True)

    est_normal2 = EstiloFuente("Arial", 12, "negro")
    est_normal2.set_estilo("Arial", 12, "negro")
    print(f"\n  Iguales ID implica el mismo objeto: est_normal is est_normal2 -> {est_normal is est_normal2}")

    documento = []
    textos = [
        ("Titulo del documento", 0, est_titulo),
        ("Texto normal de relleno", 1, est_normal),
        ("enfasis en cursiva", 2, est_acento),
    ]

    for texto, fila, estilo in textos:
        for col, c in enumerate(texto):
            documento.append(CaracterEnDocumento(c, fila, col, estilo))

    for linea in range(100):
        for col, c in enumerate("relleno para simular un documento largo"):
            documento.append(CaracterEnDocumento(c, 3 + linea, col, est_normal))

    print(f"\nDocumento construido con {len(documento)} caracteres.")
    print(f"Estilos unicos en memoria: {len(EstiloFuente._estilos)}  (solo 3)")

    print("\nRenderizando primeras lineas del documento:")
    print("-" * 55)
    n = len("Titulo del documento") + len("Texto normal de relleno") + len("enfasis en cursiva")
    for car in documento[:n]:
        car.renderizar()

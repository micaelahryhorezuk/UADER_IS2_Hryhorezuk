#Imagine una situación donde pueda ser de utilidad el patrón “flyweight”.
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Flyweight
#* TP4 - Ejercicio 5
#*------------------------------------------------------------------------
"""
Situación: Editor de texto con miles de caracteres en pantalla.

PROBLEMA SIN FLYWEIGHT:
  Cada carácter almacena su propio estilo (fuente, tamaño, color, negrita).
  Con decenas de miles de caracteres, el gasto de memoria es enorme.

SOLUCIÓN CON FLYWEIGHT:
  El estado INTRÍNSECO (fuente, tamaño, color, negrita) se comparte entre
  todos los caracteres que tengan el mismo estilo → un solo objeto por estilo.
  El estado EXTRÍNSECO (carácter concreto y posición) se maneja fuera.

  Se usa __new__ con un diccionario de clase para garantizar que cada
  combinación de estilo exista UNA SOLA VEZ en memoria.
"""


class EstiloFuente:
    """
    Flyweight.
    Contiene el estado intrínseco compartido.
    __new__ garantiza que solo existe una instancia por combinación de atributos.
    """

    _estilos = {}   # diccionario de clase compartido por todas las instancias

    def __new__(cls, fuente, tamaño, color, negrita=False, cursiva=False):
        clave = (fuente, tamaño, color, negrita, cursiva)
        try:
            instancia = cls._estilos[clave]
        except KeyError:
            instancia = object.__new__(cls)
            cls._estilos[clave] = instancia
            print(f"  [Flyweight] Nuevo estilo creado: {fuente} {tamaño}pt {color} "
                  f"{'bold' if negrita else ''} {'italic' if cursiva else ''}")
        return instancia

    def set_estilo(self, fuente, tamaño, color, negrita=False, cursiva=False):
        self.fuente  = fuente
        self.tamaño  = tamaño
        self.color   = color
        self.negrita = negrita
        self.cursiva = cursiva

    def renderizar(self, caracter, fila, col):
        bold = "bold" if self.negrita else "normal"
        ital = "italic" if self.cursiva else "upright"
        print(f"  '{caracter}' en ({fila},{col:3d}) | "
              f"{self.fuente} {self.tamaño}pt {self.color} {bold} {ital}")


class CaracterEnDocumento:
    """
    Contexto (estado extrínseco).
    Cada carácter del documento guarda solo su posición y una
    referencia al flyweight de estilo compartido.
    """

    def __init__(self, caracter, fila, col, estilo):
        self.caracter = caracter
        self.fila     = fila
        self.col      = col
        self.estilo   = estilo   # referencia compartida, NO copia

    def renderizar(self):
        self.estilo.renderizar(self.caracter, self.fila, self.col)


"""main method"""

if __name__ == "__main__":

    import os
    os.system('clear')

    # Crear estilos (cada combinación se instancia UNA sola vez)
    print("Creando estilos:")

    est_normal = EstiloFuente("Arial", 12, "negro")
    est_normal.set_estilo("Arial", 12, "negro")

    est_titulo = EstiloFuente("Arial", 18, "negro", negrita=True)
    est_titulo.set_estilo("Arial", 18, "negro", negrita=True)

    est_acento = EstiloFuente("Arial", 12, "azul", cursiva=True)
    est_acento.set_estilo("Arial", 12, "azul", cursiva=True)

    # Verificar que mismos parámetros devuelven el mismo objeto
    est_normal2 = EstiloFuente("Arial", 12, "negro")
    est_normal2.set_estilo("Arial", 12, "negro")
    print(f"\n  Iguales ID implica el mismo objeto: est_normal is est_normal2 → {est_normal is est_normal2}")
    print(f"  id(est_normal)={id(est_normal)}  id(est_normal2)={id(est_normal2)}")

    # Construir documento con miles de caracteres
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
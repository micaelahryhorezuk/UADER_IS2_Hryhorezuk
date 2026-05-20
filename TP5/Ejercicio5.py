import os

#*--------------------------------------------------------------------
#* Design pattern MEMENTO — con historial de hasta 4 estados
#* Modificación de IS2_taller_memory.py
#*--------------------------------------------------------------------

# --- MEMENTO ---
# Objeto que "fotografía" el estado del FileWriterUtility en un momento dado.
# No tiene lógica propia: solo guarda los datos (file, content) para poder
# restaurarlos después. Es inmutable por convención (nadie debería modificarlo).
class Memento:
    def __init__(self, file, content):
        self.file = file
        self.content = content


# --- ORIGINATOR: FileWriterUtility ---
# El objeto cuyo estado queremos preservar y restaurar.
# save()  → crea y devuelve un Memento con su estado actual.
# undo()  → recibe un Memento y restaura su estado desde él.
# El Originator no sabe nada del historial; eso es responsabilidad del Caretaker.
class FileWriterUtility:
    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        # Crea un Memento con el estado actual (una "foto" del objeto)
        return Memento(self.file, self.content)

    def undo(self, memento):
        # Restaura el estado desde un Memento recibido
        self.file = memento.file
        self.content = memento.content


# --- CARETAKER: FileWriterCaretaker ---
# Gestiona el historial de Mementos.
# CAMBIO RESPECTO AL ORIGINAL: en lugar de guardar un solo estado en self.obj,
# ahora mantiene una lista (self.history) de hasta MAX_HISTORY estados.
#
# Lógica del historial:
#   - self.history es una lista donde el ÚLTIMO elemento es el estado más reciente.
#   - save() agrega al final; si supera MAX_HISTORY, descarta el más antiguo.
#   - undo(writer, steps) recupera el estado en la posición:
#       steps=0 → el más reciente (history[-1])
#       steps=1 → el anterior a ese (history[-2])
#       steps=2 → history[-3]
#       steps=3 → history[-4]  (el más antiguo guardado)
class FileWriterCaretaker:
    MAX_HISTORY = 4  # Capacidad máxima del historial

    def __init__(self):
        self.history = []  # Lista de Mementos; el último es el más reciente

    def save(self, writer):
        # Guarda el estado actual del writer al final de la lista
        self.history.append(writer.save())
        # Si supera el límite, elimina el estado más antiguo (el primero)
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)

    def undo(self, writer, steps=0):
        # steps indica cuántos estados atrás recuperar:
        #   0 = inmediato anterior, 1 = el anterior a ese, etc.
        if not self.history:
            print("No hay estados guardados en el historial.")
            return

        # Convierte steps en índice negativo: steps=0 → [-1], steps=1 → [-2], etc.
        index = -(steps + 1)

        if abs(index) > len(self.history):
            print(f"No existe un estado {steps} pasos atrás (solo hay {len(self.history)} guardados).")
            return

        writer.undo(self.history[index])
        print(f"  [undo] Recuperado estado {steps} paso(s) atrás.")


#*---------------------
if __name__ == '__main__':
    os.system("clear")

    print("Crea el Caretaker (gestor del historial) y el objeto a preservar")
    caretaker = FileWriterCaretaker()
    writer = FileWriterUtility("GFG.txt")

    print("\n--- Escritura y guardado de 4 estados ---\n")

    writer.write("Estado 1: Clase de IS2 en UADER\n")
    caretaker.save(writer)
    print(f"Guardado estado 1:\n{writer.content}")

    writer.write("Estado 2: Material adicional\n")
    caretaker.save(writer)
    print(f"Guardado estado 2:\n{writer.content}")

    writer.write("Estado 3: Patrones de diseño\n")
    caretaker.save(writer)
    print(f"Guardado estado 3:\n{writer.content}")

    writer.write("Estado 4: Memento pattern\n")
    caretaker.save(writer)
    print(f"Guardado estado 4:\n{writer.content}")

    print("--- Escritura sin guardar (estado actual no guardado) ---\n")
    writer.write("Estado 5: Sin guardar\n")
    print(f"Estado actual (no guardado):\n{writer.content}")

    print("\n--- Recuperando estados con undo ---\n")

    print("undo(0) → recupera el inmediato anterior (estado 4):")
    caretaker.undo(writer, 0)
    print(writer.content)

    print("undo(1) → recupera 1 paso más atrás (estado 3):")
    caretaker.undo(writer, 1)
    print(writer.content)

    print("undo(2) → recupera 2 pasos más atrás (estado 2):")
    caretaker.undo(writer, 2)
    print(writer.content)

    print("undo(3) → recupera 3 pasos más atrás (estado 1):")
    caretaker.undo(writer, 3)
    print(writer.content)

    print("undo(4) → intento fuera de rango (solo hay 4 guardados):")
    caretaker.undo(writer, 4)

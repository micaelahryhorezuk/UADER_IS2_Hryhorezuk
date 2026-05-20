import os

#*--------------------------------------------------------------------
#* Patrón de diseño STATE - Radio con memorias AM/FM
#* Modificación de IS2_taller_scanner.py
#*--------------------------------------------------------------------

# --- CLASE BASE DE ESTADO ---
# Define el comportamiento común a todos los estados de sintonía.
# scan() avanza la posición en la lista de estaciones de forma circular.
# Los estados concretos (AmState, FmState, MemoryState) heredan este método.
class State:
    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0  # Vuelve al inicio cuando llega al final (ciclo circular)
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))


# --- ESTADO AM ---
# Representa el modo de sintonía AM de la radio.
# Contiene la lista de frecuencias AM a barrer y sabe cómo cambiar a FM.
class AmState(State):
    def __init__(self, radio):
        self.radio = radio                        # Referencia al contexto (Radio), necesaria para cambiar de estado
        self.stations = ["1250", "1380", "1510"]  # Frecuencias AM disponibles para barrer
        self.pos = 0                              # Índice de la estación actual
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate     # Le dice al contexto que cambie su estado activo a FM


# --- ESTADO FM ---
# Representa el modo de sintonía FM de la radio.
# Contiene la lista de frecuencias FM a barrer y sabe cómo cambiar a AM.
class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]  # Frecuencias FM disponibles para barrer
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate     # Le dice al contexto que cambie su estado activo a AM


# --- ESTADO MEMORIAS ---
# Nuevo estado que representa las 4 frecuencias memorizadas (M1-M4).
# Cada memoria puede ser AM o FM con su propia frecuencia específica.
# A diferencia de AM/FM, este estado no usa toggle_amfm porque no es un
# modo que alterne; se invoca directamente con scan_memories().
class MemoryState:
    def __init__(self):
        # Lista de memorias: cada entrada es (nombre, banda, frecuencia)
        # M1 y M3 son AM, M2 y M4 son FM — pueden ser cualquier combinación
        self.memories = [
            ("M1", "AM", "1190"),
            ("M2", "FM", "97.1"),
            ("M3", "AM", "1420"),
            ("M4", "FM", "105.5"),
        ]
        self.pos = 0  # Índice de la memoria actual

    def scan(self):
        # Sintoniza la memoria actual y avanza al siguiente índice (circular)
        memory_name, band, freq = self.memories[self.pos]
        print("Sintonizando memoria... {} - {} {}".format(memory_name, freq, band))
        self.pos += 1
        if self.pos == len(self.memories):
            self.pos = 0


# --- CONTEXTO: RADIO ---
# Es el objeto principal. No contiene lógica de sintonía propia:
# delega scan() y toggle_amfm() al estado activo (self.state).
# Esto es la clave del patrón State: el comportamiento de Radio cambia
# dinámicamente según cuál sea su estado activo en cada momento.
class Radio:
    def __init__(self):
        # Crea los tres estados pasándose a sí mismo como argumento,
        # para que AmState y FmState puedan cambiar self.state cuando se llame toggle_amfm
        self.fmstate = FmState(self)
        self.amstate = AmState(self)
        self.memstate = MemoryState()  # Estado de memorias (no necesita referencia al contexto)

        self.state = self.fmstate      # Estado inicial: empieza en FM

    def toggle_amfm(self):
        # Delega el cambio de banda al estado actual
        # AmState cambia a FM y FmState cambia a AM
        self.state.toggle_amfm()

    def scan(self):
        # Delega el barrido de estaciones al estado activo (AM o FM según corresponda)
        self.state.scan()

    def scan_memories(self):
        # Recorre las 4 memorias en secuencia dentro de cada ciclo de barrido
        print("-- Escaneando memorias --")
        for _ in range(len(self.memstate.memories)):
            self.memstate.scan()


#*---------------------
if __name__ == "__main__":
    os.system("clear")
    print("\nCrea un objeto radio y almacena las siguientes acciones")
    radio = Radio()

    # Secuencia de acciones por ciclo:
    # 3 scan (FM) → toggle a AM → 3 scan (AM) → barrido de 4 memorias
    # Se repite 2 veces con actions *= 2
    actions = [radio.scan] * 3 + [radio.toggle_amfm] + [radio.scan] * 3 + [radio.scan_memories]
    actions *= 2

    print("Recorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado\n")
    for action in actions:
        action()

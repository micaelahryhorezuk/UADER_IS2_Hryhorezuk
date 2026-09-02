
""" Q4: Esfuerzo y calendario a partir del tamano del proyecto
E = 8 * S^0.95
td = 2.4 * E^0.33
"""
import matplotlib
matplotlib.use("Agg")  # backend sin ventana grafica, evita que se cuelgue en terminal
import numpy as np
import matplotlib.pyplot as plt

def esfuerzo(S):
    return 8 * S**0.95

def calendario(E):
    return 2.4 * E**0.33

# Prueba rapida con algunos valores
for S in [100, 1000, 5000, 10000]:
    E = esfuerzo(S)
    td = calendario(E)
    print(f"S={S:6d} -> E={E:9.2f} -> td={td:6.2f}")

# Grafico 1: Esfuerzo vs Tamano, S en [0, 10000]
S = np.linspace(0, 10000, 500)
E = esfuerzo(S)

plt.figure(figsize=(8, 5))
plt.plot(S, E)
plt.xlabel("Tamano del proyecto (S)")
plt.ylabel("Esfuerzo (E)")
plt.title("Esfuerzo vs Tamano (E = 8*S^0.95)")
plt.grid(True)
plt.savefig("Q4_esfuerzo_vs_tamano.png", dpi=120)
plt.close()

# Grafico 2: Calendario vs Esfuerzo, E en [1, 500]
E2 = np.linspace(1, 500, 500)
td = calendario(E2)

plt.figure(figsize=(8, 5))
plt.plot(E2, td, color="orange")
plt.xlabel("Esfuerzo (E)")
plt.ylabel("Calendario (td)")
plt.title("Calendario vs Esfuerzo (td = 2.4*E^0.33)")
plt.grid(True)
plt.savefig("Q4_calendario_vs_esfuerzo.png", dpi=120)
plt.close()

print("\nGraficos guardados: Q4_esfuerzo_vs_tamano.png y Q4_calendario_vs_esfuerzo.png")
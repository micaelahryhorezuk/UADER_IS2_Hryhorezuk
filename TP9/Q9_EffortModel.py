"""
TP9 - Q9: Regresion lineal vs exponencial (LOC -> Esfuerzo)
"""
import matplotlib
matplotlib.use("Agg")  # backend sin ventana grafica, evita que se cuelgue en terminal
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

LOC = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
E   = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

# --- Regresion lineal ---
slope, intercept, r_lin, p, se = stats.linregress(LOC, E)
r2_lin = r_lin**2

# --- Regresion exponencial: E = a * exp(b*LOC) ---
lnE = np.log(E)
slope2, intercept2, r_exp, p2, se2 = stats.linregress(LOC, lnE)
a_exp, b_exp = np.exp(intercept2), slope2
E_pred_exp = a_exp * np.exp(b_exp * LOC)
ss_res = np.sum((E - E_pred_exp) ** 2)
ss_tot = np.sum((E - np.mean(E)) ** 2)
r2_exp = 1 - ss_res / ss_tot

def E_lin(loc):
    return slope * loc + intercept

def E_expo(loc):
    return a_exp * np.exp(b_exp * loc)

print(f"Lineal:      E = {slope:.6f}*LOC + {intercept:.4f}   R2={r2_lin:.4f}")
print(f"Exponencial: E = {a_exp:.4f} * exp({b_exp:.6f}*LOC)   R2={r2_exp:.4f}")

for loc in [9100, 200]:
    print(f"LOC={loc}: lineal={E_lin(loc):.2f} PM | exponencial={E_expo(loc):.2f} PM")

# --- Grafico ---
loc_range = np.linspace(0, 10000, 200)
plt.figure(figsize=(8, 5))
plt.scatter(LOC, E, color="black", label="Datos historicos")
plt.plot(loc_range, E_lin(loc_range), label=f"Lineal (R2={r2_lin:.3f})")
plt.plot(loc_range, E_expo(loc_range), label=f"Exponencial (R2={r2_exp:.3f})")
plt.scatter([9100, 200], [E_lin(9100), E_lin(200)], color="red", marker="x", s=100, label="Predicciones (lineal)")
plt.xlabel("LOC")
plt.ylabel("Esfuerzo (PM)")
plt.title("Modelo de esfuerzo: Lineal vs Exponencial")
plt.legend()
plt.grid(True)
plt.savefig("Q9_regresion.png", dpi=120)
plt.close()

print("\nGrafico guardado: Q9_regresion.png")
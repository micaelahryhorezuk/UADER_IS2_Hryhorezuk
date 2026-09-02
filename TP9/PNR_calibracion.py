"""
Taller Modelos Dinamicos - Calibracion del modelo PNR (Putnam-Norden-Rayleigh)
E(t) = 2*K*a*t*exp(-a*t^2)

Datos historicos: t [Meses] vs E(t) [PM]
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, brentq

# --- Datos historicos del taller ---
t_hist = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
E_hist = np.array([8, 21, 25, 30, 25, 24, 17, 15, 11])

def pnr(t, K, a):
    return 2 * K * a * t * np.exp(-a * t**2)

# --- Calibracion (probando varios puntos de partida para evitar minimos locales) ---
best = None
for a0 in [0.01, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]:
    for K0 in [50, 100, 150, 200, 300]:
        try:
            popt, _ = curve_fit(pnr, t_hist, E_hist, p0=[K0, a0], maxfev=10000)
            K_, a_ = popt
            ss_res = np.sum((E_hist - pnr(t_hist, K_, a_)) ** 2)
            if best is None or ss_res < best[0]:
                best = (ss_res, K_, a_)
        except Exception:
            pass

_, K_cal, a_cal = best
E_pred = pnr(t_hist, K_cal, a_cal)
ss_res = np.sum((E_hist - E_pred) ** 2)
ss_tot = np.sum((E_hist - np.mean(E_hist)) ** 2)
r2 = 1 - ss_res / ss_tot

print(f"K calibrado = {K_cal:.2f} PM")
print(f"a calibrado = {a_cal:.6f}")
print(f"R2 = {r2:.4f}")

t_pico = 1 / np.sqrt(a_cal)
E_pico = pnr(t_pico, K_cal, a_cal)
print(f"Pico natural: t_pico={t_pico:.2f}, E_pico={E_pico:.2f} PM")

def tf_98(K, a, tmax=None):
    if tmax is None:
        tmax = max(40, 8 / np.sqrt(a))
    t_range = np.linspace(0, tmax, 600000)
    E_model = pnr(t_range, K, a)
    dt = t_range[1] - t_range[0]
    E_acum = np.cumsum(E_model) * dt
    idx = np.argmax(E_acum >= 0.98 * K)
    return t_range[idx]

tf_base = tf_98(K_cal, a_cal)
print(f"tf calibrado (98% de K entregado) = {tf_base:.2f} meses")

# --- Grafico de calibracion ---
t_range = np.linspace(0, 20, 500)
plt.figure(figsize=(8, 5))
plt.scatter(t_hist, E_hist, color="black", label="Datos historicos")
plt.plot(t_range, pnr(t_range, K_cal, a_cal), color="red",
         label=f"Modelo PNR calibrado (a={a_cal:.4f}, R2={r2:.3f})")
plt.xlabel("Tiempo (meses)")
plt.ylabel("Esfuerzo E(t) [PM]")
plt.title("Calibracion modelo PNR")
plt.legend()
plt.grid(True)
plt.savefig("PNR_calibracion.png", dpi=120)
plt.close()

# --- Restriccion de staff maximo ---
print("\n=== Restriccion de staff maximo (K fijo) ===")
staff_results = {}
for staff_max in [5, 12, 20]:
    def f(a_):
        return pnr(1 / np.sqrt(a_), K_cal, a_) - staff_max
    a_r = brentq(f, 1e-6, a_cal)
    tpico_r = 1 / np.sqrt(a_r)
    tf_r = tf_98(K_cal, a_r)
    staff_results[staff_max] = (a_r, tpico_r, tf_r)
    print(f"Staff max={staff_max:3d} -> a={a_r:.6f}, t_pico={tpico_r:.2f}, "
          f"tf={tf_r:.2f} meses (base={tf_base:.2f}, x{tf_r/tf_base:.2f})")

# --- Reduccion de calendario ---
print("\n=== Reduccion de calendario tf (K fijo) ===")
for frac in [0.9, 0.8, 0.7]:
    tf_target = tf_base * frac
    def g(a_):
        return tf_98(K_cal, a_) - tf_target
    a_r = brentq(g, a_cal, 5.0)
    tpico_r = 1 / np.sqrt(a_r)
    Epico_r = pnr(tpico_r, K_cal, a_r)
    incremento = 100 * (Epico_r / E_pico - 1)
    print(f"tf objetivo={tf_target:.2f} ({int(frac*100)}%) -> a={a_r:.6f}, "
          f"E_pico={Epico_r:.2f} PM (vs base={E_pico:.2f}, +{incremento:.1f}%)")

# --- Grafico comparativo de restricciones de staff ---
plt.figure(figsize=(8, 5))
plt.plot(t_range, pnr(t_range, K_cal, a_cal), label="Base (sin restriccion)")
for staff_max, (a_r, _, _) in staff_results.items():
    plt.plot(t_range, pnr(t_range, K_cal, a_r), label=f"Staff max={staff_max}")
plt.xlabel("Tiempo (meses)")
plt.ylabel("Esfuerzo E(t) [PM]")
plt.title("Efecto de restringir el staff maximo")
plt.legend()
plt.grid(True)
plt.savefig("PNR_restricciones_staff.png", dpi=120)
plt.close()

print("\nGraficos guardados: PNR_calibracion.png y PNR_restricciones_staff.png")
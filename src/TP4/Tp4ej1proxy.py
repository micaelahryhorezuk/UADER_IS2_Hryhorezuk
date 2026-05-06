#Provea una clase ping que luego de creada al ser invocada con un método
#“execute(string)” realice 10 intentos de ping a la dirección IP contenida en
#“string” (argumento pasado), la clase solo debe funcionar si la dirección IP
#provista comienza con “192.”. Provea un método executefree(string) que haga
#lo mismo pero sin el control de dirección. Ahora provea una clase pingproxy
#cuyo método execute(string) si la dirección es “192.168.0.254” realice un ping a
#www.google.com usando el método executefree de ping y re-envie a execute de la clae ping en cualquier otro caso.
#  (Modele la solución como un patrón proxy).


#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Proxy - TP4 Ejercicio 1
#*------------------------------------------------------------------------

import subprocess
import platform


class ping:
    def execute(self, ip: str):
        if not ip.startswith("192."):
            print(f"[ping] Error: la dirección '{ip}' no está permitida. Debe comenzar con '192.'")
            return
        self._do_ping(ip, 10)

    def executefree(self, ip: str):
        self._do_ping(ip, 10)

    def _do_ping(self, host: str, count: int):
        print(f"\n[ping] Iniciando {count} intentos de ping a '{host}'...")
        param = "-n" if platform.system().lower() == "windows" else "-c"
        for i in range(1, count + 1):
            result = subprocess.run(["ping", param, "1", host], capture_output=True, text=True)
            status = "OK" if result.returncode == 0 else "FALLO"
            print(f"  Intento {i:2d}: {status}")
        print(f"[ping] Fin del ping a '{host}'.\n")


class pingproxy:
    def __init__(self):
        self._ping = ping()

    def execute(self, ip: str):
        if ip == "192.168.0.254":
            print(f"[pingproxy] IP especial detectada ({ip}). Redirigiendo a www.google.com...")
            self._ping.executefree("www.google.com")
        else:
            print(f"[pingproxy] IP normal ({ip}). Delegando a ping.execute...")
            self._ping.execute(ip)


if __name__ == "__main__":
    proxy = pingproxy()

    print("=" * 50)
    print("Caso 1: IP especial → redirige a Google")
    proxy.execute("192.168.0.254")

    print("=" * 50)
    print("Caso 2: IP normal 192.x → llega a ping.execute")
    proxy.execute("192.168.1.1")

    print("=" * 50)
    print("Caso 3: IP fuera del rango (bloqueada por ping)")
    proxy.execute("10.0.0.1")

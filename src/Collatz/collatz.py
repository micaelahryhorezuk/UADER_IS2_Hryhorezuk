import matplotlib.pyplot as plt

def collatz_iteraciones(n):
    contador = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        contador += 1
    return contador


def main():
    numeros = []
    iteraciones = []

    for n in range(1, 10001):
        it = collatz_iteraciones(n)
        numeros.append(n)
        iteraciones.append(it)

    # Gráfico
    plt.figure()
    plt.scatter(iteraciones, numeros, s=1)

    plt.title("Conjetura de Collatz")
    plt.xlabel("Iteraciones")
    plt.ylabel("Número inicial (n)")

    plt.show()


if __name__ == "__main__":
    main()
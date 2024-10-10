import random
import time
import os

class JuegoMemoria:
    def __init__(self, tamaño=4):
        self.tamaño = tamaño
        self.tablero = self.crear_tablero(tamaño)
        self.descubiertas = [[False] * tamaño for _ in range(tamaño)]
        self.ruta_archivo = os.path.join(os.path.expanduser("~"), "Desktop", "juego_guardado.txt")

    def crear_tablero(self, tamaño):
        num_cartas = tamaño * tamaño // 2
        cartas = list(range(1, num_cartas + 1)) * 2
        random.shuffle(cartas)
        
        tablero = []
        for i in range(tamaño):
            fila = cartas[i * tamaño:(i + 1) * tamaño]
            tablero.append(fila)
        return tablero

    def limpiar_pantalla(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def mostrar_tablero(self):
        self.limpiar_pantalla()
        print("Tablero:")
        separador_fila = "----" * self.tamaño  # Línea horizontal

        for i in range(self.tamaño):
            fila = []
            for j in range(self.tamaño):
                if self.descubiertas[i][j]:
                    fila.append(f" {self.tablero[i][j]:2} ")
                else:
                    fila.append(" X  ")
            print(" | ".join(fila))
            if i < self.tamaño - 1:
                print(separador_fila)

    def seleccionar_carta(self):
        while True:
            try:
                fila = int(input(f"Selecciona la fila (0-{self.tamaño - 1}): "))
                columna = int(input(f"Selecciona la columna (0-{self.tamaño - 1}): "))
                if 0 <= fila < self.tamaño and 0 <= columna < self.tamaño:
                    return fila, columna
                else:
                    print(f"Error: las coordenadas deben estar entre 0 y {self.tamaño - 1}.")
            except ValueError:
                print("Error: por favor, ingresa números enteros.")

    def mostrar_mini_menu(self):
        while True:
            print("\nMenú:")
            print("1. Ingresar Fila/Columna")
            print("2. Guardar y Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                return True
            elif opcion == '2':
                self.guardar_juego()
                return False
            else:
                print("Opción inválida. Por favor, intenta de nuevo.")

    def jugar_turno(self):
        self.mostrar_tablero()
        
        if not self.mostrar_mini_menu():
            return  # Salir del juego si elige guardar y salir

        print("\nSelecciona dos cartas:")
        f1, c1 = self.seleccionar_carta()
        f2, c2 = self.seleccionar_carta()

        if self.descubiertas[f1][c1] or self.descubiertas[f2][c2]:
            print("Coordenadas no válidas o cartas ya descubiertas.")
            time.sleep(2)
            return

        self.descubiertas[f1][c1] = True
        self.descubiertas[f2][c2] = True
        self.mostrar_tablero()

        if self.tablero[f1][c1] == self.tablero[f2][c2]:
            print("¡Par encontrado!")
        else:
            print("No son iguales, intenta de nuevo.")
            time.sleep(2)
            self.descubiertas[f1][c1] = False
            self.descubiertas[f2][c2] = False
            self.limpiar_pantalla()

    def todas_descubiertas(self):
        return all(all(fila) for fila in self.descubiertas)

    def jugar(self):
        while not self.todas_descubiertas():
            self.jugar_turno()
        print("¡Felicidades! Has descubierto todas las parejas.")

    def reiniciar_juego(self):
        self.descubiertas = [[False] * self.tamaño for _ in range(self.tamaño)]
        self.tablero = self.crear_tablero(self.tamaño)

    def guardar_juego(self):
        with open(self.ruta_archivo, "w") as archivo:
            archivo.write(f"{self.tamaño}\n")
            for fila in self.tablero:
                archivo.write(" ".join(map(str, fila)) + "\n")
            for fila in self.descubiertas:
                archivo.write(" ".join(map(str, map(int, fila))) + "\n")
        print("Juego guardado con éxito en el escritorio.")

    def cargar_juego(self):
        if os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "r") as archivo:
                self.tamaño = int(archivo.readline().strip())
                self.tablero = [list(map(int, archivo.readline().strip().split())) for _ in range(self.tamaño)]
                self.descubiertas = [list(map(bool, map(int, archivo.readline().strip().split()))) for _ in range(self.tamaño)]
            print("Juego cargado con éxito.")
        else:
            print("No hay un juego guardado en el escritorio.")

    def mostrar_menu(self):
        while True:
            self.limpiar_pantalla()
            print("Bienvenido al Juego de Memoria")
            print("1. Iniciar Nuevo Juego")
            print("2. Continuar Juego")
            print("3. Cambiar Dificultad")
            print("4. Guardar Juego")
            print("5. Cargar Juego")
            print("6. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                self.iniciar_nuevo_juego()
            elif opcion == '2':
                self.jugar()
            elif opcion == '3':
                self.cambiar_dificultad()
            elif opcion == '4':
                self.guardar_juego()
            elif opcion == '5':
                self.cargar_juego()
            elif opcion == '6':
                break
            else:
                print("Opción inválida. Por favor, intenta de nuevo.")

    def iniciar_nuevo_juego(self):
        self.reiniciar_juego()
        self.jugar()

    def cambiar_dificultad(self):
        while True:
            self.limpiar_pantalla()
            print("Selecciona la dificultad:")
            print("1. Fácil (4x4)")
            print("2. Medio (6x6)")
            print("3. Difícil (8x8)")
            dificultad = input("Selecciona una opción: ")

            if dificultad == '1':
                self.tamaño = 4
                break
            elif dificultad == '2':
                self.tamaño = 6
                break
            elif dificultad == '3':
                self.tamaño = 8
                break
            else:
                print("Opción inválida. Por favor, intenta de nuevo.")

        self.reiniciar_juego()

if __name__ == "__main__":
    juego = JuegoMemoria(tamaño=4)
    juego.mostrar_menu()

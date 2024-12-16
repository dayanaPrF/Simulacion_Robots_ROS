import os
import networkx as nx
import math as mt
import matplotlib.pyplot as plt

class SpawnOrigin:
    def __init__(self, archivo_original, coordenada, maze, orientacion):
        self.archivo_original = archivo_original
        self.coordenadaOrigen = self.guardarValores(maze, coordenada, orientacion)

    def guardarValores(self,maze, coordenada, orientacion):
        num_rows = len(maze)
        num_cols = len(maze[0])
        if (orientacion == 'Norte'):
            return (coordenada[0] - num_rows / 2) * 0.4, (coordenada[1] - num_cols / 2) * 0.4, 0
        elif (orientacion == 'Sur'):
            return (coordenada[0] - num_rows / 2) * 0.4, (coordenada[1] - num_cols / 2) * 0.4, 3.1416
        elif (orientacion == 'Este'):
            return (coordenada[0] - num_rows / 2) * 0.4, (coordenada[1] - num_cols / 2) * 0.4, 4.7123
        elif (orientacion == 'Oeste'):
            return (coordenada[0] - num_rows / 2) * 0.4, (coordenada[1] - num_cols / 2) * 0.4, 1.5707
    
    def escribirEnArchivo(self):
        proceso1 = proceso2 = proceso3 = proceso4 = proceso5 = proceso6 = proceso7 = proceso8 = False
        with open(self.archivo_original, 'r') as archivo:
            lineas = archivo.readlines()

        for i, linea in enumerate(lineas):
            if 'spawn = Node(' in linea:
                proceso1 = True
            elif proceso1 and 'package=\'gazebo_ros\',' in linea:
                proceso2 = True
            elif proceso2 and 'executable=\'spawn_entity.py\',' in linea:
                proceso3 = True
            elif proceso3 and 'arguments=["-topic", "/robot_description", ' in linea:
                proceso4 = True
            elif proceso4 and '"-entity", robot_name_in_model,' in linea:
                proceso5 = True
            elif proceso5 and '"-x", ' in linea:
                lineas[i] = f'                    "-x", \'{self.coordenadaOrigen[0]}\',\n'
                proceso6 = True
            elif proceso6 and '"-y", ' in linea:
                lineas[i] = f'                    "-y", \'{self.coordenadaOrigen[1]}\',\n'
                proceso7 = True
            elif proceso7 and '"-z",' in linea:
                lineas[i] = '                    "-z", \'0.05\',\n'
                proceso8 = True
            elif proceso8 and '"-Y",' in linea:
                lineas[i] = f'                    "-Y", \'{self.coordenadaOrigen[2]}\']\n'
                proceso1 = proceso2 = proceso3 = proceso4 = proceso5 = proceso6 = proceso7 = proceso8 = False

        with open(self.archivo_original, 'w') as archivo:
            archivo.writelines(lineas)

def main():
    maze = [
        [False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False],
        [False, True, True, True, True, True, True, True, False, True, False, True, True, True, False, True, True, True, False, True, False],
        [False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, True, False, True, False, True, False],
        [False, True, True, True, False, True, True, True, False, True, True, True, True, True, False, True, False, True, False, True, False],
        [False, True, True, True, False, True, False, True, False, False, False, False, False, True, False, True, False, True, False, True, False],
        [False, False, False, False, False, True, False, True, True, True, True, True, False, True, False, True, False, True, False, True, False],
        [False, True, True, True, True, True, False, True, True, True, True, True, False, True, True, True, False, True, True, True, False],
        [False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, True, False, True, False, False, False],
        [False, True, True, True, False, True, True, True, False, True, True, True, True, True, False, True, False, True, False, True, False],
        [False, True, False, True, False, True, False, False, False, True, True, True, True, True, False, False, False, True, False, True, False],
        [True, True, False, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, False, True, True],
        [False, False, False, True, False, True, False, True, False, True, True, True, True, True, False, False, False, False, False, True, False],
        [False, True, False, True, True, True, False, True, False, True, True, True, True, True, False, True, True, True, False, True, False],
        [False, True, False, False, False, False, False, True, False, False, False, True, False, False, False, True, False,True, False, True, False],
        [False, True, False, True, True, True, True, True, False, True, False, True, True, True, False, True, False, True, False, True, False],
        [False, True, False, True, False, False, False, False, False, True, False, True, False, True, False, False, False, True, False, True, False],
        [False, True, False, True, False, True, True, True, True, True, False, True, False, True, True, True, False, True, False, True, False],
        [False, True, False, True, False, True, False, True, False, True, False, False, False, False, False, True, False, True, False, True, False],
        [False, True, False, True, False, True, False, True, False, True, False, True, True, True, True, True, False, True, False, True, False],
        [False, True, True, True, False, True, False, True, False, True, False, True, False, False, False, False, False, True, True, True, False],
        [False, True, False, False, False, True, False, False, False, True, False, True, True, True, True, True, True, True, False, True, False],
        [False, True, True, True, True, True, True, True, False, True, False, True, True, True, True, True, False, True, False, True, False],
        [False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False]
    ]
    norte = (0, 9)
    sur = (22, 9)
    este = (10, 20)
    oeste = (10, 0)
    coordenada = (0, 0)
    orientacion = None
    while True:
        print("¿Donde iniciara el recorrido?")
        print("1. Norte")
        print("2. Sur")
        print("3. Este")
        print("4. Oeste")
        opc = input("Seleccione una opción: ")
        try:
            opc = int(opc)
        except ValueError:
            print("Por favor, ingrese un número válido.\n")
            continue
        if opc == 1:
            coordenada = norte
            orientacion = 'Norte'
            break
        elif opc == 2:
            coordenada = sur
            orientacion = 'Sur'
            break
        elif opc == 3:
            coordenada = este
            orientacion = 'Este'
            break
        elif opc == 4:
            coordenada = oeste
            orientacion = 'Oeste'
            break
        else:
            print("Opción incorrecta, seleccione una opción válida.\n")
    inicio = SpawnOrigin('/home/user/robotPrueba/src/modelo_robot/launch/gazebo.launch.py', coordenada, maze, orientacion)
    inicio.escribirEnArchivo()
    print("\n")

if __name__ == "__main__":
    main()

class Celda:
    def __init__(self, norte, sur, este, oeste, noroeste, noreste, suroeste, sureste, estado,x,y, inicio, fin):
        self.x = x  #coordenada x, y de posicion de la celda
        self.y = y
        self.norte = norte #apuntadores a celdas colindantes
        self.sur = sur
        self.este = este
        self.oeste = oeste
        self.noroeste = noroeste
        self.noreste = noreste
        self.suroeste = suroeste
        self.sureste = sureste
        self.estado = estado
        self.inicio = inicio
        self.fin = fin

class Area:
    def __init__(self, celdas):
        self.celdas = celdas #Matriz de estados de las celdas
        self.inicio, self.fin = self.encontrar_inicio_y_fin() #Coordenadas de las celdas donde inicia el robot y donde llega el robot
        self.tabla = self.crearTabla() #apuntador a tabla

    def crearTabla(self):
        tabla = [[None] * len(self.celdas[0]) for _ in range(len(self.celdas))] #Instanciamos tabla como cuadricula en nulo

        for i in range(len(self.celdas)): #Se crean los objetos celdas en la tabla
            for j in range(len(self.celdas[i])):
                estado, inicio, fin = self.celdas[i][j]
                tabla[i][j] = Celda(None, None, None, None, None, None, None, None, estado, i, j, inicio, fin)

        for i in range(len(self.celdas)): #Relacionamos colindantes
            for j in range(len(self.celdas[i])):
                celda_actual = tabla[i][j]
                celda_actual.norte = tabla[i-1][j] if i > 0 else None
                celda_actual.sur = tabla[i+1][j] if i < len(self.celdas) - 1 else None
                celda_actual.este = tabla[i][j+1] if j < len(self.celdas[i]) - 1 else None
                celda_actual.oeste = tabla[i][j-1] if j > 0 else None
                celda_actual.noroeste = tabla[i-1][j-1] if i > 0 and j > 0 else None
                celda_actual.noreste = tabla[i-1][j+1] if i > 0 and j < len(self.celdas[i]) - 1 else None
                celda_actual.suroeste = tabla[i+1][j-1] if i < len(self.celdas) - 1 and j > 0 else None
                celda_actual.sureste = tabla[i+1][j+1] if i < len(self.celdas) - 1 and j < len(self.celdas[i]) - 1 else None
        return tabla

    def encontrar_inicio_y_fin(self):
        inicio = None
        fin = None
        for i in range(len(self.celdas)):
            for j in range(len(self.celdas[i])):
                if self.celdas[i][j][1]:  # Verificar si es inicio
                    inicio = (i, j)
                if self.celdas[i][j][2]:  # Verificar si es fin
                    fin = (i, j)
        return inicio, fin

# Función para imprimir solo los valores de los punteros de cada celda
def imprimir_punteros(tabla):
    for fila in tabla:
        for celda in fila:
            if celda:
                print(celda.estado, end='\t')
            else:
                print("None", end='\t')
        print()

# Prueba en el main
if __name__ == "__main__":
    # Lista de celdas de ejemplo con el formato (estado, inicio, fin)
    celdas_ejemplo = [
        [(False, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, True), (True, False, False), (False, False, False), (True, False, False)],
        [(False, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False)],
        [(False, False, False), (True, False, False), (True, False, False), (False, False, False), (False, False, False), (False, False, False), (False, False, False), (False, False, False), (False, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (False, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, True, False), (False, False, False), (False, False, False), (False, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False)]
    ]


    # Crear un objeto de la clase Area
    area = Area(celdas_ejemplo)

    # Imprimir los valores de los punteros de cada celda
    imprimir_punteros(area.tabla)

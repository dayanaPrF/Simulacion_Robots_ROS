#/cmd_vel [geometry_msgs/msg/Twist]
#/wheel/odometry [nav_msgs/msg/Odometry]
"""
linear:
    x: 0.0
    y: 0.0
    z: 0.0
angular:
    x: 0.0
    y: 0.0
    z: -0.3
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class PublicadorMovimiento(Node):

    def __init__(self, celdas):
        super().__init__('publicador_movimiento')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) #(tipo_mensaje, nombre_topic_QoS)
        timer_period = 0.0001  # seconds (periodo de muestreo)
        #self.celdas = celdas
        self.area = Area(celdas)
        self.a = AEstrella(self.area)
        self.a.algoritmo()
        self.camino = self.a.caminoFinal
        self.cell_1 = self.cell_2 = None
        self.i = 0 #Contar los elementos de la lista final
        self.count_tempo = 0 #Contar tiempo
        self.tempo = 0
        self.tempo_avance_lado = 10000 #Constantes para contabilizar
        self.tempo_avance_diagonal = 14142
        self.tempo_avance_0 = 1
        self.tempo_avance_45 = 5236
        self.tempo_avance_90 = 10472
        self.tempo_avance_135 = 15708
        self.tempo_avance_180 = 20942
        self.bDiagonal = self.bRecta = self.giro_direccionar = self.giro_posicionar = False
        self.bN = self.bNE =self.bE = self.bSE = self.bS = self.bSO = self.bO = self.bNO = False #Banderas para acceder a un campos
        self.timer = self.create_timer(timer_period, self.timer_callback)#timer y rutina de interrupcion

    def timer_callback(self): #Armado del mensaje
        msg = Twist() #Define el tipo del mensaje
        msg = self.definir_movimiento(msg)
        self.publisher_.publish(msg) #publica el mensaje
        self.get_logger().info('Publishing: "%s"' % msg) #Imprime mensaje en pantalla
    
    def definir_movimiento(self,msg):
        #En x ira a 0.30 m/s
        #Angular ira a 1.50 rad/s
        if (self.cell_1 is None or self.cell_2 is None):
            self.cell_1, self.cell_2 = self.obtenerCells()
            self.i = self.i + 1
            if (self.cell_1 is not None and self.cell_2 is not None): #Solo para primera iteracion
                self.buscarColindancia()
                self.giro_direccionar = True
            else:
                self.movimiento_cero(msg) #Cuando no se mueve
        elif self.giro_direccionar: #Para direccionar el carrito
            self.tempo = self.definir_giro_direccionar_y_tiempo(msg)
            self.count_tempo = self.count_tempo + 1
            if(self.count_tempo == self.tempo):
                self.count_tempo = self.tempo = 0
                self.giro_direccionar = False
        elif self.giro_posicionar: #Para posicionar el carro
            self.tempo = self.definir_giro_posicionar_y_tiempo(msg)
            self.count_tempo = self.count_tempo + 1
            if(self.count_tempo == self.tempo):
                self.count_tempo = self.tempo = 0
                self.giro_posicionar = False
                self.cell_1, self.cell_2 = self.obtenerCells()
                self.i = self.i + 1
                if (self.cell_1 is not None and self.cell_2 is not None):
                    self.buscarColindancia()
                    self.giro_direccionar = True
        elif self.bDiagonal: #Avanzar en diagonal
            self.colocarMovimiento(msg,0.3,0.0,0.0,0.0,0.0,0.0)
            self.tempo = self.tempo_avance_diagonal
            self.count_tempo = self.count_tempo + 1
            if(self.count_tempo == self.tempo):
                self.giro_posicionar = True
                self.count_tempo = self.tempo = 0
                self.bDiagonal = False
        elif self.bRecta: #Avanzar en linea recta
            self.colocarMovimiento(msg,0.3,0.0,0.0,0.0,0.0,0.0)
            self.tempo = self.tempo_avance_lado
            self.count_tempo = self.count_tempo + 1
            if(self.count_tempo == self.tempo):
                self.giro_posicionar = True
                self.count_tempo = self.tempo = 0
                self.bRecta = False
        return msg

        
    def definir_giro_posicionar_y_tiempo(self,msg):
        constante_val = 0
        if self.bN:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,0.0)
            constante_val = self.tempo_avance_0
        elif self.bNE:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,-1.5)
            constante_val = self.tempo_avance_45
        elif self.bE:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,-1.5)
            constante_val = self.tempo_avance_90
        elif self.bSE:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,-1.5)
            constante_val = self.tempo_avance_135
        elif self.bS:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_180
        elif self.bSO:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_135
        elif self.bO:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_90
        elif self.bNO:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_45
        return constante_val


    def definir_giro_direccionar_y_tiempo(self,msg):
        constante_val = 0
        if self.bN:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,0.0)
            constante_val = self.tempo_avance_0
        elif self.bNE:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_45
        elif self.bE:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_90
        elif self.bSE:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_135
        elif self.bS:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,1.5)
            constante_val = self.tempo_avance_180
        elif self.bSO:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,-1.5)
            constante_val = self.tempo_avance_135
        elif self.bO:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,-1.5)
            constante_val = self.tempo_avance_90
        elif self.bNO:
            self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,-1.5)
            constante_val = self.tempo_avance_45
        return constante_val

        
    def movimiento_cero(self,msg):
        self.colocarMovimiento(msg,0.0,0.0,0.0,0.0,0.0,0.0)
    
    def colocarMovimiento(self,msg,lx,ly,lz,ax,ay,az):
        msg.linear.x = lx
        msg.linear.y = ly
        msg.linear.z = lz
        msg.angular.x = ax
        msg.angular.y = ay
        msg.angular.z = az

    def buscarColindancia(self):
        if self.cell_1.norte == self.cell_2: 
            self.bN = True
            self.bRecta = True
            self.bDiagonal = False
        elif self.cell_1.sur == self.cell_2: 
            self.bS = True
            self.bRecta = True
            self.bDiagonal = False
        elif self.cell_1.este == self.cell_2: 
            self.bE = True
            self.bRecta = True
            self.bDiagonal = False
        elif self.cell_1.oeste == self.cell_2: 
            self.bO = True
            self.bRecta = True
            self.bDiagonal = False
        elif self.cell_1.noroeste == self.cell_2: 
            self.bNO = True
            self.bRecta = False
            self.bDiagonal = True
        elif self.cell_1.noreste == self.cell_2: 
            self.bNE = True
            self.bRecta = False
            self.bDiagonal = True
        elif self.cell_1.suroeste == self.cell_2: 
            self.bSO = True
            self.bRecta = False
            self.bDiagonal = True
        elif self.cell_1.sureste == self.cell_2: 
            self.bSE = True
            self.bRecta = False
            self.bDiagonal = True

    def obtenerCells(self):
        if self.i >= len(self.camino):#Si la celda siguiente no existe 
            return None,None
        elif self.i+1 >= len(self.camino):#Cuando ya pasamos por todos los elementos de la lista
            return self.camino[self.i],None
        else:                           #Cuando hay mas celdas por visitar
            return self.camino[self.i],self.camino[self.i+1]

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


class Nodo: #Clase para agregar caracteristicas de celdas para la ejecucion del algoritmo A*
    def __init__(self, distancia, heuristica, puntaje, padre, celda):
        self.distancia = distancia
        self.heuristica = heuristica
        self.puntaje = puntaje
        self.padre = padre
        self.celda = celda



"""---------ALGORITMO A*--------------------"""
class  AEstrella:
    def __init__(self, area):
        self.area = area    #Cuadricula de trabajo
        self.inicio = area.inicio #Ubicacion del inicio (posicion inicial de robot)
        self.fin = area.fin #Ubicacion del fin (posicion final de robot)
        self.openList = []
        self.closeList = []
        self.caminoFinal = []
    
    def isEmptyList(self, lista):
        return not lista
    
    def isCeldaInList(self, lista, objeto):
        return any(o.celda == objeto for o in lista)
        
    def distancia_manhattan(self, celda, x, y): #Para calcular distancia y heuristica
        return abs(celda.x+1 - x) + abs(celda.y+1 - y)
    
    def agregarLista(self, celdas_colindantes, celda_actual):
        #Revisa las celdas colindantes de la celda actual cumpliendo las siguientes condiciones
        # * La celda no sea un obstaculo
        # * La celda no se encuentre en la lista cerrada (aun no sea considerada)
        # * La celda no este en la lista abierta (ya sea colindante de otra celda)
        for c in celdas_colindantes:
            if c != None:
                if c.estado and not self.isCeldaInList(self.openList, c) and not self.isCeldaInList(self.closeList, c):
                    distancia = self.distancia_manhattan(c,(self.inicio[0]+1),(self.inicio[1]+1))
                    heuristica = self.distancia_manhattan(c,(self.fin[0]+1),(self.fin[1]+1))
                    self.openList.append(Nodo(distancia, heuristica, (distancia+heuristica), celda_actual, c))
                    print(f"Nodo añadido: ({c.x+1} , {c.y+1}), Padre: ({celda_actual.x+1} , {celda_actual.y+1}) ,Distancia: {distancia}, Heuristica: {heuristica}, Puntaje: {distancia+heuristica}")
    
    def obtenerMenorPuntaje(self):
        return min(self.openList, key=lambda nodo: nodo.puntaje)
    
    def eliminarNodo(self, nodo):
        self.openList.remove(nodo)

    def iteraciones(self, celda_actual):
        #A partir de la celda actual, se añaden los colindantes en contra de las manecillas del reloj y 
        #se obtiene el nodo menor
        celdas_colindantes = [celda_actual.norte, celda_actual.noroeste, celda_actual.oeste, celda_actual.suroeste,
                              celda_actual.sur, celda_actual.sureste, celda_actual.este, celda_actual.noreste]
        self.agregarLista(celdas_colindantes,celda_actual)
        menor_nodo = self.obtenerMenorPuntaje()
        return menor_nodo
        
    def algoritmo(self):
        #Ejecucion del algoritmo
        celda_actual = self.area.tabla[self.inicio[0]][self.inicio[1]]
        menor_nodo = self.iteraciones(celda_actual)
        self.closeList.append(menor_nodo)
        celda_actual = menor_nodo.celda
        self.eliminarNodo(menor_nodo)
        while(not self.isEmptyList(self.openList) and self.area.tabla[self.fin[0]][self.fin[1]] != celda_actual):
            menor_nodo = self.iteraciones(celda_actual)
            self.closeList.append(menor_nodo)
            celda_actual = menor_nodo.celda
            self.eliminarNodo(menor_nodo)
        self.obtenerRuta(menor_nodo)
        print("\n\nCONTENIDO DE LISTA CERRADA")
        for n in self.closeList:
            print(f"({n.celda.x+1} , {n.celda.y+1})")

    def buscarNodoPorCelda(self, celda):
        return next((nodo for nodo in self.closeList if nodo.celda == celda), None)
    
    def obtenerRuta(self, nodo):
        aux = nodo
        while aux.padre != self.area.tabla[self.inicio[0]][self.inicio[1]]:
            self.caminoFinal.append(aux.celda)
            aux = self.buscarNodoPorCelda(aux.padre)
        self.caminoFinal.append(aux.celda)  # Añadir la celda de inicio
        self.caminoFinal.append(self.area.tabla[self.inicio[0]][self.inicio[1]])
        self.caminoFinal.reverse()  # Invertir la lista para que el camino esté en el orden correcto




def main(args=None):
    celdas = [
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
    rclpy.init(args=args) #Inicializa rclpy para inicializar nodos de ros2 en python

    publicador_movimiento = PublicadorMovimiento(celdas) #Crea objeto de la clase

    rclpy.spin(publicador_movimiento) #Ejecuta la clase

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    PublicadorMovimiento.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
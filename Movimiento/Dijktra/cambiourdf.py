import os

class SpawnOrigin:
    def __init__(self, archivo_original, celdas):
        self.archivo_original = archivo_original
        self.x, self.y = self.obtenerValores(celdas)

    def obtenerValores(self,celdas):
        num_rows = len(celdas)
        num_cols = len(celdas[0])
        for i in range(num_rows):
            for j in range(num_cols):
                if celdas[i][j][1]: 
                    x = (i - num_rows / 2) * 0.4
                    y = (j - num_cols / 2) * 0.4  
        return x,y

    def guardarValores(self):
        proceso1 = proceso2 = proceso3 = proceso4 = proceso5 = proceso6 = proceso7 = False
        #enlaces = ['base_link', 'Rueda_Izquierda_Link', 'Rueda_Derecha_Link', 'Base_castor_Link', 'Rueda_Castor_Link']
        #proceso = []
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
                lineas[i] = f'                    "-x", \'{self.x}\',\n'
                proceso6 = True
            elif proceso6 and '"-y", ' in linea:
                lineas[i] = f'                    "-y", \'{self.y}\',\n'
                proceso7 = True
            elif proceso7 and '"-z",' in linea:
                proceso1 = proceso2 = proceso3 = proceso4 = proceso5 = proceso6 = proceso7 = False

        with open(self.archivo_original, 'w') as archivo:
            archivo.writelines(lineas)




class GeneracionMundo:
    def __init__(self,filename,celdas):
        self.filename = filename
        self.celdas = celdas


    def generate_world_file(self):
        with open(self.filename, 'w') as file:
            file.write("""<?xml version="1.0" ?>
    <sdf version="1.6">
    <world name="default">
        <include>
        <uri>model://ground_plane</uri>
        </include>
        <include>
        <uri>model://sun</uri>
        </include>
    """)

            num_rows = len(self.celdas)
            num_cols = len(self.celdas[0])
            cube_count = 1  # Variable para contar los cubos y generar nombres únicos
            for i in range(num_rows):
                for j in range(num_cols):
                    if not self.celdas[i][j][0]:  # Si el estado es False
                        x = (i - num_rows / 2) * 0.4
                        y = (j - num_cols / 2) * 0.4
                        cube_name = f"cube_{cube_count}"  # Nombre único para cada cubo
                        file.write(f"""
        <include>
        <uri>model://cube</uri>
        <name>{cube_name}</name>
        <pose>{x} {y} 0 0 0 0</pose>
        </include>
    """)
                        cube_count += 1  # Incrementar el contador de cubos
            
            for i in range(num_rows):
                for j in range(num_cols):
                    if self.celdas[i][j][2]:  # Si el estado es False
                        x = (i - num_rows / 2) * 0.4
                        y = (j - num_cols / 2) * 0.4
                        cube_name = f"cube_traslucido"  # Nombre único para cada cubo
                        file.write(f"""
        <include>
        <uri>model://cube_traslucid</uri>
        <name>{cube_name}</name>
        <pose>{x} {y} 0 0 0 0</pose>
        </include>
    """)
                        
            # Generación de paredes alrededor del perímetro
            # Ancho del perímetro (pared) de un cubo
            wall_width = 0.4
            
            # Definir las dimensiones de la matriz ampliada para incluir las paredes
            expanded_num_rows = num_rows + 2
            expanded_num_cols = num_cols + 2
            
            # Iterar para generar las paredes
            for i in range(expanded_num_rows):
                for j in range(expanded_num_cols):
                    if i == 0 or j == 0 or i == expanded_num_rows - 1 or j == expanded_num_cols - 1:
                        if not (0 < i < expanded_num_rows - 1 and 0 < j < expanded_num_cols - 1 and not self.celdas[i-1][j-1][0]):
                            x = (i - expanded_num_rows / 2) * 0.4
                            y = (j - expanded_num_cols / 2) * 0.4
                            cube_name = f"cube_wall_{cube_count}"  # Nombre único para cada cubo de pared
                            file.write(f"""
        <include>
        <uri>model://cube</uri>
        <name>{cube_name}</name>
        <pose>{x} {y} 0 0 0 0</pose>
        </include>
    """)
                            cube_count += 1  # Incrementar el contador de cubos
            
            file.write("""
    </world>
    </sdf>
    """)
                   
if __name__ == "__main__":
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
    inicio = SpawnOrigin('/home/user/robotA/src/robot/robot/launch/gazebo.launch.py', celdas)
    inicio.guardarValores()

    mundo = GeneracionMundo('/home/user/robotA/install/robot/share/robot/worlds/world.world', celdas)
    mundo.generate_world_file()


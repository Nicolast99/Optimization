# Pedir al usuario el número de máquinas de cada tipo
import random

num_maquinas_A = int(input("¿Cuántas máquinas de tipo A hay? "))
num_maquinas_B = int(input("¿Cuántas máquinas de tipo B hay? "))
num_maquinas_C = int(input("¿Cuántas máquinas de tipo C hay? "))

# Pedir al usuario el número de piezas
num_piezas = int(input("¿Cuántas piezas hay? "))

# Crear un diccionario para almacenar los tiempos de procesamiento de cada pieza
tiempos_piezas = {}

# Pedir los tiempos de procesamiento para cada pieza
for i in range(1, num_piezas + 1):
    print(f"Ingresando tiempos para la pieza {i}")
    tiempo_a = int(input("Tiempo en la máquina A (minutos): "))
    tiempo_b = int(input("Tiempo en la máquina B (minutos, 0 si no se procesa en esta máquina): "))
    tiempo_c = int(input("Tiempo en la máquina C (minutos): "))
    
    # Guardar los tiempos en el diccionario
    tiempos_piezas[f'pieza_{i}'] = {'A': tiempo_a, 'B': tiempo_b, 'C': tiempo_c}

# Función para calcular el tiempo total de procesamiento en un orden dado
def calcular_tiempo_total(orden_piezas, num_maquinas_A, num_maquinas_B, num_maquinas_C):
    # Inicializamos el tiempo de las máquinas como una lista para manejar múltiples máquinas en paralelo
    tiempos_A = [0] * num_maquinas_A
    tiempos_B = [0] * num_maquinas_B
    tiempos_C = [0] * num_maquinas_C

    # Lista para almacenar la asignación de cada pieza a una máquina
    asignaciones = []

    # Asignar tiempos de procesamiento a las máquinas A
    for pieza in orden_piezas:
        tiempo_a = tiempos_piezas[pieza]['A']
        maquina_disponible = tiempos_A.index(min(tiempos_A))
        tiempos_A[maquina_disponible] += tiempo_a
        asignaciones.append(f"{pieza} en A{maquina_disponible + 1}")

    # Asignar tiempos de procesamiento a las máquinas B
    for pieza in orden_piezas:
        tiempo_b = tiempos_piezas[pieza]['B']
        if tiempo_b > 0:
            maquina_disponible = tiempos_B.index(min(tiempos_B))
            tiempos_B[maquina_disponible] += tiempo_b
            asignaciones.append(f"{pieza} en B{maquina_disponible + 1}")

    # Asignar tiempos de procesamiento a las máquinas C
    for pieza in orden_piezas:
        tiempo_c = tiempos_piezas[pieza]['C']
        if tiempo_c > 0:
            maquina_disponible = tiempos_C.index(min(tiempos_C))
            tiempos_C[maquina_disponible] += tiempo_c
            asignaciones.append(f"{pieza} en C{maquina_disponible + 1}")

    # El tiempo total será el máximo de cada conjunto de máquinas
    tiempo_total = max(tiempos_A) + max(tiempos_B) + max(tiempos_C)
    
    return tiempo_total, asignaciones


# Función de optimización con ACO
def optimizar_con_ACO(num_maquinas_A, num_maquinas_B, num_maquinas_C):
    mejor_tiempo = float('inf')
    mejor_orden = None
    mejor_asignacion = None
    
    num_hormigas = 100  # Número de hormigas (intentos)
    
    for _ in range(num_hormigas):
        orden_actual = list(tiempos_piezas.keys())  # Lista de las piezas
        random.shuffle(orden_actual)  # Mezclar el orden de las piezas
        
        # Calcular el tiempo total para este orden
        tiempo_actual, asignaciones_actuales = calcular_tiempo_total(orden_actual, num_maquinas_A, num_maquinas_B, num_maquinas_C)
        
        if tiempo_actual < mejor_tiempo:
            mejor_tiempo = tiempo_actual
            mejor_orden = orden_actual
            mejor_asignacion = asignaciones_actuales
    
    return mejor_orden, mejor_tiempo, mejor_asignacion

# Función de optimización con IG
def optimizar_con_IG(num_maquinas_A, num_maquinas_B, num_maquinas_C):
    orden_inicial = list(tiempos_piezas.keys())
    mejor_orden = orden_inicial
    mejor_tiempo, mejor_asignacion = calcular_tiempo_total(orden_inicial, num_maquinas_A, num_maquinas_B, num_maquinas_C)
    
    for _ in range(100):  # 100 intentos de mejora
        nuevo_orden = mejor_orden[:]
        i, j = random.sample(range(len(nuevo_orden)), 2)
        nuevo_orden[i], nuevo_orden[j] = nuevo_orden[j], nuevo_orden[i]
        
        nuevo_tiempo, nueva_asignacion = calcular_tiempo_total(nuevo_orden, num_maquinas_A, num_maquinas_B, num_maquinas_C)
        
        if nuevo_tiempo < mejor_tiempo:
            mejor_tiempo = nuevo_tiempo
            mejor_orden = nuevo_orden
            mejor_asignacion = nueva_asignacion
    
    return mejor_orden, mejor_tiempo, mejor_asignacion

# Ejecutar la optimización ACO
mejor_orden_aco, mejor_tiempo_aco, asignaciones_aco = optimizar_con_ACO(num_maquinas_A, num_maquinas_B, num_maquinas_C)
print(f"ACO: El mejor orden es {mejor_orden_aco} con un tiempo total de {mejor_tiempo_aco} minutos")
print("Asignaciones ACO:")
for asignacion in asignaciones_aco:
    print(asignacion)

# Ejecutar la optimización IG
mejor_orden_ig, mejor_tiempo_ig, asignaciones_ig = optimizar_con_IG(num_maquinas_A, num_maquinas_B, num_maquinas_C)
print(f"IG: El mejor orden es {mejor_orden_ig} con un tiempo total de {mejor_tiempo_ig} minutos")
print("Asignaciones IG:")
for asignacion in asignaciones_ig:
    print(asignacion)

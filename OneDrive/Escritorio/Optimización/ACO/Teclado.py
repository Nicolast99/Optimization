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
def calcular_tiempo_total(orden_piezas):
    tiempo_total = 0
    
    for pieza in orden_piezas:
        tiempo_total += tiempos_piezas[pieza]['A'] + tiempos_piezas[pieza]['B'] + tiempos_piezas[pieza]['C']
    
    return tiempo_total

import random

# Función de optimización con ACO
def optimizar_con_ACO():
    mejor_tiempo = float('inf')
    mejor_orden = None
    
    num_hormigas = 100  # Número de hormigas (intentos)
    
    # Cada hormiga prueba un orden aleatorio de las piezas
    for _ in range(num_hormigas):
        orden_actual = list(tiempos_piezas.keys())  # Lista de las piezas
        random.shuffle(orden_actual)  # Mezclar el orden de las piezas
        
        # Calcular el tiempo total para este orden
        tiempo_actual = calcular_tiempo_total(orden_actual)
        
        # Si el tiempo es mejor que el mejor tiempo registrado, lo actualizamos
        if tiempo_actual < mejor_tiempo:
            mejor_tiempo = tiempo_actual
            mejor_orden = orden_actual
    
    return mejor_orden, mejor_tiempo

# Ejecutar la optimización ACO
mejor_orden_aco, mejor_tiempo_aco = optimizar_con_ACO()
print(f"ACO: El mejor orden es {mejor_orden_aco} con un tiempo total de {mejor_tiempo_aco} minutos")

# Función de optimización con IG
def optimizar_con_IG():
    # Empezamos con el orden original de las piezas
    orden_inicial = list(tiempos_piezas.keys())
    mejor_orden = orden_inicial
    mejor_tiempo = calcular_tiempo_total(orden_inicial)
    
    # Intentamos mejorar el orden intercambiando piezas aleatoriamente
    for _ in range(100):  # 100 intentos de mejora
        # Crear una copia del mejor orden
        nuevo_orden = mejor_orden[:]
        
        # Intercambiar dos piezas al azar
        i, j = random.sample(range(len(nuevo_orden)), 2)
        nuevo_orden[i], nuevo_orden[j] = nuevo_orden[j], nuevo_orden[i]
        
        # Calcular el tiempo para el nuevo orden
        nuevo_tiempo = calcular_tiempo_total(nuevo_orden)
        
        # Si el nuevo tiempo es mejor, lo guardamos
        if nuevo_tiempo < mejor_tiempo:
            mejor_tiempo = nuevo_tiempo
            mejor_orden = nuevo_orden
    
    return mejor_orden, mejor_tiempo

# Ejecutar la optimización IG
mejor_orden_ig, mejor_tiempo_ig = optimizar_con_IG()
print(f"IG: El mejor orden es {mejor_orden_ig} con un tiempo total de {mejor_tiempo_ig} minutos")

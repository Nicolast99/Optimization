import random
import numpy as np

# Pedir al usuario el número de máquinas de cada tipo
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

# Función para calcular la matriz de distancias entre las piezas
def calcular_distancias(num_piezas):
    bound = 100
    x = np.random.rand(num_piezas) * bound
    y = np.random.rand(num_piezas) * bound
    D = np.zeros((num_piezas, num_piezas))

    for i in range(num_piezas - 1):
        for j in range(i + 1, num_piezas):
            D[i, j] = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            D[j, i] = D[i, j]
    
    return D

# Función para calcular la longitud de un tour
def tour_length(tour, D):
    tour = list(tour) + [tour[0]]
    L = sum(D[tour[i], tour[i + 1]] for i in range(len(tour) - 1))
    return L

# Función de optimización con ACO adaptada para tiempos de procesamiento
def optimizar_con_ACO_tiempos(num_piezas, num_maquinas_A, num_maquinas_B, num_maquinas_C):
    N = 40  # Número de hormigas
    Q = 1
    alpha = 1
    beta = 1
    rho = 0.05
    kmax = 1000  # Número de iteraciones
    tau_0 = 1.0  # Inicializar feromonas con un valor base
    tau = tau_0 * np.ones((num_piezas, num_piezas))  # Matriz de feromonas inicial
    eta = np.ones((num_piezas, num_piezas))  # Para este caso, visibilidad es constante
    best_tour = None
    best_fit = np.inf
    f_hist = np.zeros(kmax)

    for it in range(kmax):
        ants = []

        # Crear tours para todas las hormigas
        for _ in range(N):
            tour = [random.randint(0, num_piezas - 1)]  # Empezar con una pieza aleatoria
            while len(tour) < num_piezas:
                i = tour[-1]
                P = (tau[i, :] ** alpha) * (eta[i, :] ** beta)
                P[tour] = 0  # Evitar repetir nodos
                P = P / P.sum()  # Normalizar probabilidades
                j = np.random.choice(range(num_piezas), p=P)  # Seleccionar próxima pieza
                tour.append(j)
            ants.append(tour)

        # Evaluar las hormigas usando la función de tiempos
        for ant in ants:
            # Convertimos el tour en el formato correcto (pieza_1, pieza_2, etc.)
            orden_piezas = [f'pieza_{i + 1}' for i in ant]
            fit, _ = calcular_tiempo_total(orden_piezas, num_maquinas_A, num_maquinas_B, num_maquinas_C)

            if fit < best_fit:
                best_tour = ant
                best_fit = fit

        # Actualizar feromonas basado en el fitness
        for ant in ants:
            orden_piezas = [f'pieza_{i + 1}' for i in ant]
            fit, _ = calcular_tiempo_total(orden_piezas, num_maquinas_A, num_maquinas_B, num_maquinas_C)

            for i in range(num_piezas - 1):
                tau[ant[i], ant[i + 1]] += Q / fit

        # Evaporación de feromonas
        tau = (1 - rho) * tau

        f_hist[it] = best_fit
        if it % 100 == 0:
            print(f"Iteración {it}: Tiempo total (fitness) = {best_fit}")

    # Devolver el mejor tour y fitness encontrados
    mejor_orden = [f'pieza_{i + 1}' for i in best_tour]
    return mejor_orden, best_fit, f_hist

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

# Ejecutar la optimización ACO ajustada para tiempos de procesamiento
mejor_orden_aco, mejor_tiempo_aco, f_hist_aco = optimizar_con_ACO_tiempos(num_piezas, num_maquinas_A, num_maquinas_B, num_maquinas_C)
print(f"ACO ajustado: El mejor orden es {mejor_orden_aco} con un tiempo total de {mejor_tiempo_aco} minutos")


# Ejecutar la optimización IG
mejor_orden_ig, mejor_tiempo_ig, asignaciones_ig = optimizar_con_IG(num_maquinas_A, num_maquinas_B, num_maquinas_C)
print(f"IG: El mejor orden es {mejor_orden_ig} con un tiempo total de {mejor_tiempo_ig} minutos")
print("Asignaciones IG:")
for asignacion in asignaciones_ig:
    print(asignacion)

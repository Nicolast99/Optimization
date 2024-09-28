import random
import numpy as np

# Función para validar el orden de máquinas ingresado
def validar_orden(entrada, maquinas_disponibles):
    orden = entrada.upper().split('-')
    if len(orden) != len(maquinas_disponibles):
        return None
    if sorted(orden) != sorted(maquinas_disponibles):
        return None
    return orden

# Pedir al usuario el número de máquinas de cada tipo
num_maquinas_A = int(input("¿Cuántas máquinas de tipo A hay? "))
num_maquinas_B = int(input("¿Cuántas máquinas de tipo B hay? "))
num_maquinas_C = int(input("¿Cuántas máquinas de tipo C hay? "))

# Definir los tipos de máquinas disponibles
tipos_maquinas = ['A'] * num_maquinas_A + ['B'] * num_maquinas_B + ['C'] * num_maquinas_C

# Pedir al usuario el número de piezas
num_piezas = int(input("¿Cuántas piezas hay? "))

# Crear un diccionario para almacenar los tiempos de procesamiento y el orden de máquinas de cada pieza
piezas_info = {}

# Pedir los tiempos de procesamiento y el orden de máquinas para cada pieza
for i in range(1, num_piezas + 1):
    print(f"\nIngresando información para la pieza {i}")
    
    # Solicitar el orden de máquinas
    while True:
        orden_input = input("Ingrese el orden de máquinas separado por guiones (por ejemplo, A-B-C): ")
        orden_maquinas = validar_orden(orden_input, ['A', 'B', 'C'])
        if orden_maquinas:
            break
        else:
            print("Orden inválido. Asegúrese de incluir todas las máquinas una vez y solo una vez.")
    
    # Solicitar los tiempos de procesamiento según el orden de máquinas
    tiempos = {}
    for maquina in orden_maquinas:
        tiempo = int(input(f"Tiempo en la máquina {maquina} (minutos, 0 si no se procesa en esta máquina): "))
        tiempos[maquina] = tiempo
    
    # Guardar la información de la pieza
    piezas_info[f'pieza_{i}'] = {
        'orden_maquinas': orden_maquinas,
        'tiempos': tiempos
    }

# Función para calcular el tiempo total de procesamiento en un orden dado
def calcular_tiempo_total(orden_piezas, num_maquinas_A, num_maquinas_B, num_maquinas_C):
    # Inicializamos el tiempo de las máquinas como una lista para manejar múltiples máquinas en paralelo
    tiempos_A = [0] * num_maquinas_A
    tiempos_B = [0] * num_maquinas_B
    tiempos_C = [0] * num_maquinas_C

    # Diccionario para rastrear el tiempo en que cada pieza termina su procesamiento
    fin_piezas = {pieza: 0 for pieza in orden_piezas}

    # Lista para almacenar la asignación de cada pieza a una máquina
    asignaciones = []

    for pieza in orden_piezas:
        info = piezas_info[pieza]
        orden_maquinas = info['orden_maquinas']
        tiempos = info['tiempos']
        tiempo_fin_anterior = 0

        for maquina in orden_maquinas:
            if tiempos[maquina] == 0:
                continue  # Si no se procesa en esta máquina, saltar

            if maquina == 'A':
                maquina_disponible = tiempos_A.index(min(tiempos_A))
                inicio = max(tiempos_A[maquina_disponible], tiempo_fin_anterior)
                tiempos_A[maquina_disponible] = inicio + tiempos[maquina]
                fin_piezas[pieza] = tiempos_A[maquina_disponible]
                asignaciones.append(f"{pieza} en A{maquina_disponible + 1} desde {inicio} hasta {tiempos_A[maquina_disponible]}")
            elif maquina == 'B':
                maquina_disponible = tiempos_B.index(min(tiempos_B))
                inicio = max(tiempos_B[maquina_disponible], tiempo_fin_anterior)
                tiempos_B[maquina_disponible] = inicio + tiempos[maquina]
                fin_piezas[pieza] = tiempos_B[maquina_disponible]
                asignaciones.append(f"{pieza} en B{maquina_disponible + 1} desde {inicio} hasta {tiempos_B[maquina_disponible]}")
            elif maquina == 'C':
                maquina_disponible = tiempos_C.index(min(tiempos_C))
                inicio = max(tiempos_C[maquina_disponible], tiempo_fin_anterior)
                tiempos_C[maquina_disponible] = inicio + tiempos[maquina]
                fin_piezas[pieza] = tiempos_C[maquina_disponible]
                asignaciones.append(f"{pieza} en C{maquina_disponible + 1} desde {inicio} hasta {tiempos_C[maquina_disponible]}")
            
            # Actualizar el tiempo fin anterior para la siguiente máquina de la pieza
            tiempo_fin_anterior = fin_piezas[pieza]

    # El tiempo total será el máximo de los tiempos fin de todas las piezas
    tiempo_total = max(fin_piezas.values())
    
    return tiempo_total, asignaciones

# Función para calcular la matriz de distancias entre las piezas (mantiene original, puede ser ajustada si es necesario)
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

# Función para calcular la longitud de un tour (no se usa directamente en el cálculo de tiempo, puede ser relevante para otras optimizaciones)
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
                if P.sum() == 0:
                    break  # No hay más nodos disponibles
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

            for i in range(len(ant) - 1):
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
    orden_inicial = list(piezas_info.keys())
    mejor_orden = orden_inicial
    mejor_tiempo, mejor_asignacion = calcular_tiempo_total(mejor_orden, num_maquinas_A, num_maquinas_B, num_maquinas_C)
    
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
print(f"\nACO ajustado: El mejor orden es {mejor_orden_aco} con un tiempo total de {mejor_tiempo_aco} minutos")

# Ejecutar la optimización IG
mejor_orden_ig, mejor_tiempo_ig, asignaciones_ig = optimizar_con_IG(num_maquinas_A, num_maquinas_B, num_maquinas_C)
print(f"\nIG: El mejor orden es {mejor_orden_ig} con un tiempo total de {mejor_tiempo_ig} minutos")
print("Asignaciones IG:")
for asignacion in asignaciones_ig:
    print(asignacion)

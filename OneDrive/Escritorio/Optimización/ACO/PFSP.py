import numpy as np
import random

# Definir los tiempos de procesamiento específicos para cada trabajo y máquina
processing_times = np.array([
    [20, 30, 25, 35, 40],  # Job 0
    [35, 25, 30, 20, 25],  # Job 1
    [40, 20, 20, 30, 35],  # Job 2
    [30, 25, 35, 25, 30],  # Job 3
    #[25, 30, 40, 35, 20],  # Job 4
    #[20, 30, 35, 40, 25],  # Job 5
    #[30, 20, 25, 35, 30],  # Job 6
    #[35, 25, 30, 20, 40],  # Job 7
    #[40, 20, 30, 25, 30],  # Job 8
    #[25, 35, 20, 30, 25]   # Job 9 
])

# Inicialización de parámetros
num_jobs = processing_times.shape[0]
num_machines = processing_times.shape[1]
pheromone_initial = 1.0
pheromone_min = 0.1
pheromone_max = 10.0
alpha = 1.0
beta = 2.0
evaporation_rate = 0.5
num_ants = 10
iterations = 1000

# Inicialización de feromonas
pheromones = np.full((num_jobs, num_jobs), pheromone_initial)

def schedule_length(schedule):
    completion_times = np.zeros((num_jobs, num_machines))
    for i in range(num_jobs):
        for j in range(num_machines):
            if i == 0 and j == 0:
                completion_times[i, j] = processing_times[schedule[i], j]
            elif i == 0:
                completion_times[i, j] = completion_times[i, j-1] + processing_times[schedule[i], j]
            elif j == 0:
                completion_times[i, j] = completion_times[i-1, j] + processing_times[schedule[i], j]
            else:
                completion_times[i, j] = max(completion_times[i-1, j], completion_times[i, j-1]) + processing_times[schedule[i], j]
    return completion_times[-1, -1]

def update_pheromones(best_schedule, best_length):
    for i in range(num_jobs - 1):
        pheromones[best_schedule[i], best_schedule[i+1]] *= (1 - evaporation_rate)
        pheromones[best_schedule[i], best_schedule[i+1]] += (1 / best_length)
        pheromones[best_schedule[i], best_schedule[i+1]] = min(max(pheromones[best_schedule[i], best_schedule[i+1]], pheromone_min), pheromone_max)

def local_search(schedule):
    best_schedule = schedule
    best_length = schedule_length(schedule)
    for i in range(num_jobs):
        for j in range(i + 1, num_jobs):
            new_schedule = schedule.copy()
            new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
            new_length = schedule_length(new_schedule)
            if new_length < best_length:
                best_schedule = new_schedule
                best_length = new_length
    return best_schedule

# Bucle principal del algoritmo ACO
best_global_schedule = None
best_global_length = float('inf')

for iteration in range(iterations):
    schedules = []
    lengths = []

    for ant in range(num_ants):
        schedule = []
        visited = set()
        for _ in range(num_jobs):
            probabilities = []
            current_job = schedule[-1] if schedule else random.randint(0, num_jobs - 1)
            for job in range(num_jobs):
                if job not in visited:
                    probabilities.append((pheromones[current_job, job] ** alpha) * ((1 / (processing_times[job].sum())) ** beta))
                else:
                    probabilities.append(0)
            probabilities = np.array(probabilities)
            probabilities /= probabilities.sum()
            next_job = np.random.choice(range(num_jobs), p=probabilities)
            schedule.append(next_job)
            visited.add(next_job)
        schedules.append(schedule)
        lengths.append(schedule_length(schedule))
    
    best_local_schedule = schedules[np.argmin(lengths)]
    best_local_length = min(lengths)

    best_local_schedule = local_search(best_local_schedule)
    best_local_length = schedule_length(best_local_schedule)

    if best_local_length < best_global_length:
        best_global_schedule = best_local_schedule
        best_global_length = best_local_length
    
    update_pheromones(best_global_schedule, best_global_length)

print("Mejor secuencia encontrada:", best_global_schedule)
print("Longitud del makespan:", best_global_length)

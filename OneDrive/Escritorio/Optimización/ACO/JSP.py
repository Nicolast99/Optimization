import numpy as np
import random
import matplotlib.pyplot as plt

def initialize_pheromone_matrix(num_jobs, num_machines):
    pheromone_matrix = np.random.rand(num_jobs, num_machines)
    return pheromone_matrix

def calculate_visibility_matrix(processing_times):
    with np.errstate(divide='ignore', invalid='ignore'):
        visibility_matrix = np.where(processing_times > 0, 1.0 / processing_times, 0)
    return visibility_matrix

def generate_random_tour(num_jobs):
    tour = np.random.permutation(num_jobs)
    return tour

def calculate_tour_time(tour, processing_times):
    tour_time = 0
    for i in range(len(tour) - 1):
        current_job = tour[i]
        next_job = tour[i + 1]
        tour_time += processing_times[current_job, next_job]
    return tour_time

def select_next_machine(probabilities, tabu_list):
    available_machines = [i for i in range(len(probabilities)) if i not in tabu_list]
    if not available_machines:
        return random.choice(range(len(probabilities)))
    probabilities = np.array([probabilities[i] if i in available_machines else 0 for i in range(len(probabilities))])
    if np.sum(probabilities) == 0:
        return random.choice(available_machines)
    else:
        probabilities /= np.sum(probabilities)
        return np.random.choice(range(len(probabilities)), p=probabilities)

def update_pheromone_matrix(pheromone_matrix, tour, rho, Q, processing_times):
    tour_time = calculate_tour_time(tour, processing_times)
    if tour_time == 0:
        return
    for i in range(len(tour) - 1):
        pheromone_matrix[tour[i], tour[i + 1]] = (1 - rho) * pheromone_matrix[tour[i], tour[i + 1]] + Q / tour_time

def calculate_probabilities(pheromone_matrix, visibility_matrix, current_job, tabu_list, num_machines):
    probabilities = np.zeros(num_machines)
    for machine in range(num_machines):
        if machine not in tabu_list:
            probabilities[machine] = pheromone_matrix[current_job, machine] * visibility_matrix[current_job, machine]
    if np.sum(probabilities) > 0:
        probabilities /= np.sum(probabilities)
    else:
        probabilities = np.zeros(num_machines)
    return probabilities

def plot_gantt_chart(schedule, processing_times):
    fig, gnt = plt.subplots()
    
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Máquinas')
    gnt.set_yticks([i + 1 for i in range(len(processing_times))])
    gnt.set_yticklabels(['Máquina {}'.format(i + 1) for i in range(len(processing_times))])
    gnt.grid(True)

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    start_times = [0] * len(processing_times)

    for job in range(len(schedule)):
        machine = schedule[job]
        if machine >= len(start_times):
            continue
        processing_time = processing_times[job, machine]
        gnt.broken_barh([(start_times[machine], processing_time)], (machine + 0.5, 0.8), facecolors=(colors[job % len(colors)]))
        start_times[machine] += processing_time

    plt.show()

num_jobs = 4
num_machines = 5
processing_times = np.array([
    [10, 0, 20, 5, 10],
    [15, 15, 0, 0, 10],
    [5, 8, 12, 20, 0],
    [0, 10, 5, 15, 20],
   #[20, 30, 25, 35, 40],  # Job 0
    #[35, 25, 30, 20, 25],  # Job 1
    #[40, 20, 20, 30, 35],  # Job 2
    #[30, 25, 35, 25, 30],  # Job 3
    #[25, 30, 40, 35, 20],  # Job 4
    #[20, 30, 35, 40, 25],  # Job 5
    #[30, 20, 25, 35, 30],  # Job 6
    #[35, 25, 30, 20, 40],  # Job 7
    #[40, 20, 30, 25, 30],  # Job 8
    #[25, 35, 20, 30, 25]   # Job 9 
])
ant_count = 10
iterations = 1000
rho = 0.5
Q = 1.0

pheromone_matrix = initialize_pheromone_matrix(num_jobs, num_machines)
visibility_matrix = calculate_visibility_matrix(processing_times)

best_tour = None
best_tour_time = np.inf
best_schedule = None

for iteration in range(iterations):
    population = []
    for _ in range(ant_count):
        tour = generate_random_tour(num_jobs)
        population.append(tour)

    schedules = []
    for tour in population:
        schedule = []
        tabu_list = []
        for i in range(num_jobs):
            current_job = tour[i]
            tabu_list.append(current_job)
            probabilities = calculate_probabilities(pheromone_matrix, visibility_matrix, current_job, tabu_list, num_machines)
            next_machine = select_next_machine(probabilities, tabu_list)
            schedule.append(next_machine)
        schedules.append(schedule)

    tour_times = []
    for tour in population:
        tour_time = calculate_tour_time(tour, processing_times)
        tour_times.append(tour_time)

    min_tour_time = min(tour_times)
    min_tour_index = tour_times.index(min_tour_time)
    if best_tour_time > min_tour_time:
        best_tour = population[min_tour_index].tolist()
        best_tour_time = min_tour_time
        best_schedule = schedules[min_tour_index]

    for tour in population:
        update_pheromone_matrix(pheromone_matrix, tour, rho, Q, processing_times)

print("Secuencia de asignaciones:", best_tour)
print("Máquinas asignadas:", best_schedule)
print("Makespan:", best_tour_time)

plot_gantt_chart(best_schedule, processing_times)


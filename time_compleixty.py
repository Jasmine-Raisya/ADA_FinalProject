import itertools
import random
import time

# Define the tasks
tasks = [
    ('Mix Ingredients', 10, 'Mixer A'),
    ('Bake Bread', 30, 'Oven B'),
    ('Pack Breads', 15, 'Packaging Machine C'),
    ('Quality Check', 20, 'Quality Control D'),
    ('Mix Dough', 12, 'Mixer A'),
    ('Bake Cookies', 25, 'Oven B'),
    ('Pack Cookies', 18, 'Packaging Machine C'),
    ('Quality Check Cookies', 15, 'Quality Control D')
]

# Greedy Scheduling
def greedy_schedule(tasks):
    machines = {}
    for task, duration, machine in tasks:
        if machine not in machines:
            machines[machine] = []
        machines[machine].append((task, duration))
    
    schedule = {}
    for machine, jobs in machines.items():
        total_time = sum(duration for _, duration in jobs)
        schedule[machine] = (jobs, total_time)
    
    return schedule

# Brute Force Scheduling
def brute_force_schedule(tasks):
    best_schedule = None
    best_time = float('inf')
    
    for perm in itertools.permutations(tasks):
        machines = {}
        for task, duration, machine in perm:
            if machine not in machines:
                machines[machine] = []
            machines[machine].append((task, duration))
        
        total_time = max(sum(duration for _, duration in jobs) for jobs in machines.values())
        
        if total_time < best_time:
            best_time = total_time
            best_schedule = machines
    
    return best_schedule, best_time

# Simulated Annealing Scheduling
def simulated_annealing_schedule(tasks, initial_temp=1000, cooling_rate=0.95):
    current_schedule = greedy_schedule(tasks)
    current_time = max(total_time for _, total_time in current_schedule.values())
    
    temperature = initial_temp
    
    while temperature > 1:
        # Randomly swap two tasks
        new_tasks = tasks[:]
        i, j = random.sample(range(len(new_tasks)), 2)
        new_tasks[i], new_tasks[j] = new_tasks[j], new_tasks[i]
        
        new_schedule = greedy_schedule(new_tasks)
        new_time = max(total_time for _, total_time in new_schedule.values())
        
        # Accept the new schedule if it's better or with a probability
        if new_time < current_time or random.uniform(0, 1) < temperature / initial_temp:
            current_schedule = new_schedule
            current_time = new_time
        
        temperature *= cooling_rate
    
    return current_schedule, current_time

# Measure performance
def measure_performance():
    start_time = time.perf_counter()
    greedy_result = greedy_schedule(tasks)
    greedy_duration = time.perf_counter() - start_time
    
    start_time = time.perf_counter()
    brute_force_result, brute_force_duration = brute_force_schedule(tasks)
    brute_force_duration = time.perf_counter() - start_time
    
    start_time = time.perf_counter()
    simulated_annealing_result, simulated_annealing_duration = simulated_annealing_schedule(tasks)
    simulated_annealing_duration = time.perf_counter() - start_time
    
    print("Greedy Scheduling Result:")
    print(greedy_result)
    print(f"Total Time: {max(total_time for _, total_time in greedy_result.values())} minutes")
    print(f"Execution Time: {greedy_duration * 1_000_000_000:.0f} nanoseconds\n")  # Convert to nanoseconds

    print("Brute Force Scheduling Result:")
    print(brute_force_result)
    print(f"Total Time: {brute_force_duration:.0f} minutes")
    print(f"Execution Time: {brute_force_duration * 1_000_000_000:.0f} nanoseconds\n")  # Convert to nanoseconds

    print("Simulated Annealing Scheduling Result:")
    print(simulated_annealing_result)
    print(f"Total Time: {simulated_annealing_duration:.0f} minutes")
    print(f"Execution Time: {simulated_annealing_duration * 1_000_000_000:.0f} nanoseconds\n")  # Convert to nanoseconds

# Run performance measurement
measure_performance()
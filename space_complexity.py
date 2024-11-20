import random
import time
import itertools
from memory_profiler import memory_usage

# Define a function to generate tasks
def generate_tasks(num_tasks):
    tasks = []
    for i in range(num_tasks):
        duration = random.randint(1, 30)  # Random duration between 1 and 30 minutes
        machine = f'Machine {random.choice(["A", "B", "C", "D"])}'
        tasks.append((f'Task {i + 1}', duration, machine))
    return tasks

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
    
    return best_schedule

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
    
    return current_schedule

# Measure memory usage of the scheduling methods
def measure_memory(num_tasks):
    tasks = generate_tasks(num_tasks)
    
    # Measure memory usage for Greedy
    greedy_mem = memory_usage((greedy_schedule, (tasks,)), max_usage=True)
    
    # Measure memory usage for Brute Force
    brute_force_mem = memory_usage((brute_force_schedule, (tasks,)), max_usage=True)
    
    # Measure memory usage for Simulated Annealing
    simulated_annealing_mem = memory_usage((simulated_annealing_schedule, (tasks,)), max_usage=True)
    
    return greedy_mem, brute_force_mem, simulated_annealing_mem

# Main function to run the memory profiling
def main():
    task_sizes = [10, 50, 100, 200]  # Different sizes of tasks
    results = []

    for size in task_sizes:
        greedy_mem, brute_force_mem, simulated_annealing_mem = measure_memory(size)
        results.append((size, greedy_mem, brute_force_mem, simulated_annealing_mem))

    # Print the results
    print("Task Size | Greedy Memory Usage | Brute Force Memory Usage | Simulated Annealing Memory Usage")
    print("------------------------------------------------------------------------------------------")
    for size, greedy_mem, brute_force_mem, simulated_annealing_mem in results:
        print(f"{size:10} | {greedy_mem[0]:20.2f} MiB | {brute_force_mem[0]:23.2f} MiB | {simulated_annealing_mem[0]:27.2f} MiB")

if __name__ == "__main__":
    main()
import numpy as np
import math

# Priority queue implementation
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, item, priority):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda x: x[0])

    def pop(self):
        if not self.is_empty():
            return self.queue.pop(0)[1]
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        if not self.is_empty():
            return self.queue[0][1]
        return None

# Function to generate truncated normal distribution
def truncated_normal(mean, std, low, high):
    while True:
        value = np.random.normal(mean, std)
        if low <= value <= high:
            return value

def non_normal(low, high):
    while True:
        value = np.random.normal(5, 15)
        if low <= value <= high:
            return value

# Simulation function for the base case (no priority queue)
def simulate_base_case(num_windows, num_customers, total_time, work_units):
    windows = PriorityQueue()
    for _ in range(num_windows):
        windows.push(0, 0)  # All windows start available at time 0

    arrival_times = np.random.uniform(0, total_time, num_customers)
    arrival_times.sort()

    # Parameters
    waiting_times = []
    served_customers = 0
    unserved_customers = 0
    window_busy_time = [0] * num_windows  # Track busy time for utilization

    for i in range(num_customers):
        arrival_time = arrival_times[i]
        work_unit = work_units[i]

        window_end_time = windows.pop()
        if window_end_time <= arrival_time:
            start_time = arrival_time
        else:
            start_time = window_end_time

        end_time = start_time + (work_unit / 10) * 60  # Convert work-units to minutes
        waiting_time = start_time - arrival_time
        waiting_times.append(waiting_time)

        windows.push(end_time, end_time)

        if end_time <= total_time:
            served_customers += 1
            window_busy_time[i % num_windows] += (end_time - start_time)
        else:
            unserved_customers += 1

    avg_waiting_time = np.mean(waiting_times)
    utilization_rate = np.sum(window_busy_time) / (num_windows * total_time) * 100
    return avg_waiting_time, served_customers, unserved_customers, utilization_rate

# Simulation function for the priority queue case (light requests prioritized)
def simulate_priority_case(num_windows, num_customers, total_time, work_units):
    windows = PriorityQueue()
    for _ in range(num_windows):
        windows.push(0, 0)

    arrival_times = np.random.uniform(0, total_time, num_customers)
    arrival_times.sort()

    # Parameters
    waiting_times = []
    served_customers = 0
    unserved_customers = 0
    window_busy_time = [0] * num_windows

    # Separate queues for light and heavy requests
    light_queue = PriorityQueue()
    heavy_queue = PriorityQueue()

    for i in range(num_customers):
        arrival_time = arrival_times[i]
        work_unit = work_units[i]

        if work_unit <= 5:  # Light request
            light_queue.push((arrival_time, work_unit), arrival_time)
        else:  # Heavy request
            heavy_queue.push((arrival_time, work_unit), arrival_time)

    while not light_queue.is_empty() or not heavy_queue.is_empty():
        # Prioritize light requests
        if not light_queue.is_empty():
            arrival_time, work_unit = light_queue.pop()
        else:
            arrival_time, work_unit = heavy_queue.pop()

        window_end_time = windows.pop()
        if window_end_time <= arrival_time:
            start_time = arrival_time
        else:
            start_time = window_end_time

        end_time = start_time + (work_unit / 10) * 60
        waiting_time = start_time - arrival_time
        waiting_times.append(waiting_time)

        windows.push(end_time, end_time)

        if end_time <= total_time:
            served_customers += 1
            window_busy_time[i % num_windows] += (end_time - start_time)
        else:
            unserved_customers += 1

    avg_waiting_time = np.mean(waiting_times)
    utilization_rate = np.sum(window_busy_time) / (num_windows * total_time) * 100
    return avg_waiting_time, served_customers, unserved_customers, utilization_rate

def simulate_multiple_times(simulation_func, num_windows, num_customers, total_time, num_runs):
    # intialize list to store result
    avg_waiting_times = []
    served_customers_list = []
    unserved_customers_list = []
    utilization_rates = []

    for _ in range(num_runs):
        # Generate new work units for each run (to avoid bias)
        work_units = [truncated_normal(5, .5, 5, 15) for _ in range(num_customers)]

        # Run the simulation
        avg_wait, served, unserved, utilization = simulation_func( num_windows, num_customers, total_time, work_units)

        # Store results
        avg_waiting_times.append(avg_wait)
        served_customers_list.append(served)
        unserved_customers_list.append(unserved)
        utilization_rates.append(utilization)

    # Calculate mean results
    return (
        np.mean(avg_waiting_times),
        np.mean(served_customers_list),
        np.mean(unserved_customers_list),
        np.mean(utilization_rates),
    )

# Parameters
num_windows = 10
num_customers = 160
total_time = 8 * 60  # 8 hours in minutes
num_runs = 10000
work_units = [truncated_normal(5, 0.5, 5, 15) for _ in range(num_customers)]
non_normal_work_units = [non_normal(5, 15) for _ in range(num_customers)]

print(f"\nRunning FIFO (Base Case) {num_runs} times...")
avg_wait_fifo, served_fifo, unserved_fifo, util_fifo = simulate_multiple_times(
    simulate_base_case, num_windows, num_customers, total_time, num_runs
)

print(f"\nRunning Priority Queue {num_runs} times...")
avg_wait_priority, served_priority, unserved_priority, util_priority = simulate_multiple_times(
    simulate_priority_case, num_windows, num_customers, total_time, num_runs
)

print(f"\n=== Results (Averaged over {num_runs} runs) ===")
print("\nFIFO Queue (Base Case):")
print(f"Average Wait Time: {avg_wait_fifo:.2f} min")
print(f"Average Served: {served_fifo:.1f} customers")
print(f"Average Unserved: {unserved_fifo:.1f} customers")
print(f"Average Utilization: {util_fifo:.2f}%")

print("\nPriority Queue (Light Requests First):")
print(f"Average Wait Time: {avg_wait_priority:.2f} min")
print(f"Average Served: {served_priority:.1f} customers")
print(f"Average Unserved: {unserved_priority:.1f} customers")
print(f"Average Utilization: {util_priority:.2f}%")

print("-------------------------------------------------------------------")
# Run simulations
print("Base Case (10 windows, FIFO):")
avg_waiting_time_base, served_base, unserved_base, utilization_base = simulate_base_case(num_windows, num_customers, total_time, work_units)
print(f"Average waiting time: {avg_waiting_time_base:.2f} minutes")
print(f"Customers served: {served_base}, Customers not served: {unserved_base}")
print(f"Window utilization rate: {utilization_base:.2f}%")

print("\nPriority Queue Case (10 windows, light requests prioritized):")
avg_waiting_time_priority, served_priority, unserved_priority, utilization_priority = simulate_priority_case(num_windows, num_customers, total_time, work_units)
print(f"Average waiting time: {avg_waiting_time_priority:.2f} minutes")
print(f"Customers served: {served_priority}, Customers not served: {unserved_priority}")
print(f"Window utilization rate: {utilization_priority:.2f}%")

print("\nExtra Window Case (11 windows, no priority queue):")
avg_waiting_time_extra, served_extra, unserved_extra, utilization_extra = simulate_base_case(11, num_customers, total_time, work_units)
print(f"Average waiting time: {avg_waiting_time_extra:.2f} minutes")
print(f"Customers served: {served_extra}, Customers not served: {unserved_extra}")
print(f"Window utilization rate: {utilization_extra:.2f}%")

print("\nFewer Window Case (9 windows, no priority queue):")
avg_waiting_time_fewer, served_fewer, unserved_fewer, utilization_fewer = simulate_base_case(9, num_customers, total_time, work_units)
print(f"Average waiting time: {avg_waiting_time_fewer:.2f} minutes")
print(f"Customers served: {served_fewer}, Customers not served: {unserved_fewer}")
print(f"Window utilization rate: {utilization_fewer:.2f}%")

print("\nNon-Uniform Case (10 windows, FIFO):")
avg_waiting_time_non_uniform, served_non_uniform, unserved_non_uniform, utilization_non_uniform = simulate_base_case(num_windows, num_customers, total_time, non_normal_work_units)
print(f"Average waiting time: {avg_waiting_time_non_uniform:.2f} minutes")
print(f"Customers served: {served_non_uniform}, Customers not served: {unserved_non_uniform}")
print(f"Window utilization rate: {utilization_non_uniform:.2f}%")
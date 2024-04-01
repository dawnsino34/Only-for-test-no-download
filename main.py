import subprocess
import time
import csv
import matplotlib.pyplot as plt
from serial_crawler import serial_crawler
from parallel_crawler import parallel_crawler

test_sizes = [2,3,4]
thread_process_counts = [2, 4, 8]
runs_per_combination = 2z

results = []

for test_size in test_sizes:
    for count in thread_process_counts:
        serial_times = []
        parallel_times = []
        distributed_times = []

        for _ in range(runs_per_combination):
            # Run serial crawler
            print(f"Running serial crawler with test size {test_size}...")
            start = time.time()
            serial_crawler(test_size)
            end = time.time()
            serial_times.append(end - start)
            print(f"Serial crawler completed in {end - start} seconds.")

            # Run parallel crawler
            print(f"Running parallel crawler with test size {test_size} and {count} threads...")
            start = time.time()
            parallel_crawler(count, test_size)
            end = time.time()
            parallel_times.append(end - start)
            print(f"Parallel crawler completed in {end - start} seconds.")

            # Run distributed crawler
            print(f"Running distributed crawler with test size {test_size} and {count} processes...")
            start = time.time()
            subprocess.run(["mpiexec", "-n", str(count), "python", "distributed_crawler.py", str(test_size)])
            end = time.time()
            distributed_times.append(end - start)
            print(f"Distributed crawler completed in {end - start} seconds.")

        serial_time_avg = sum(serial_times) / runs_per_combination
        parallel_time_avg = sum(parallel_times) / runs_per_combination
        distributed_time_avg = sum(distributed_times) / runs_per_combination

        results.append([test_size, count, serial_time_avg, parallel_time_avg, distributed_time_avg])

# Write results to a CSV file
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Test Size", "Thread/Process Count", "Serial Time", "Parallel Time", "Distributed Time"])
    writer.writerows(results)

# Generate a plot
plt.figure(figsize=(10, 6))
for i, label in enumerate(["Serial Time", "Parallel Time", "Distributed Time"]):
    plt.plot([x[0] for x in results], [x[i+2] for x in results], label=label)
plt.xlabel('Test Size')
plt.ylabel('Time (seconds)')
plt.legend
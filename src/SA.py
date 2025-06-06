import json
import random
import time
import math
import sys


def calculate_total_distance(route, distance_matrix):
    return sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


def simulated_annealing(route, distance_matrix, initial_temp=1000, cooling_rate=0.999, max_iter=2000, min_temp=1e-4):
    depot = route[0]
    path = route[1:-1]
    current_route = path[:]
    current_distance = calculate_total_distance([depot] + current_route + [depot], distance_matrix)
    best_route = current_route[:]
    best_distance = current_distance

    T = initial_temp

    def two_opt_swap(r, i, j):
        return r[:i] + r[i:j+1][::-1] + r[j+1:]

    for _ in range(max_iter):
        i, j = sorted(random.sample(range(len(current_route)), 2))
        new_route = two_opt_swap(current_route, i, j)
        new_distance = calculate_total_distance([depot] + new_route + [depot], distance_matrix)

        delta = new_distance - current_distance
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_route = new_route
            current_distance = new_distance

            if current_distance < best_distance:
                best_route = current_route[:]
                best_distance = current_distance

        T *= cooling_rate
        if T < min_temp:
            break

    return [depot] + best_route + [depot], best_distance


def main(output_path, input_json_file, refined_output_path, time_path):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    distance = data['distance']

    with open(output_path, 'r') as f:
        lines = f.readlines()
        original_route = list(map(int, lines[1].strip().split()))

    original_route = [0] + original_route + [0]

    start_time = time.time()
    improved_route, _ = simulated_annealing(original_route, distance)
    runtime = time.time() - start_time

    with open(refined_output_path, "w") as f_out:
        f_out.write(f"{len(improved_route) - 2}\n")
        f_out.write(" ".join(map(str, improved_route[1:-1])) + "\n")

    with open(time_path, "w") as f_time:
        f_time.write(f"{runtime:.6f} seconds (metaheuristic: SA)\n")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python3 scripts/SA.py <original_output> <input_json> <refined_output> <refined_time>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
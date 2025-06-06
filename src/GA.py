import json
import random
import time
import sys


def calculate_total_distance(route, distance_matrix):
    return sum(
        distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1)
    )


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]

    fill_values = [gene for gene in parent2 if gene not in child]
    idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = fill_values[idx]
            idx += 1
    return child


def mutate(route, mutation_rate=0.2):
    if random.random() < mutation_rate:
        a, b = sorted(random.sample(range(len(route)), 2))
        route[a], route[b] = route[b], route[a]


def genetic_algorithm(route, distance_matrix, generations=300, population_size=50):
    depot = route[0]
    path = route[1:-1]  # exclude depot

    # Initialize population with Greedy route first
    population = [path] + [random.sample(path, len(path)) for _ in range(population_size - 1)]
    population = [[depot] + individual + [depot] for individual in population]

    best_route = min(population, key=lambda r: calculate_total_distance(r, distance_matrix))
    best_distance = calculate_total_distance(best_route, distance_matrix)

    for _ in range(generations):
        new_population = []
        for _ in range(population_size):
            p1, p2 = random.sample(population, 2)
            child_path = crossover(p1[1:-1], p2[1:-1])
            mutate(child_path, mutation_rate=0.2)
            child = [depot] + child_path + [depot]
            new_population.append(child)

        # Elitism: keep the best from previous generation
        population = [best_route] + sorted(new_population, key=lambda r: calculate_total_distance(r, distance_matrix))[:population_size - 1]

        current_best = population[0]
        current_distance = calculate_total_distance(current_best, distance_matrix)
        if current_distance < best_distance:
            best_route = current_best
            best_distance = current_distance

    return best_route, best_distance


def main(output_path, input_json_file, refined_output_path, time_path):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    distance = data['distance']

    with open(output_path, 'r') as f:
        lines = f.readlines()
        original_route = list(map(int, lines[1].strip().split()))

    original_route = [0] + original_route + [0]

    start_time = time.time()
    improved_route, _ = genetic_algorithm(original_route, distance)
    runtime = time.time() - start_time

    with open(refined_output_path, "w") as f_out:
        f_out.write(f"{len(improved_route) - 2}\n")
        f_out.write(" ".join(map(str, improved_route[1:-1])) + "\n")

    with open(time_path, "w") as f_time:
        f_time.write(f"{runtime:.6f} seconds (metaheuristic: GA)\n")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python3 scripts/GA.py <original_output> <input_json> <refined_output> <refined_time>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
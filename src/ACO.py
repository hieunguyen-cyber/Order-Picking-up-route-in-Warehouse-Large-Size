import json
import random
import time
import sys


def calculate_total_distance(route, distance_matrix):
    return sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


def ant_colony_optimization(route, distance_matrix, n_ants=30, n_iterations=100, alpha=1.0, beta=5.0, evaporation=0.5, Q=100, elitist_weight=2.0):
    depot = route[0]
    path = route[1:-1]  # exclude depot
    n = len(path)

    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]
    distances = [[distance_matrix[path[i]][path[j]] for j in range(n)] for i in range(n)]
    epsilon = 1e-6  # avoid division by zero

    best_path = None
    best_distance = float('inf')

    for iteration in range(n_iterations):
        all_routes = []
        all_distances = []

        for _ in range(n_ants):
            unvisited = set(range(n))
            current = random.choice(list(unvisited))
            route_indices = [current]
            unvisited.remove(current)

            while unvisited:
                probs = []
                denom = 0.0
                for j in unvisited:
                    tau = pheromone[current][j] ** alpha
                    eta = (1.0 / max(distances[current][j], epsilon)) ** beta
                    prob = tau * eta
                    probs.append((j, prob))
                    denom += prob

                r = random.uniform(0, denom)
                cumulative = 0.0
                for j, p in probs:
                    cumulative += p
                    if cumulative >= r:
                        next_node = j
                        break

                route_indices.append(next_node)
                unvisited.remove(next_node)
                current = next_node

            full_route = [depot] + [path[i] for i in route_indices] + [depot]
            total_dist = calculate_total_distance(full_route, distance_matrix)
            all_routes.append(route_indices)
            all_distances.append(total_dist)

            if total_dist < best_distance:
                best_distance = total_dist
                best_path = route_indices

        # Evaporate
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - evaporation)

        # Deposit pheromone from all ants
        for k in range(n_ants):
            contribution = Q / max(all_distances[k], epsilon)
            r = all_routes[k]
            for i in range(n - 1):
                pheromone[r[i]][r[i + 1]] += contribution

        # Elitist strategy: reinforce best path
        if best_path:
            contribution = elitist_weight * Q / max(best_distance, epsilon)
            for i in range(n - 1):
                pheromone[best_path[i]][best_path[i + 1]] += contribution

    improved_route = [depot] + [path[i] for i in best_path] + [depot]
    return improved_route, best_distance


def main(output_path, input_json_file, refined_output_path, time_path):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    distance = data['distance']

    with open(output_path, 'r') as f:
        lines = f.readlines()
        original_route = list(map(int, lines[1].strip().split()))

    original_route = [0] + original_route + [0]

    start_time = time.time()
    improved_route, _ = ant_colony_optimization(original_route, distance)
    runtime = time.time() - start_time

    with open(refined_output_path, "w") as f_out:
        f_out.write(f"{len(improved_route) - 2}\n")
        f_out.write(" ".join(map(str, improved_route[1:-1])) + "\n")

    with open(time_path, "w") as f_time:
        f_time.write(f"{runtime:.6f} seconds (metaheuristic: ACO)\n")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python3 scripts/ACO.py <original_output> <input_json> <refined_output> <refined_time>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
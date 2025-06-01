import random
import math
import json
from typing import List, Tuple
import numpy as np
import fire
from ortools.linear_solver import pywraplp


def euclidean(p1: Tuple[float, float], p2: Tuple[float, float]) -> int:
    return round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]))


def solve_with_ortools(N, M, Q, D, q):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        raise RuntimeError("SCIP solver not available")

    x = [solver.BoolVar(f'x_{j}') for j in range(M)]
    r = [[solver.IntVar(0, Q[i][j], f'r_{i}_{j}') for j in range(M)] for i in range(N)]

    for i in range(N):
        solver.Add(sum(r[i][j] for j in range(M)) >= q[i])
    for j in range(M):
        for i in range(N):
            solver.Add(r[i][j] <= Q[i][j] * x[j])

    total_distance = solver.Sum([x[j] * (D[0][j + 1] + D[j + 1][0]) for j in range(M)])
    solver.Minimize(total_distance)

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError(f"Solver failed with status: {status}")

    visited = [j + 1 for j in range(M) if x[j].solution_value() > 0.5]
    return visited


def greedy_selection(N, M, Q, D, q):
    selected = set()
    remaining = q[:]
    product_to_shelves = [[] for _ in range(N)]

    for i in range(N):
        for j in range(M):
            if Q[i][j] > 0:
                dist = D[0][j + 1] + D[j + 1][0]
                product_to_shelves[i].append((dist, j))

    for i in range(N):
        product_to_shelves[i].sort()
        for _, j in product_to_shelves[i]:
            if remaining[i] <= 0:
                break
            take = min(Q[i][j], remaining[i])
            remaining[i] -= take
            selected.add(j)

    return [j + 1 for j in selected]


def generate_test_case(
    N: int,
    M: int,
    max_quantity: int = 10,
    num_visited: int = None,
    seed: int = None,
    sparsity: float = 0.4,
    spread_factor: float = 2.0,
    use_solver: bool = False,
    use_greedy: bool = True
) -> None:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Generate Q: Quantity of product i available on shelf j
    Q = np.zeros((N, M), dtype=int)
    for i in range(N):
        idx = np.random.choice(M, size=max(1, int(sparsity * M)), replace=False)
        Q[i, idx] = np.random.randint(1, max_quantity + 1, size=len(idx))
    Q_list = Q.tolist()

    # Generate D: Distance matrix using NumPy for speed
    positions = np.random.uniform(0, 100, size=(M + 1, 2))
    D = np.round(np.linalg.norm(positions[:, None, :] - positions[None, :, :], axis=2)).astype(int).tolist()

    # Generate q: Demand per product
    total_supply = Q.sum(axis=1)
    q = [0 if total == 0 else random.randint(max(1, int(total // spread_factor)), total) for total in total_supply]

    # Solve to get visited shelves
    if use_solver:
        visited = solve_with_ortools(N, M, Q_list, D, q)
    elif use_greedy:
        visited = greedy_selection(N, M, Q_list, D, q)
    else:
        visited = []

    if num_visited is not None:
        visited = visited[:num_visited]

    result = {
        "input": {
            "N": N,
            "M": M,
            "Q": Q_list,
            "D": D,
            "q": q
        },
        "expected_output": {
            "d": len(visited),
            "m": visited
        }
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    fire.Fire({"generate_test_case": generate_test_case})
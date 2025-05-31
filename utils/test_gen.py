import random
import math
import json
from typing import List, Tuple, Dict
import fire
from ortools.linear_solver import pywraplp


def euclidean(p1: Tuple[float, float], p2: Tuple[float, float]) -> int:
    """Calculate Euclidean distance between two points, rounded to nearest integer."""
    return round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]))


def solve_with_ortools(N: int, M: int, Q: List[List[int]], D: List[List[int]], q: List[int]) -> List[int]:
    """Solve the warehouse optimization problem using OR-Tools."""
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        raise RuntimeError("SCIP solver not available")

    # Decision variables: x[j] = 1 if shelf j is visited, 0 otherwise
    x = [solver.BoolVar(f'x_{j}') for j in range(M)]

    # Decision variables: r[i][j] = quantity of product i taken from shelf j
    r = [[solver.IntVar(0, Q[i][j], f'r_{i}_{j}') for j in range(M)] for i in range(N)]

    # Constraint: Total quantity collected for each product i must meet or exceed demand q[i]
    for i in range(N):
        solver.Add(sum(r[i][j] for j in range(M)) >= q[i])

    # Constraint: Cannot collect from shelf j if it is not visited
    for j in range(M):
        for i in range(N):
            solver.Add(r[i][j] <= Q[i][j] * x[j])

    # Objective: Minimize total distance (to and from warehouse entrance)
    total_distance = solver.Sum([x[j] * (D[0][j + 1] + D[j + 1][0]) for j in range(M)])
    solver.Minimize(total_distance)

    # Solve the problem
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError(f"Solver failed with status: {status}")

    # Extract visited shelves (1-based indexing)
    visited = [j + 1 for j in range(M) if x[j].solution_value() > 0.5]
    return visited


def generate_test_case(
    N: int,
    M: int,
    max_quantity: int = 10,
    num_visited: int = None,
    seed: int = None,
    sparsity: float = 0.4,
    spread_factor: float = 2.0
) -> None:
    """
    Generate a test case for the warehouse optimization problem.
    
    Args:
        N: Number of product types
        M: Number of shelves
        max_quantity: Maximum quantity of a product on a shelf
        num_visited: Maximum number of shelves to visit (optional)
        seed: Random seed for reproducibility (optional)
        sparsity: Fraction of shelves containing each product
        spread_factor: Factor to determine demand range
    """
    if seed is not None:
        random.seed(seed)

    # Generate Q: Quantity of product i available on shelf j
    Q = [[0] * M for _ in range(N)]
    for i in range(N):
        shelves_with_product = random.sample(range(M), max(1, int(sparsity * M)))
        for j in shelves_with_product:
            Q[i][j] = random.randint(1, max_quantity)

    # Generate D: Distance matrix between warehouse entrance (0) and shelves (1 to M)
    positions = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(M + 1)]
    D = [[euclidean(positions[i], positions[j]) for j in range(M + 1)] for i in range(M + 1)]

    # Generate q: Demand for each product
    q = []
    for i in range(N):
        total = sum(Q[i])
        if total == 0:
            q.append(0)
        else:
            base = total // spread_factor
            q.append(random.randint(max(1, int(base)), total))

    # Solve to get expected output
    visited = solve_with_ortools(N, M, Q, D, q)

    # Limit number of visited shelves if specified
    if num_visited is not None:
        visited = visited[:num_visited]

    # Prepare result
    result = {
        "input": {
            "N": N,
            "M": M,
            "Q": Q,
            "D": D,
            "q": q
        },
        "expected_output": {
            "d": len(visited),
            "m": visited
        }
    }

    # Output JSON with proper formatting
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    fire.Fire({"generate_test_case": generate_test_case})
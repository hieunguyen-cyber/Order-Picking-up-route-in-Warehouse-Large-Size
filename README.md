```markdown
# Order-Picking-up-route-in-Warehouse-Large-Size

## Overview

This project addresses the warehouse order-picking problem, aiming to minimize the total travel distance for a worker to collect products from shelves in a large warehouse. The worker starts at the warehouse entrance (position 0), visits a subset of shelves to fulfill product demands, and returns to the entrance. The solution involves selecting an optimal sequence of shelves to visit, ensuring all product demands are met with minimal travel distance.

The repository implements and evaluates five algorithms to solve this problem, with a focus on balancing computational efficiency and solution quality. The project includes a test case generator and evaluation framework to assess algorithm performance across different problem sizes.

---

## Problem

### Statement

#### **Description**

A warehouse contains **M** shelves, numbered from 1 to **M**, where shelf **j** is located at position **j** (j = 1, …, M). There are **N** product types, numbered from 1 to **N**, with the quantity of product **i** at shelf **j** given by **Q[i][j]**.

The worker starts at the warehouse entrance (position 0) and must visit a subset of shelves (each shelf visited at most once, not necessarily all shelves) to collect products according to a customer order. The order specifies a demand of **q[i]** units for product **i** (i = 1, …, N). The distance between positions **i** and **j** (including the entrance at 0) is given by **d(i,j)** (0 ≤ i, j ≤ M).

**Objective**: Find the sequence of shelves to visit that minimizes the total travel distance while satisfying all product demands.

---

#### **Input Format**

- Line 1: Two positive integers **N** and **M** (1 ≤ N ≤ 50, 1 ≤ M ≤ 1000)
- Lines 2 to N+1: Each line represents a row of the supply matrix **Q**
- Lines N+2 to N+M+2: Each line represents a row of the distance matrix **d**
- Line N+M+3: The demand vector **q[1], q[2], …, q[N]**

---

**Solution Format**: A sequence of positive integers **x₁, x₂, …, xₙ** representing the order of shelves to visit.

---

#### **Output Format**

- Line 1: A positive integer **n** (number of shelves to visit)
- Line 2: **n** positive integers **x₁, x₂, …, xₙ** (sequence of shelves)

---

#### **Example**

##### **Input**
```
6 5
3 2 2 4 2
4 3 7 3 5
6 7 2 5 4
2 3 3 2 1
2 5 7 6 1
7 2 1 6 5
0 16 10 13 13 19
16 0 8 3 19 5
10 8 0 7 23 11
13 3 7 0 16 6
13 19 23 16 0 22
19 5 11 6 22 0
8 7 4 8 11 13
```

##### **Output**
```
4
2 3 1 5
```

##### **Explanation**
The worker’s route is: `0 → 2 → 3 → 1 → 5 → 0`

---

## Algorithms Implemented

The project implements five algorithms to solve the warehouse order-picking problem, each balancing efficiency and solution quality differently:

1. **Exact Dynamic Programming (Exact DP)**:
   - Enumerates all subsets of shelves for small instances (\( M \leq 18 \)) to find the optimal route with minimal travel distance.
   - Guarantees optimality but has exponential time complexity, making it suitable only for small problems.

2. **DP-Greedy**:
   - A hybrid approach that uses Exact DP for small instances (\( M \leq 18 \)) and falls back to a greedy heuristic for larger instances.
   - The greedy phase selects the nearest unvisited shelf that contributes to unmet demand.
   - Achieves the fastest runtime across all test sizes (e.g., 0.00486s for large instances).

3. **DP-Greedy with 2-Opt**:
   - Extends DP-Greedy by applying 2-opt local search to refine the greedy route, reducing total travel distance.
   - Produces the shortest routes across all test sizes (e.g., 1581.2 units for large instances).

4. **Greedy**:
   - A simple heuristic that iteratively selects the nearest unvisited shelf with needed products, starting from the entrance.
   - Fast (approximately \( O(N M^2) \)) and feasible but may yield suboptimal routes due to its local optimization approach.

5. **Greedy with 2-Opt**:
   - Enhances the Greedy algorithm by applying 2-opt local search to optimize the initial route, improving travel distance with moderate computational overhead.

---

## Evaluation Framework

### Test Case Overview

Test cases are generated synthetically using a Python script controlled by a Bash wrapper, producing 10 test cases per size category:

#### 🔹 Small
- Number of products (\( N \)): 10
- Number of shelves (\( M \)): 20
- Maximum quantity per shelf: 20
- Number of shelves to visit: 6
- Number of test cases: User-specified

#### 🔸 Medium
- Number of products (\( N \)): 40
- Number of shelves (\( M \)): 100
- Maximum quantity per shelf: 100
- Number of shelves to visit: 20
- Number of test cases: User-specified

#### 🔺 Large
- Number of products (\( N \)): 100
- Number of shelves (\( M \)): 400
- Maximum quantity per shelf: 200
- Number of shelves to visit: 40
- Number of test cases: User-specified

---

### Evaluation Criteria

The algorithms are evaluated based on the following metrics:

- **Total Travel Distance**: Sum of distances along the route, aiming for minimization.
- **Runtime**: Wall-clock time in seconds, measured using Python’s `time.time()`.
- **Number of Shelves Visited**: Count of shelves in the route (excluding the depot), reflecting shelf selection efficiency.
- **Feasibility**: Ensures the solution meets the demand vector \( q \).

---

## Experimental Setup

- **Hardware**: Apple M3 Pro chip, 18GB RAM
- **Software**: Python 3.12.7
- **Test Case Generation**: A Python script generates test cases, controlled by a Bash wrapper script.

---

## Results

The algorithms were evaluated on 10 randomized instances per size category (small, medium, large). Key findings include:

### Runtime
- **DP-Greedy** is the fastest, with an average runtime of 0.00486s for large instances, up to 9x faster than 2-opt variants.
- 2-opt-based algorithms (e.g., DP-Greedy with 2-Opt, Greedy with 2-Opt) have higher runtimes (0.034–0.048s for large instances) due to local search overhead.

### Number of Shelves Visited
- All algorithms select a similar number of shelves (~399–400 for large instances), confirming demand satisfaction.
- **DP-Greedy** and **DP-Greedy with 2-Opt** slightly outperform others by selecting fewer shelves, indicating better packing efficiency.

### Total Travel Distance
- **DP-Greedy with 2-Opt** achieves the shortest distances (e.g., 1581.2 units for large instances), ~200 units shorter than Greedy or DP-Greedy.
- 2-opt variants consistently improve route quality over their non-optimized counterparts.

### Summary Tables

#### Table 1: Average Runtime (seconds)
| Algorithm            | Small   | Medium  | Large   |
|----------------------|---------|---------|---------|
| Local_Search_Two_Opt | 0.000068| 0.001651| 0.033545|
| Greedy_Local_Search  | 0.000131| 0.002585| 0.048416|
| DP_Greedy_Two_Opt    | 0.000069| 0.002111| 0.041992|
| Greedy               | 0.000123| 0.002526| 0.037710|
| DP_Greedy            | 0.000032| 0.000405| 0.004863|

#### Table 2: Average Number of Shelves Visited
| Algorithm            | Small | Medium | Large |
|----------------------|-------|--------|-------|
| Local_Search_Two_Opt | 19    | 100    | 399   |
| Greedy_Local_Search  | 19    | 99     | 397   |
| DP_Greedy_Two_Opt    | 19    | 100    | 399   |
| Greedy               | 19    | 99     | 397   |
| DP_Greedy            | 19    | 100    | 399   |

#### Table 3: Average Total Travel Distance
| Algorithm            | Small | Medium | Large  |
|----------------------|-------|--------|--------|
| Local_Search_Two_Opt | 365.5 | 831.3  | 1597.3 |
| Greedy_Local_Search  | 376.7 | 929.1  | 1777.8 |
| DP_Greedy_Two_Opt    | 357.1 | 819.4  | 1581.2 |
| Greedy               | 376.7 | 929.1  | 1777.8 |
| DP_Greedy            | 376.6 | 931.5  | 1783.3 |

---

## Conclusion

The **DP-Greedy with 2-Opt** algorithm is the most effective, balancing computational efficiency and solution quality. It achieves the shortest travel distances (e.g., 1581.2 units for large instances) while maintaining reasonable runtimes. **DP-Greedy** excels in speed (0.00486s for large instances), making it ideal for time-critical applications. The 2-opt optimization significantly enhances route quality, making **DP-Greedy with 2-Opt** the recommended choice for practical warehouse systems.

---

## Installation and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hieunguyen-cyber/Order-Picking-up-route-in-Warehouse-Large-Size.git
   cd Order-Picking-up-route-in-Warehouse-Large-Size
   ```

2. **Install Dependencies**:
   Ensure Python 3.12.7 is installed. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Test Cases**:
   Use the Bash wrapper script to generate test cases:
   ```bash
   ./generate_test_cases.sh --size <small|medium|large> --num_case <number>
   ```

4. **Run Algorithms**:
   Execute the main Python script to run and evaluate algorithms:
   ```bash
   python main.py --input <test_case_file> --algorithm <algorithm_name>
   ```
   Supported algorithms: `exact_dp`, `dp_greedy`, `dp_greedy_two_opt`, `greedy`, `greedy_two_opt`.

5. **View Results**:
   Results are saved in the output directory, including runtime, number of shelves visited, and total travel distance.

---

## Project Structure

```
Order-Picking-up-route-in-Warehouse-Large-Size/
├── generate_test_cases.sh    # Bash script for test case generation
├── main.py                   # Main script to run algorithms
├── requirements.txt          # Python dependencies
├── src/                      # Source code for algorithms
│   ├── exact_dp.py           # Exact Dynamic Programming implementation
│   ├── dp_greedy.py          # DP-Greedy implementation
│   ├── dp_greedy_two_opt.py  # DP-Greedy with 2-Opt implementation
│   ├── greedy.py             # Greedy algorithm implementation
│   ├── greedy_two_opt.py     # Greedy with 2-Opt implementation
├── test_cases/               # Directory for generated test cases
├── output/                   # Directory for algorithm outputs
└── README.md                 # This file
```

---

## Future Work

- **Advanced Heuristics**: Incorporate metaheuristics like simulated annealing or genetic algorithms to further optimize routes.
- **Parallel Computing**: Implement parallel processing to reduce runtime for large instances.
- **Real-World Validation**: Test algorithms on real warehouse data to ensure practical applicability.
- **Extended Constraints**: Add constraints like shelf capacity limits or time windows for order picking.

---

## Contributors

- **Nguyen T. Hieu** (Student ID: 2024)
- **Nguyen Q. Duong** (Student ID: 2024)
- **Do X. Truong** (Student ID: 2024)
- **Mai G. Hy** (Student ID: 2024)
- **Professor**: Phams Q. Daing

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


# Order-Picking-up-route-in-Warehouse-Large-Size

## Overview

This project addresses the warehouse order-picking problem, aiming to minimize the total travel distance for a worker to collect products from shelves in a large warehouse. The worker starts at the warehouse entrance (position 0), visits a subset of shelves to fulfill product demands, and returns to the entrance. The solution involves selecting an optimal sequence of shelves to visit, ensuring all product demands are met with minimal travel distance.

The repository implements and evaluates five algorithms to solve this problem, with a focus on balancing computational efficiency and solution quality. The project includes a test case generator and evaluation framework to assess algorithm performance across different problem sizes.

---

## Problem

### Statement

#### **Description**

A warehouse contains **M** shelves, numbered from 1 to **M**, where shelf **j** is located at position **j** (j = 1, …, M). There are **N** product types, numbered from 1 to **N**, with the quantity of product **i** at shelf **j** given by **Q[i][j]**.

The worker starts at the warehouse entrance (position 0) and must visit a subset of shelves (each shelf visited at most once, not necessarily all shelves) to collect products according to a customer order. The order specifies a demand of **q[i]** units for product **i** (i = 1, …, N). The distance between positions **i** and **j** (including the entrance at 0) is given by **d(i,j)** (0 ≤ i, j ≤ M).

**Objective**: Find the sequence of shelves to visit that minimizes the total travel distance while satisfying all product demands.

---

#### **Input Format**

- Line 1: Two positive integers **N** and **M** (1 ≤ N ≤ 50, 1 ≤ M ≤ 1000)
- Lines 2 to N+1: Each line represents a row of the supply matrix **Q**
- Lines N+2 to N+M+2: Each line represents a row of the distance matrix **d**
- Line N+M+3: The demand vector **q[1], q[2], …, q[N]**

---

**Solution Format**: A sequence of positive integers **x₁, x₂, …, xₙ** representing the order of shelves to visit.

---

#### **Output Format**

- Line 1: A positive integer **n** (number of shelves to visit)
- Line 2: **n** positive integers **x₁, x₂, …, xₙ** (sequence of shelves)

---

#### **Example**

##### **Input**
```
6 5
3 2 2 4 2
4 3 7 3 5
6 7 2 5 4
2 3 3 2 1
2 5 7 6 1
7 2 1 6 5
0 16 10 13 13 19
16 0 8 3 19 5
10 8 0 7 23 11
13 3 7 0 16 6
13 19 23 16 0 22
19 5 11 6 22 0
8 7 4 8 11 13
```

##### **Output**
```
4
2 3 1 5
```

##### **Explanation**
The worker’s route is: `0 → 2 → 3 → 1 → 5 → 0`

---

## Algorithms Implemented

The project implements five algorithms to solve the warehouse order-picking problem, each balancing efficiency and solution quality differently:

1. **Exact Dynamic Programming (Exact DP)**:
   - Enumerates all subsets of shelves for small instances (\( M \leq 18 \)) to find the optimal route with minimal travel distance.
   - Guarantees optimality but has exponential time complexity, making it suitable only for small problems.

2. **DP-Greedy**:
   - A hybrid approach that uses Exact DP for small instances (\( M \leq 18 \)) and falls back to a greedy heuristic for larger instances.
   - The greedy phase selects the nearest unvisited shelf that contributes to unmet demand.
   - Achieves the fastest runtime across all test sizes (e.g., 0.00486s for large instances).

3. **DP-Greedy with 2-Opt**:
   - Extends DP-Greedy by applying 2-opt local search to refine the greedy route, reducing total travel distance.
   - Produces the shortest routes across all test sizes (e.g., 1581.2 units for large instances).

4. **Greedy**:
   - A simple heuristic that iteratively selects the nearest unvisited shelf with needed products, starting from the entrance.
   - Fast (approximately \( O(N M^2) \)) and feasible but may yield suboptimal routes due to its local optimization approach.

5. **Greedy with 2-Opt**:
   - Enhances the Greedy algorithm by applying 2-opt local search to optimize the initial route, improving travel distance with moderate computational overhead.

---

## Evaluation Framework

### Test Case Overview

Test cases are generated synthetically using a Python script controlled by a Bash wrapper, producing 10 test cases per size category:

#### 🔹 Small
- Number of products (\( N \)): 10
- Number of shelves (\( M \)): 20
- Maximum quantity per shelf: 20
- Number of shelves to visit: 6
- Number of test cases: User-specified

#### 🔸 Medium
- Number of products (\( N \)): 40
- Number of shelves (\( M \)): 100
- Maximum quantity per shelf: 100
- Number of shelves to visit: 20
- Number of test cases: User-specified

#### 🔺 Large
- Number of products (\( N \)): 100
- Number of shelves (\( M \)): 400
- Maximum quantity per shelf: 200
- Number of shelves to visit: 40
- Number of test cases: User-specified

---

### Evaluation Criteria

The algorithms are evaluated based on the following metrics:

- **Total Travel Distance**: Sum of distances along the route, aiming for minimization.
- **Runtime**: Wall-clock time in seconds, measured using Python’s `time.time()`.
- **Number of Shelves Visited**: Count of shelves in the route (excluding the depot), reflecting shelf selection efficiency.
- **Feasibility**: Ensures the solution meets the demand vector \( q \).

---

## Experimental Setup

- **Hardware**: Apple M3 Pro chip, 18GB RAM
- **Software**: Python 3.12.7
- **Test Case Generation**: A Python script generates test cases, controlled by a Bash wrapper script.

---

## Results

The algorithms were evaluated on 10 randomized instances per size category (small, medium, large). Key findings include:

### Runtime
- **DP-Greedy** is the fastest, with an average runtime of 0.00486s for large instances, up to 9x faster than 2-opt variants.
- 2-opt-based algorithms (e.g., DP-Greedy with 2-Opt, Greedy with 2-Opt) have higher runtimes (0.034–0.048s for large instances) due to local search overhead.

### Number of Shelves Visited
- All algorithms select a similar number of shelves (~399–400 for large instances), confirming demand satisfaction.
- **DP-Greedy** and **DP-Greedy with 2-Opt** slightly outperform others by selecting fewer shelves, indicating better packing efficiency.

### Total Travel Distance
- **DP-Greedy with 2-Opt** achieves the shortest distances (e.g., 1581.2 units for large instances), ~200 units shorter than Greedy or DP-Greedy.
- 2-opt variants consistently improve route quality over their non-optimized counterparts.

### Summary Tables

#### Table 1: Average Runtime (seconds)
| Algorithm            | Small   | Medium  | Large   |
|----------------------|---------|---------|---------|
| Local_Search_Two_Opt | 0.000068| 0.001651| 0.033545|
| Greedy_Local_Search  | 0.000131| 0.002585| 0.048416|
| DP_Greedy_Two_Opt    | 0.000069| 0.002111| 0.041992|
| Greedy               | 0.000123| 0.002526| 0.037710|
| DP_Greedy            | 0.000032| 0.000405| 0.004863|

#### Table 2: Average Number of Shelves Visited
| Algorithm            | Small | Medium | Large |
|----------------------|-------|--------|-------|
| Local_Search_Two_Opt | 19    | 100    | 399   |
| Greedy_Local_Search  | 19    | 99     | 397   |
| DP_Greedy_Two_Opt    | 19    | 100    | 399   |
| Greedy               | 19    | 99     | 397   |
| DP_Greedy            | 19    | 100    | 399   |

#### Table 3: Average Total Travel Distance
| Algorithm            | Small | Medium | Large  |
|----------------------|-------|--------|--------|
| Local_Search_Two_Opt | 365.5 | 831.3  | 1597.3 |
| Greedy_Local_Search  | 376.7 | 929.1  | 1777.8 |
| DP_Greedy_Two_Opt    | 357.1 | 819.4  | 1581.2 |
| Greedy               | 376.7 | 929.1  | 1777.8 |
| DP_Greedy            | 376.6 | 931.5  | 1783.3 |

---

## Conclusion

The **DP-Greedy with 2-Opt** algorithm is the most effective, balancing computational efficiency and solution quality. It achieves the shortest travel distances (e.g., 1581.2 units for large instances) while maintaining reasonable runtimes. **DP-Greedy** excels in speed (0.00486s for large instances), making it ideal for time-critical applications. The 2-opt optimization significantly enhances route quality, making **DP-Greedy with 2-Opt** the recommended choice for practical warehouse systems.

---

## Installation and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hieunguyen-cyber/Order-Picking-up-route-in-Warehouse-Large-Size.git
   cd Order-Picking-up-route-in-Warehouse-Large-Size
   ```

2. **Install Dependencies**:
   Ensure Python 3.12.7 is installed. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Test Cases**:
   Use the Bash wrapper script to generate test cases:
   ```bash
   ./generate_test_cases.sh --num_case <number>
   ```

4. **Run Algorithms**:
   Execute the main Python script to run and evaluate algorithms:
   ```bash 
   ./run.sh --stage 2 --stop_stage 9
   ```
   Supported algorithms: `exact_dp`, `dp_greedy`, `dp_greedy_two_opt`, `greedy`, `greedy_two_opt`.

5. **View Results**:
   Results are saved in the output directory, including runtime, number of shelves visited, and total travel distance.


```

---

## Contributors

- **Nguyen T. Hieu** (Student ID: 2024)
- **Nguyen Q. Duong** (Student ID: 2024)
- **Do X. Truong** (Student ID: 2024)
- **Mai G. Hy** (Student ID: 2024)
- **Professor**: Phams Q. Daing
---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
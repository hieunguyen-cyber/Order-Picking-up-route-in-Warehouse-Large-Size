# 📦 Optimization Algorithms for Order Picking-up Route in Large-Scale Warehouses

This project explores heuristic and hybrid optimization techniques for solving the **warehouse order picking** problem. The objective is to select shelves and generate a picking route that satisfies product demand while minimizing total travel distance and the number of shelves visited.

---

## 📚 Introduction

In modern supply chains, warehouse order fulfillment plays a crucial role in operational efficiency. One of the core challenges in warehouse logistics is the **shelf selection and routing problem** — deciding which shelves to visit and in what order to collect all items in an order, while minimizing travel cost.

Traditional exact optimization methods (e.g., integer programming) are computationally expensive for large warehouses. To address this, we investigate a range of **heuristic**, **hybrid**, and **metaheuristic** algorithms that balance solution quality and runtime performance.

This project includes:
- A **test case generator** simulating realistic warehouse layouts.
- Multiple **heuristic and hybrid algorithms** for shelf selection and routing.
- **Metaheuristic post-processing** to refine route quality.
- Extensive benchmarking on small, medium, and large-scale warehouse scenarios.

---

## 🚀 How to Use

### ✅ Prerequisites

- **Python 3.12+**
- **Bash shell**
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

### 📂 Project Structure

```bash
├── run.sh                      # Main entry point
├── path.sh                     # Environment variable setup
├── requirements.txt            # Python dependencies
├── LICENSE
├── README.md
├── REPORT.pdf
├── scripts/                    # Bash wrappers for each algorithm
│   ├── generate_testcases.sh
│   ├── Greedy.sh
│   ├── Greedy_Local_Search.sh
│   ├── DP_Greedy.sh
│   ├── DP_Greedy_Two_Opt.sh
│   ├── Local_Search_Two_Opt.sh
│   ├── SA.sh
│   ├── ACO.sh
│   ├── GA.sh
│   └── plot.sh
├── src/                        # Python implementations of algorithms
│   ├── Greedy.py
│   ├── Greedy_Local_Search.py
│   ├── DP_Greedy.py
│   ├── DP_Greedy_Two_Opt.py
│   ├── Local_Search_Two_Opt.py
│   ├── SA.py
│   ├── ACO.py
│   └── GA.py
├── utils/                      # Utilities for plotting, metrics, etc.
│   ├── calc_total_distance.py
│   ├── log_csv.py
│   ├── plot.py
│   ├── read_input.py
│   └── test_gen.py
├── test/                       # Auto-generated output folders
│   ├── input/
│   ├── eval/
│   └── result folders for each method...
```

---

### ▶️ Run All Stages

To run the full pipeline:

```bash
bash run.sh
```

To include metaheuristic post-processing (SA, ACO, GA):

```bash
bash run.sh --meta true
```

---

### 🎯 Run Specific Stages

Use `--stage` and `--stop_stage` to control the pipeline:

```bash
bash run.sh --stage 2 --stop_stage 4
```

| Stage | Description             |
|-------|--------------------------|
| 1     | Generate 10 test cases   |
| 2     | Run Greedy               |
| 3     | Run DP_Greedy            |
| 4     | Run DP_Greedy_Two_Opt    |
| 5     | Run Greedy_Local_Search  |
| 6     | Run Local_Search_Two_Opt |
| 7     | Run metaheuristics (SA, ACO, GA) |
| 8     | Plot metrics and log CSV |

⚠️ Skip stage 1 if you already have `/test/input` data.

---

### 📊 Plot Results Only

```bash
bash run.sh --stage 8 --stop_stage 8
```

This will:
- Plot runtime, shelf count, and travel distance per model
- Log results to CSV via `utils/log_csv.py`

---

## 🧠 Methodology

### 🏗️ Test Case Generation: Greedy Shelf Selection

Greedy selection chooses shelves that satisfy demands with minimal round-trip distance. Time complexity: O(NM log M). Ensures feasible and realistic scenarios.

### 🔍 Heuristic and Hybrid Algorithms

1. **Greedy**
2. **Greedy + 2-Opt**
3. **Greedy Local Search**
4. **Local Search + 2-Opt**
5. **DP-Greedy**
6. **DP-Greedy + 2-Opt**

### 🔁 Metaheuristic Algorithms

We apply metaheuristics to refine the order of shelf visits for any generated route:

1. **Simulated Annealing (SA)** – Probabilistic acceptance of worse solutions using 2-opt, fast and suitable for online use.
2. **Ant Colony Optimization (ACO)** – Probabilistic construction with pheromone guidance, highest quality, longer runtime.
3. **Genetic Algorithm (GA)** – Population-based crossover + mutation, balances speed and quality.

Run automatically if `--meta true`. The number of shelves stays unchanged; only the visit order is optimized.

---

## 🧪 Experiment Setup

### 🖥️ Environment

- Machine: Apple M3 Pro, 18GB RAM
- Language: Python 3.12.7

### 🧾 Data Generation

Synthetic test cases:
| Category | Products (N) | Shelves (M) | Shelf Cap. | Target Shelves |
|----------|--------------|-------------|------------|----------------|
| Small    | 10           | 20          | 20         | 6              |
| Medium   | 40           | 100         | 100        | 20             |
| Large    | 100          | 400         | 200        | 40             |

---

## 📏 Evaluation Metrics

- **Runtime (s)**
- **Total travel distance**
- **Number of shelves visited**
- **Feasibility**

---

## 📊 Results Summary

| Algorithm               | Runtime (L) | Shelves (L) | Distance (L) |
|-------------------------|-------------|-------------|--------------|
| DP-Greedy               | 0.00486s    | 399         | 1783.3       |
| DP-Greedy + 2-Opt       | 0.04199s    | 399         | **1581.2**   |
| Greedy                  | 0.03771s    | 397         | 1777.8       |
| Local Search + 2-Opt    | 0.03354s    | 399         | 1597.3       |

**Metaheuristic Add-on (Large):**

| Metaheuristic | Runtime     | Distance    |
|---------------|-------------|-------------|
| SA            | **0.12s**   | 1710.3      |
| GA            | 16.51s      | **1710.3**  |
| ACO           | 102.62s     | 1713.1      |

---

## ✅ Conclusion

- **DP-Greedy + 2-Opt** is best overall.
- **Metaheuristics** further improve route quality.
- Use **SA** for fast refinement, **ACO/GA** for higher-quality offline optimization.

---

## 📎 Citation and Acknowledgements

Developed as part of IT3052E Project at SOICT.  
Authors: Nguyen T. Hieu, Nguyen Q. Duong, Do X. Truong, Mai G. Hy  
Supervisor: Pham Q. Dung

Project Repository: [GitHub Link](https://github.com/hieunguyen-cyber/Order-Picking-up-route-in-Warehouse-Large-Size)
# 📦 Optimization Algorithms for Order Picking-up Route in Large-Scale Warehouses

This project explores heuristic and hybrid optimization techniques for solving the **warehouse order picking** problem. The objective is to select shelves and generate a picking route that satisfies product demand while minimizing total travel distance and the number of shelves visited.

---

## 📚 Introduction

In modern supply chains, warehouse order fulfillment plays a crucial role in operational efficiency. One of the core challenges in warehouse logistics is the **shelf selection and routing problem** — deciding which shelves to visit and in what order to collect all items in an order, while minimizing travel cost.

Traditional exact optimization methods (e.g., integer programming) are computationally expensive for large warehouses. To address this, we investigate a range of **heuristic** and **hybrid** algorithms that balance solution quality and runtime performance.

This project includes:
- A **test case generator** simulating realistic warehouse layouts.
- Multiple **heuristic algorithms** for shelf selection and routing.
- Extensive benchmarking on small, medium, and large-scale warehouse scenarios.

---

---

## 🚀 How to Use

### ✅ Prerequisites

- **Python 3.12+**
- **Bash shell**
- Install dependencies:
  ```bash
  pip install -r requirements.txt

⸻

### 📂 Project Structure

```python
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
│   ├── Local_Search_Two_opt.sh
│   ├── dist_cal.sh
│   └── plot.sh
├── src/                        # Python implementations of algorithms
│   ├── Greedy.py
│   ├── Greedy_Local_Search.py
│   ├── DP_Greedy.py
│   ├── DP_Greedy_Two_Opt.py
│   └── Local_Search_Two_Opt.py
├── utils/                      # Utilities for plotting, metrics, etc.
│   ├── calc_total_distance.py
│   ├── log_csv.py
│   ├── plot.py
│   ├── read_input.py
│   └── test_gen.py
├── test/                       # Auto-generated output folders
│   ├── input/
│   ├── eval/
│   ├── Greedy/
│   ├── Greedy_Local_Search/
│   ├── DP_Greedy/
│   ├── DP_Greedy_Two_Opt/
│   └── Local_Search_Two_Opt/
```

⸻

▶️ Run All Stages
```bash
bash run.sh
```
This runs:
	1.	Test case generation
	2.	All algorithms
	3.	Metric plotting & CSV export

⸻

🎯 Run Specific Stages

Use ```--stage``` and ```--stop_stage``` to control the pipeline:
```bash
bash run.sh --stage 2 --stop_stage 4
```

|Stage	|Description             |
|-------|------------------------|
|1	    |Generate 10 test cases  |
|2	    |Run Greedy              |
|3	    |Run DP_Greedy           |
|4	    |Run DP_Greedy_Two_Opt   |
|5	    |Run Greedy_Local_Search |
|6	    |Run Local_Search_Two_Opt|
|7	    |Plot metrics and log CSV|

⚠️ Skip stage 1 if you already have /test/input data.

⸻

### 📊 Plot Results Only
```bash
bash run.sh --stage 9 --stop_stage 9
```

This will:
- Plot runtime, shelf count, and travel distance per model
- Log results to CSV via utils/log_csv.py

⸻

## 🧠 Methodology

### 🏗️ Test Case Generation: Greedy Shelf Selection

We designed a greedy algorithm to generate test cases that are feasible and scalable. For each product in demand, it selects shelves offering the product with the **minimum round-trip distance** from the depot. This ensures:
- Feasibility of the instance.
- Realistic layouts reflecting practical warehouse settings.
- Efficient generation with time complexity \( O(NM \log M) \).

### 🔍 Heuristic Algorithms

1. **Greedy**  
   At each step, the algorithm visits the nearest unvisited shelf containing at least one needed product. It is fast and guarantees feasibility but may produce suboptimal routes due to its local decision-making nature.

2. **Greedy + 2-Opt**  
   Applies the 2-Opt local search algorithm to refine the greedy-generated route by swapping segments that reduce total distance.

3. **Greedy Local Search**  
   Iteratively chooses the nearest shelf that contributes to remaining demand, dynamically updating choices based on current state.

4. **Local Search + 2-Opt**  
   Uses nearest-neighbor to build an initial solution, then applies 2-Opt refinement.

### 🧮 DP-Enhanced Algorithms

1. **DP-Greedy**  
   - Uses **Dynamic Programming (DP)** for exact optimization when the number of shelves is small (≤18).
   - Falls back to Greedy for larger cases to ensure tractability.

2. **DP-Greedy + 2-Opt**  
   Combines DP-Greedy with 2-Opt refinement, enabling high-quality solutions even in large-scale scenarios.

⸻

## 🧪 Experiment Setup

### 🖥️ Environment

- Machine: Apple M3 Pro, 18GB RAM
- Language: Python 3.12.7

### 🧾 Data Generation

We synthetically generated test cases with varied scale using a Python + Bash pipeline. Each scale (small, medium, large) contains 10 randomized instances.

| Category | # Products (N) | # Shelves (M) | Shelf Capacity | Target Shelves |
|----------|----------------|----------------|----------------|----------------|
| Small    | 10             | 20             | 20             | 6              |
| Medium   | 40             | 100            | 100            | 20             |
| Large    | 100            | 400            | 200            | 40             |

Each test case includes a supply matrix \(Q\), distance matrix \(D\), and demand vector \(q\). Expected outputs from Greedy are used as baseline references.

### 🧪 Evaluated Algorithms

- **Exact DP**: Only feasible for small cases (≤18 shelves).
- **Greedy**
- **Greedy + 2-Opt**
- **DP-Greedy**
- **DP-Greedy + 2-Opt**

### 📏 Evaluation Metrics

- **Runtime** (seconds)
- **Number of shelves visited**
- **Total travel distance**
- **Feasibility** (whether demand is satisfied)

---

## 📊 Results

### ⏱️ Runtime

- **DP-Greedy** was the fastest across all problem sizes.
- **Greedy** had slightly higher runtime.
- Methods with 2-Opt (e.g., DP-Greedy + 2-Opt) were 7–9× slower than DP-Greedy on large inputs but still under 0.05s.

### 📦 Shelves Visited

- All algorithms selected a similar number of shelves.
- **DP-Greedy** and its 2-Opt variant selected **slightly fewer shelves**, indicating better overall efficiency.

### 📏 Travel Distance

- **DP-Greedy + 2-Opt** consistently achieved the **shortest travel distance**, especially on large instances (~200 units less than Greedy).
- Greedy-based methods without local search yielded longer routes.

### 📌 Summary Table

| Algorithm               | Runtime (L) | Shelves (L) | Distance (L) |
|-------------------------|-------------|-------------|--------------|
| DP-Greedy               | 0.00486s    | 399         | 1783.3       |
| DP-Greedy + 2-Opt       | 0.04199s    | 399         | **1581.2**   |
| Greedy                  | 0.03771s    | 397         | 1777.8       |
| Greedy + 2-Opt          | 0.04841s    | 397         | 1777.8       |
| Local Search + 2-Opt    | 0.03354s    | 399         | 1597.3       |

---

## ✅ Conclusion

Our comparative study highlights the **DP-Greedy + 2-Opt** approach as the most effective overall:

- **Fast enough** for large-scale deployment.
- **High-quality routes**, consistently better than basic heuristics.
- **Robust and scalable**, balancing optimality and efficiency.

This makes it a strong candidate for real-world warehouse optimization applications.

---

## 📎 Citation and Acknowledgements

Developed as part of IT3052E Project at  SOICT.  
Authors: Nguyen T. Hieu, Nguyen Q. Duong, Do X. Truong, Mai G. Hy  
Supervisor: Pham Q. Dung

Project Repository: [GitHub Link](https://github.com/hieunguyen-cyber/Order-Picking-up-route-in-Warehouse-Large-Size)


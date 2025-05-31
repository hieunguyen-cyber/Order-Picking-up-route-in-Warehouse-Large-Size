import fire
import json
import time

def solve_warehouse_optimization(N_products, M_shelves, Q, distance, q_require):
    current_position = 0  # bắt đầu tại cửa kho
    remaining = q_require.copy()
    selected_shelves = []
    visited = set()

    while any(remaining[i] > 0 for i in range(N_products)):
        candidates = []
        for j in range(1, M_shelves + 1):
            if j in visited:
                continue
            if any(Q[i][j] > 0 and remaining[i] > 0 for i in range(N_products)):
                candidates.append(j)

        if not candidates:
            raise ValueError("Không thể thỏa mãn nhu cầu")

        # Chọn kệ gần nhất trong số các ứng viên
        next_shelf = min(candidates, key=lambda j: distance[current_position][j])
        selected_shelves.append(next_shelf)
        visited.add(next_shelf)

        for i in range(N_products):
            taken = min(Q[i][next_shelf], remaining[i])
            remaining[i] -= taken

        current_position = next_shelf

    return len(selected_shelves), selected_shelves


def main(input_json_file, output_path, time_path):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    N_products = data["N_products"]
    M_shelves = data["M_shelves"]
    Q = data["Q"]
    distance = data["distance"]
    q_require = data["q_require"]

    start_time = time.time()
    d, m = solve_warehouse_optimization(N_products, M_shelves, Q, distance, q_require)
    runtime = time.time() - start_time

    with open(output_path, "w") as f_out:
        f_out.write(f"{d}\n")
        f_out.write(" ".join(map(str, m)) + "\n")

    with open(time_path, "w") as f_time:
        f_time.write(f"{runtime:.6f} seconds\n")


if __name__ == "__main__":
    fire.Fire(main)
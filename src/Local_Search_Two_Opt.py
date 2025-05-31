import fire
import json
import time
import copy

def solve_warehouse_optimization(N_products, M_shelves, Q, distance, q_require):
    def nearest_neighbor(dist, Q, q_require):
        current_hold = [0] * N_products
        n = len(dist)
        unvisited = set(range(1, n))  # chỉ kệ 1..M, bỏ 0 vì là cửa kho
        path = [0]  # bắt đầu từ cửa kho
        current = 0

        while unvisited:
            next_city = min(unvisited, key=lambda city: dist[current][city])
            path.append(next_city)
            unvisited.remove(next_city)
            for i in range(N_products):
                current_hold[i] += Q[i][next_city]
            current = next_city

            if all(current_hold[i] >= q_require[i] for i in range(N_products)):
                break
        path.append(0)  # quay lại cửa kho
        return path

    def two_opt(path, dist):
        improved = True
        n = len(path)
        while improved:
            improved = False
            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    a, b = path[i - 1], path[i]
                    c, d = path[j], path[j + 1]
                    if dist[a][b] + dist[c][d] > dist[a][c] + dist[b][d]:
                        path[i:j + 1] = reversed(path[i:j + 1])
                        improved = True
        return path

    # Build path
    init_path = nearest_neighbor(distance, Q, q_require)
    final_path = two_opt(init_path, distance)

    # Bỏ vị trí đầu và cuối (cửa kho = 0)
    route_only_shelves = [x for x in final_path if x != 0]
    return len(route_only_shelves), route_only_shelves

def main(input_json_file, output_path, time_path):
    # Đọc dữ liệu từ file JSON
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    N_products = data["N_products"]
    M_shelves = data["M_shelves"]
    Q = data["Q"]
    distance = data["distance"]
    q_require = data["q_require"]

    # Đo thời gian giải bài toán
    start_time = time.time()
    d, m = solve_warehouse_optimization(N_products, M_shelves, Q, distance, q_require)
    runtime = time.time() - start_time

    # Ghi kết quả ra file output.txt (2 dòng)
    with open(output_path, "w") as f_out:
        f_out.write(f"{d}\n")
        f_out.write(" ".join(map(str, m)) + "\n")

    # Ghi thời gian chạy ra file runtime.txt
    with open(time_path, "w") as f_time:
        f_time.write(f"{runtime:.6f} seconds\n")

if __name__ == "__main__":
    fire.Fire(main)
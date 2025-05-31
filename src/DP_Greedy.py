import fire
import json
import time

def solve_exact_dp(N, M, Q, dist, q_req):
    max_mask = 1 << M
    sumQ = [[0]*N for _ in range(max_mask)]
    valid = [False]*max_mask

    for mask in range(1, max_mask):
        low = mask & -mask
        j = (low.bit_length() - 1)
        prev = mask ^ low
        for p in range(N):
            sumQ[mask][p] = sumQ[prev][p] + Q[p][j+1]
        if all(sumQ[mask][p] >= q_req[p] for p in range(N)):
            valid[mask] = True

    INF = 10**18
    dp = [[INF]*M for _ in range(max_mask)]
    parent = [[-1]*M for _ in range(max_mask)]

    for j in range(M):
        dp[1<<j][j] = dist[0][j+1]

    for mask in range(max_mask):
        for j in range(M):
            if not (mask & (1<<j)): 
                continue
            prev = mask ^ (1<<j)
            if prev == 0: 
                continue
            for k in range(M):
                if not (prev & (1<<k)): 
                    continue
                cost = dp[prev][k] + dist[k+1][j+1]
                if cost < dp[mask][j]:
                    dp[mask][j] = cost
                    parent[mask][j] = k

    best = INF
    best_mask, best_end = 0, -1
    for mask in range(max_mask):
        if not valid[mask]: 
            continue
        for j in range(M):
            if not (mask & (1<<j)): 
                continue
            cost = dp[mask][j] + dist[j+1][0]
            if cost < best:
                best, best_mask, best_end = cost, mask, j

    if best_end == -1:
        return False, None, None

    path = []
    mask, j = best_mask, best_end
    while mask:
        path.append(j+1)
        pj = parent[mask][j]
        mask ^= (1<<j)
        j = pj
    path.reverse()

    return True, len(path), path

def solve_heuristic(N, M, Q, dist, q_req):
    hold = [0]*N
    unvis = set(range(1, M+1))
    path = []
    cur = 0
    while unvis:
        nxt = min(unvis, key=lambda j: dist[cur][j])
        unvis.remove(nxt)
        path.append(nxt)
        for p in range(N):
            hold[p] += Q[p][nxt]
        cur = nxt
        if all(hold[p] >= q_req[p] for p in range(N)):
            break

    return len(path), path

def solve_warehouse_optimization(N_products, M_shelves, Q, distance, q_require):
    if M_shelves <= 18:
        feasible, d, m = solve_exact_dp(N_products, M_shelves, Q, distance, q_require)
        if feasible:
            return d, m
    return solve_heuristic(N_products, M_shelves, Q, distance, q_require)

def main(input_json_file, output_path, time_path):
    # Đọc dữ liệu từ file JSON
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
        if d is None:
            f_out.write("NOT FEASIBLE\n")
        else:
            f_out.write(f"{d}\n")
            f_out.write(" ".join(map(str, m)) + "\n")

    with open(time_path, "w") as f_time:
        f_time.write(f"{runtime:.6f} seconds\n")

if __name__ == "__main__":
    fire.Fire(main)
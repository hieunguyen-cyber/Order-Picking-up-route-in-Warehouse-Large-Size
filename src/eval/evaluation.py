def grade_with_path_similarity(selected_shelves, d, expected_file):
    def evaluate_path_cost(path, d):
        if not path:
            return 0
        cost = d[0][path[0]]
        for i in range(len(path) - 1):
            cost += d[path[i]][path[i+1]]
        cost += d[path[-1]][0]
        return cost

    def levenshtein(a, b):
        n, m = len(a), len(b)
        dp = [[0]*(m+1) for _ in range(n+1)]
        for i in range(n+1):
            dp[i][0] = i
        for j in range(m+1):
            dp[0][j] = j
        for i in range(1, n+1):
            for j in range(1, m+1):
                cost = 0 if a[i-1] == b[j-1] else 1
                dp[i][j] = min(dp[i-1][j] + 1,      # delete
                               dp[i][j-1] + 1,      # insert
                               dp[i-1][j-1] + cost) # replace
        return dp[n][m]

    # Đọc file kỳ vọng
    with open(expected_file) as f:
        lines = [line.strip() for line in f if line.strip()]
        expected_cost = int(lines[0])
        expected_shelves = list(map(int, lines[1].split())) if len(lines) > 1 else []

    # Tính chi phí
    your_cost = evaluate_path_cost(selected_shelves, d)

    # Phần 1: Điểm chi phí (70)
    if your_cost == expected_cost:
        score_cost = 70
    elif your_cost > expected_cost:
        over = your_cost - expected_cost
        penalty_ratio = over / expected_cost
        score_cost = max(0, 70 - int(penalty_ratio * 70))
    else:
        score_cost = 65  # Có thể tối ưu hơn, nhưng không chắc đúng

    # Phần 2: Điểm hành trình (30)
    edist = levenshtein(selected_shelves, expected_shelves)
    max_len = max(len(selected_shelves), len(expected_shelves))
    similarity = 1 - (edist / max_len) if max_len > 0 else 1
    score_path = int(similarity * 30)

    total_score = score_cost + score_path
    return total_score
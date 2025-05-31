import fire
import json

def read_input_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Dòng 1: N_products và M_shelves
    N_products, M_shelves = map(int, lines[0].split())

    # Dòng 2 -> N_products + 1: thông tin Q
    Q = [[] for _ in range(N_products)]
    for i in range(N_products):
        Q[i] = [0] + list(map(int, lines[1 + i].split()))

    # Tiếp theo là M_shelves + 1 dòng: thông tin distance
    distance = [[] for _ in range(M_shelves + 1)]
    for i in range(M_shelves + 1):
        distance[i] = list(map(int, lines[1 + N_products + i].split()))

    # Dòng cuối cùng: q_require
    q_require = list(map(int, lines[1 + N_products + M_shelves + 1].split()))

    return {
        "N_products": N_products,
        "M_shelves": M_shelves,
        "Q": Q,
        "distance": distance,
        "q_require": q_require
    }

def main(filename):
    result = read_input_from_file(filename)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    fire.Fire(main)
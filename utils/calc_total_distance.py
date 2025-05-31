import fire
import json

def load_distance_matrix(input_file):
    """Đọc file input và trả về ma trận khoảng cách."""
    from read_input import read_input_from_file
    data = read_input_from_file(input_file)
    return data["distance"]

def parse_route_file(route_file):
    with open(route_file, 'r') as f:
        lines = f.readlines()
    route = list(map(int, lines[1].strip().split()))
    return route

def calc_route_distance(distance_matrix, route):
    """Tính tổng khoảng cách từ ma trận và lộ trình."""
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i + 1]]
    return total

def compute_distance(input_file, route_file):
    """Tổng hợp: đọc file input và route, tính khoảng cách."""
    distance_matrix = load_distance_matrix(input_file)
    route = parse_route_file(route_file)
    total_distance = calc_route_distance(distance_matrix, route)
    return total_distance

if __name__ == '__main__':
    fire.Fire(compute_distance)
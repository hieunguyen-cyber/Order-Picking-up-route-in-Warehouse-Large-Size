import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import fire
import numpy as np
import dataframe_image as dfi

# Hàm đọc dữ liệu runtime từ file txt
def read_runtime_data(runtime_path):
    data = {'small': [], 'medium': [], 'large': []}
    if not os.path.exists(runtime_path):
        print(f"Thư mục {runtime_path} không tồn tại.")
        return data
    sub = data.keys()
    for sub_folder in sub:
        path = os.path.join(runtime_path, sub_folder)
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            for file in files:
                file_path = os.path.join(path, file)
                with open(file_path, 'r') as f:
                    line = list(f.readline().strip().split())[0]
                    try:
                        runtime = float(line)
                        data[sub_folder].append(runtime)
                    except ValueError:
                        print(f"Lỗi: không thể chuyển giá trị từ {file_path} thành float.")
    return data

# Hàm vẽ biểu đồ runtime và lưu thành PNG
def plot_runtime(runtime_path, output_file='result/figure/runtime_comparison.png'):
    data = read_runtime_data(runtime_path)

    # Trích tên mô hình từ path: vd: test/Greedy/runtime => Greedy
    model_name = os.path.basename(os.path.dirname(runtime_path.rstrip('/')))

    fig = go.Figure()
    x = []
    y = []
    colors = []
    sizes = ['small', 'medium', 'large']
    color_map = {'small': 'green', 'medium': 'gold', 'large': 'red'}

    for size in sizes:
        values = data.get(size, [])
        x.extend([str(i) for i in range(len(values))])
        y.extend(values)
        colors.extend([color_map[size]] * len(values))

    for size in sizes:
        mask = [c == color_map[size] for c in colors]
        x_size = [x[i] for i in range(len(x)) if mask[i]]
        y_size = [y[i] for i in range(len(y)) if mask[i]]
        fig.add_trace(go.Scatter(
            x=x_size,
            y=y_size,
            mode='lines+markers',
            name=size,
            line=dict(color=color_map[size]),
            marker=dict(size=8)
        ))

    fig.update_layout(
        title=f"So sánh thời gian chạy - {model_name}",
        xaxis_title='Test case',
        yaxis_title='Runtime (s)',
        showlegend=True
    )

    fig.write_image(output_file, format='png')
    print(f"✅ Biểu đồ runtime đã được lưu tại {output_file}")

def read_shelf_data(folder_path):
    sizes = ['small', 'medium', 'large']
    result = {}
    for size in sizes:
        size_folder = os.path.join(folder_path, size)
        values = []
        for fname in sorted(os.listdir(size_folder)):
            with open(os.path.join(size_folder, fname)) as f:
                d = f.readline().strip()
                try:
                    values.append(int(d))
                except:
                    values.append(None)
        result[size] = values
    return result

def plot_shelves(eval_path, output_path, output_file='result/figure/shelf_comparison.png'):
    eval_data = read_shelf_data(eval_path)
    output_data = read_shelf_data(output_path)

    # Trích tên mô hình từ đường dẫn output_path
    model_name = os.path.basename(os.path.dirname(output_path.rstrip('/')))

    sizes = ['small', 'medium', 'large']
    records = []

    for size in sizes:
        eval_values = eval_data.get(size, [])
        output_values = output_data.get(size, [])
        for i in range(len(eval_values)):
            records.append({
                "Size": size,
                "Case": f"{size}_{i+1}",
                "Source": "Eval",
                "Shelves": eval_values[i]
            })
            records.append({
                "Size": size,
                "Case": f"{size}_{i+1}",
                "Source": model_name,
                "Shelves": output_values[i] if i < len(output_values) else None
            })

    df = pd.DataFrame(records)

    fig = px.bar(
        df,
        x="Case",
        y="Shelves",
        color="Source",
        barmode="group",
        title=f"So sánh số kệ giữa Eval và {model_name}",
        color_discrete_map={"Eval": "black", model_name: "royalblue"},
    )

    fig.update_layout(
        xaxis_title="Test Case theo Size",
        yaxis_title="Số kệ được chọn",
        legend_title="Nguồn",
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    fig.write_image(output_file)
    print(f"✅ Biểu đồ số kệ đã được lưu tại {output_file}")
# Hàm đọc dữ liệu tổng khoảng cách từ file txt
def read_distance_data(data_path):
    data = {'small': {'eval': [], 'model': []}, 'medium': {'eval': [], 'model': []}, 'large': {'eval': [], 'model': []}}
    subs = data.keys()
    if not os.path.exists(data_path):
        print(f"Thư mục {data_path} không tồn tại.")
        return data
    for sub in subs:
        for file in os.listdir(os.path.join(data_path, sub)):
            if file.endswith('.txt'):
                with open(os.path.join(os.path.join(data_path, sub), file), 'r') as f:
                    print(f)
                    lines = f.readlines()
                    if lines:
                        try:
                            eval_dist, model_dist = map(int, lines[0].strip().split())
                            data[sub]['eval'].append(eval_dist)
                            data[sub]['model'].append(model_dist)
                        except ValueError:
                            print(f"Lỗi định dạng ở file {file}")
    return data

def plot_distances(data_path, output_file='result/figure/distance_comparison.png'):
    data = read_distance_data(data_path)

    # Trích tên mô hình từ đường dẫn
    model_name = os.path.basename(os.path.dirname(data_path.rstrip('/')))

    sizes = ['small', 'medium', 'large']
    records = []

    for size in sizes:
        eval_values = data[size]["eval"]
        model_values = data[size]["model"]
        for i in range(len(eval_values)):
            records.append({
                "Size": size,
                "Case": f"{size}_{i+1}",
                "Source": "Eval",
                "Distance": eval_values[i]
            })
            records.append({
                "Size": size,
                "Case": f"{size}_{i+1}",
                "Source": model_name,
                "Distance": model_values[i] if i < len(model_values) else None
            })

    df = pd.DataFrame(records)

    fig = px.bar(
        df,
        x="Case",
        y="Distance",
        color="Source",
        barmode="group",
        title=f"So sánh tổng khoảng cách giữa Eval và {model_name}",
        color_discrete_map={"Eval": "black", model_name: "crimson"},
    )

    fig.update_layout(
        xaxis_title="Test Case theo Size",
        yaxis_title="Tổng khoảng cách",
        legend_title="Nguồn",
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    fig.write_image(output_file)
    print(f"✅ Biểu đồ tổng khoảng cách đã được lưu tại {output_file}")
    
def analyze_and_plot(models, base_dir="test", output_dir="result/figure"):
    SIZES = ["small", "medium", "large"]
    METRICS = ["runtime", "output", "dist"]

    if isinstance(models, str):
        models = models.split(",")

    def read_runtime(path):
        with open(path, "r") as f:
            return float(f.readline().split()[0])

    def read_output(path):
        with open(path, "r") as f:
            return int(f.readline().strip())

    def read_dist(path):
        with open(path, "r") as f:
            return int(f.readline().strip().split()[1])

    def aggregate_metric(model, size, metric):
        dir_path = os.path.join(base_dir, model, metric, size)
        values = []
        for filename in sorted(os.listdir(dir_path), key=lambda x: int(os.path.splitext(x)[0])):
            file_path = os.path.join(dir_path, filename)
            if metric == "runtime":
                val = read_runtime(file_path)
            elif metric == "output":
                val = read_output(file_path)
            elif metric == "dist":
                val = read_dist(file_path)
            values.append(val)
        return np.mean(values)

    # Collect all results
    results = {metric: {size: {} for size in SIZES} for metric in METRICS}
    for metric in METRICS:
        for size in SIZES:
            for model in models:
                avg = aggregate_metric(model, size, metric)
                results[metric][size][model] = avg

    # Plotting function
    def plot_comparison(metric_name, title, yaxis_title, filename_prefix):
        fig = go.Figure()
        for size in SIZES:
            y = [results[metric_name][size][model] for model in models]
            fig.add_trace(go.Bar(name=size, x=models, y=y))
        fig.update_layout(
            barmode='group',
            title=title,
            xaxis_title="Model",
            yaxis_title=yaxis_title,
            legend_title="Size",
        )
        fig.write_image(os.path.join(output_dir, f"{filename_prefix}.png"))

    # Generate and save plots
    plot_comparison("runtime", "So sánh thời gian chạy", "Thời gian (giây)", "runtime_comparison")
    plot_comparison("output", "So sánh số lượng kệ", "Tổng số kệ", "output_comparison")
    plot_comparison("dist", "So sánh tổng khoảng cách", "Tổng khoảng cách", "dist_comparison")
    print(f"✅ Figures (PNG) saved to: {output_dir}")
def compare_meta_vs_base(model, base_dir="test", output_dir="result/figure"):
    SIZES = ["small", "medium", "large"]
    METAS = ["GA", "ACO", "SA"]
    METRICS = ["runtime", "output", "dist"]
    LABELS = ["Base", "GA", "ACO", "SA"]
    COLORS = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]

    def read_runtime(path):
        with open(path, "r") as f:
            return float(f.readline().split()[0])

    def read_output(path):
        with open(path, "r") as f:
            return int(f.readline().strip())

    def read_dist(path):
        with open(path, "r") as f:
            return int(f.readline().strip().split()[1])

    def collect_values(metric, size):
        if metric == "runtime":
            base_path = os.path.join(base_dir, model, "runtime", size)
            meta_paths = [os.path.join(base_dir, "meta", model, m, "runtime", size) for m in METAS]
            reader = read_runtime
        elif metric == "output":
            base_path = os.path.join(base_dir, model, "output", size)
            meta_paths = [os.path.join(base_dir, "meta", model, m, "output", size) for m in METAS]
            reader = read_output
        elif metric == "dist":
            base_path = os.path.join(base_dir, model, "dist", size)
            meta_paths = [os.path.join(base_dir, "meta", model, m, "dist", size) for m in METAS]
            reader = read_dist
        else:
            return []

        def average_from_dir(folder):
            vals = []
            if not os.path.exists(folder):
                return 0
            for fname in os.listdir(folder):
                fpath = os.path.join(folder, fname)
                try:
                    vals.append(reader(fpath))
                except:
                    continue
            return np.mean(vals) if vals else 0

        return [average_from_dir(p) for p in [base_path] + meta_paths]

    for metric in METRICS:
        fig = go.Figure()
        for i, label in enumerate(LABELS):
            y_values = [collect_values(metric, size)[i] for size in SIZES]
            fig.add_trace(go.Bar(
                name=label,
                x=SIZES,
                y=y_values,
                marker_color=COLORS[i % len(COLORS)],
                offsetgroup=i,
            ))

        fig.update_layout(
            title=f"So sánh {metric.upper()} giữa base và metaheuristics - {model}",
            xaxis_title="Kích thước dữ liệu",
            yaxis_title=metric.capitalize(),
            barmode="group",
            template="plotly_white",
            legend_title="Mô hình"
        )

        out_path = os.path.join(output_dir, f"{model}_meta_{metric}.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.write_image(out_path)
        print(f"✅ Đã lưu biểu đồ {metric} meta tại: {out_path}")

def compare_meta_across_models(models, base_dir="test/meta", output_dir="result/figure"):
    SIZES = ["small", "medium", "large"]
    METAS = ["GA", "ACO", "SA"]
    METRICS = ["runtime", "output", "dist"]
    COLORS = ["#EF553B", "#00CC96", "#AB63FA"]

    if isinstance(models, str):
        models = [m.strip() for m in models.replace(",", " ").split() if m.strip()]

    os.makedirs(output_dir, exist_ok=True)

    def read_runtime(path):
        with open(path, "r") as f:
            return float(f.readline().split()[0])

    def read_output(path):
        with open(path, "r") as f:
            return int(f.readline().strip())

    def read_dist(path):
        with open(path, "r") as f:
            return int(f.readline().strip().split()[1])

    for metric in METRICS:
        meta_means = {meta: [] for meta in METAS}
        base_means = []

        for model in models:
            # Calculate base mean for this model
            vals_base = []
            for size in SIZES:
                if metric == "runtime":
                    path = os.path.join("test", model, "runtime", size)
                    reader = read_runtime
                elif metric == "output":
                    path = os.path.join("test", model, "output", size)
                    reader = read_output
                elif metric == "dist":
                    path = os.path.join("test", model, "dist", size)
                    reader = read_dist
                else:
                    continue

                if not os.path.exists(path):
                    continue
                for fname in os.listdir(path):
                    fpath = os.path.join(path, fname)
                    try:
                        vals_base.append(reader(fpath))
                    except:
                        continue
            base_means.append(np.mean(vals_base) if vals_base else 0)

            # Calculate meta means for this model
            for meta in METAS:
                vals = []
                for size in SIZES:
                    dir_path = os.path.join(base_dir, model, meta, metric, size)
                    if not os.path.exists(dir_path):
                        continue
                    for fname in os.listdir(dir_path):
                        fpath = os.path.join(dir_path, fname)
                        try:
                            if metric == "runtime":
                                vals.append(read_runtime(fpath))
                            elif metric == "output":
                                vals.append(read_output(fpath))
                            elif metric == "dist":
                                vals.append(read_dist(fpath))
                        except:
                            continue
                if vals:
                    mean_val = np.mean(vals)
                    meta_means[meta].append(mean_val)
                else:
                    meta_means[meta].append(0)

        fig = go.Figure()
        # Add base bar
        fig.add_trace(go.Bar(
            name="Base",
            x=models,
            y=base_means,
            marker_color="#636EFA",
        ))
        # Add meta bars
        for i, meta in enumerate(METAS):
            fig.add_trace(go.Bar(
                name=meta,
                x=models,
                y=meta_means[meta],
                marker_color=COLORS[i],
            ))

        fig.update_layout(
            title=f"So sánh {metric.upper()} giữa các metaheuristics và thuật toán gốc trên nhiều mô hình",
            xaxis_title="Mô hình",
            yaxis_title=metric.capitalize(),
            barmode="group",
            template="plotly_white",
            legend_title="Thuật toán"
        )

        fig.write_image(os.path.join(output_dir, f"meta_compare_with_base_{metric}.png"))
        print(f"📊 Đã lưu biểu đồ meta + base theo {metric}")
# Giao diện dòng lệnh với fire
def main():
    fire.Fire({
        "plot_runtime": plot_runtime,
        "plot_shelves": plot_shelves,
        "plot_distances": plot_distances,
        "plot_metrics": analyze_and_plot,
        "compare_meta_vs_base": compare_meta_vs_base,
        "compare_meta_across_models": compare_meta_across_models
    })

if __name__ == '__main__':
    main()
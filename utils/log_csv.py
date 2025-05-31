import os
import numpy as np
import pandas as pd
import fire
import dataframe_image as dfi

def generate_summary(models, base_dir="test", output_csv="result/table/summary.csv", output_png="result/table/summary.png"):
    SIZES = ["small", "medium", "large"]
    METRICS = ["runtime", "output", "dist"]

    if isinstance(models, str):
        models = models.split(",")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(os.path.dirname(output_png), exist_ok=True)

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

    # Thu thập dữ liệu
    rows = []
    for model in models:
        row = {"Model": model}
        for size in SIZES:
            for metric in METRICS:
                val = aggregate_metric(model, size, metric)
                col_name = f"{metric}_{size}"
                if metric in ["runtime", "dist"]:
                    row[col_name] = f"{val:.2f}"
                else:
                    row[col_name] = f"{int(round(val))}"
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"✅ CSV saved to {output_csv}")

    # Format lại DataFrame cho đẹp hơn
    df_styled = (
        df.style
        .set_caption("So sánh các mô hình theo Runtime, Output và Distance")
        .set_table_styles(
            [{
                'selector': 'caption',
                'props': [('font-size', '16px'), ('font-weight', 'bold')]
            },
            {
                'selector': 'th',
                'props': [('background-color', '#dbefff'), ('color', 'black'), ('font-weight', 'bold')]
            }]
        )
        .set_properties(**{
            'border': '1px solid black',
            'padding': '6px',
            'font-size': '12px'
        })
    )

    # Lưu bảng dưới dạng PNG đẹp như LaTeX
    dfi.export(df_styled, output_png)
    print(f"✅ Pretty LaTeX-style table saved to {output_png}")

if __name__ == "__main__":
    fire.Fire(generate_summary)
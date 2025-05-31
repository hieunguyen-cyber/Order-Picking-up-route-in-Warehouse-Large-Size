#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <model>"
  exit 1
fi

model=$1

mkdir -p result/figure
mkdir -p result/table

echo "Plotting runtime..."
python3 utils/plot.py plot_runtime "test/${model}/runtime" "result/figure/${model}_runtime_comparision.png"

echo "Plotting distance..."
python3 utils/plot.py plot_distances "test/${model}/dist" "result/figure/${model}_distance_comparison.png"

echo "Plotting shelves..."
python3 utils/plot.py plot_shelves "test/eval" "test/${model}/output" "result/figure/${model}_shelf_comparison.png"
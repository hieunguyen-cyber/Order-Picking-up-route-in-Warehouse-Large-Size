#!/bin/bash

model=""
meta="none"

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --model)
      model="$2"
      shift 2
      ;;
    --meta)
      meta="$2"
      shift 2
      ;;
    *)
      echo "❌ Unknown parameter: $1"
      exit 1
      ;;
  esac
done

if [ -z "$model" ]; then
  echo "Usage: $0 --model <model> [--meta <GA|ACO|SA>]"
  exit 1
fi

# Xác định đường dẫn theo meta hoặc không
if [[ "$meta" == "none" ]]; then
  runtime_dir="test/${model}/runtime"
  dist_dir="test/${model}/dist"
  output_dir="test/${model}/output"
  suffix=""
else
  runtime_dir="test/meta/${model}/${meta}/runtime"
  dist_dir="test/meta/${model}/${meta}/dist"
  output_dir="test/meta/${model}/${meta}/output"
  suffix="_${meta}"
fi

mkdir -p result/figure/${model}
mkdir -p result/table

echo "Plotting runtime..."
python3 utils/plot.py plot_runtime "$runtime_dir" "result/figure/${model}/${model}${suffix}_runtime_comparision.png"

echo "Plotting distance..."
python3 utils/plot.py plot_distances "$dist_dir" "result/figure/${model}/${model}${suffix}_distance_comparison.png"

echo "Plotting shelves..."
python3 utils/plot.py plot_shelves "test/eval" "$output_dir" "result/figure/${model}/${model}${suffix}_shelf_comparison.png"
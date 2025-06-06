#!/bin/bash

MODEL=("Local_Search_Two_Opt" "Greedy_Local_Search" "DP_Greedy_Two_Opt" "Greedy" "DP_Greedy")
model=""
meta="none"

# Hàm kiểm tra model có hợp lệ không
function contains() {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
  return 1
}

# Đọc tham số dòng lệnh
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

# Kiểm tra model hợp lệ
if ! contains "$model" "${MODEL[@]}"; then
  echo "❌ Invalid model: $model"
  echo "Available models: ${MODEL[*]}"
  exit 1
fi

echo "📏 Evaluating model: $model"
[[ "$meta" != "none" ]] && echo "✨ Using metaheuristic refinement: $meta"

for SIZE in small medium large; do
  echo "🔍 Processing $SIZE ..."

  if [[ "$meta" == "none" ]]; then
    OUTPUT_PATH_ROOT="test/${model}/output/${SIZE}"
    DIST_DIR="test/${model}/dist/${SIZE}"
  else
    OUTPUT_PATH_ROOT="test/meta/${model}/${meta}/output/${SIZE}"
    DIST_DIR="test/meta/${model}/${meta}/dist/${SIZE}"
  fi

  mkdir -p "$DIST_DIR"

  for input_file in test/input/$SIZE/*.txt; do
    filename=$(basename "$input_file")
    input_path="test/input/$SIZE/$filename"
    eval_path="test/eval/$SIZE/$filename"
    output_path="${OUTPUT_PATH_ROOT}/$filename"

    eval_dist=$(python3 utils/calc_total_distance.py "$input_path" "$eval_path")
    output_dist=$(python3 utils/calc_total_distance.py "$input_path" "$output_path")

    echo "$eval_dist $output_dist" > "$DIST_DIR/$filename"
  done
done

echo "✅ Evaluation distances saved to: $DIST_DIR/"
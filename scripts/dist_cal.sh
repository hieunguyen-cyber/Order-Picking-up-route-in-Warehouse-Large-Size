#!/bin/bash

# Danh sách model hợp lệ
MODEL=("Local_Search_Two_Opt" "Greedy_Local_Search" "DP_Greedy_Two_Opt" "Greedy" "DP_Greedy")

# Hàm kiểm tra model có trong danh sách không
function contains() {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
  return 1
}

# Lấy tham số --model
model=""
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --model)
      model="$2"
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

# Bắt đầu xử lý
echo "📏 Evaluating model: $model"

for SIZE in small medium large; do
  echo "🔍 Processing $SIZE ..."

  # Tạo thư mục nếu chưa có
  DIST_DIR="test/${model}/dist/${SIZE}"
  mkdir -p "$DIST_DIR"

  for input_file in test/input/$SIZE/*.txt; do
    filename=$(basename "$input_file")
    input_path="test/input/$SIZE/$filename"
    eval_path="test/eval/$SIZE/$filename"
    output_path="test/${model}/output/$SIZE/$filename"

    # Tính distance
    eval_dist=$(python3 utils/calc_total_distance.py "$input_path" "$eval_path")
    output_dist=$(python3 utils/calc_total_distance.py "$input_path" "$output_path")

    # Ghi vào file riêng theo tên case
    echo "$eval_dist $output_dist" > "$DIST_DIR/$filename"
  done
done

echo "✅ Evaluation distances saved to test/${model}/dist/{small,medium,large}/"
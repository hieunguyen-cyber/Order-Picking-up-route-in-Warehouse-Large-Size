#!/bin/bash

INPUT_DIR="test/input"
OUTPUT_DIR="test/Greedy_Local_Search/output"
TIME_DIR="test/Greedy_Local_Search/runtime"
NUM_CASE=5

mkdir -p "$OUTPUT_DIR"
mkdir -p "$TIME_DIR"
model=Greedy_Local_Search

# Default stage values
stage=-1
stop_stage=-1

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --stage) stage="$2"; shift ;;
    --stop_stage) stop_stage="$2"; shift ;;
    *) echo "❌ Unknown argument: $1"; exit 1 ;;
  esac
  shift
done

# Stage 1: Compute Output
if [ "$stage" -le 1 ] && [ "$stop_stage" -ge 1 ]; then
  for SIZE in small medium large; do
    for input_file in "$INPUT_DIR/$SIZE"/*.txt; do
      filename=$(basename "$input_file" .txt)

      echo "Processing $input_file ..."

      # Gọi script python đọc input và xuất JSON
      json_output=$(python3 utils/read_input.py "$input_file")

      N_PRODUCTS=$(echo "$json_output" | jq '.N_products')
      M_SHELVES=$(echo "$json_output" | jq '.M_shelves')
      Q=$(echo "$json_output" | jq -c '.Q')
      DISTANCE=$(echo "$json_output" | jq -c '.distance')
      Q_REQUIRE=$(echo "$json_output" | jq -c '.q_require')

      TEMP_JSON_FILE="temp_${filename}.json"
      echo "{
        \"N_products\": $N_PRODUCTS,
        \"M_shelves\": $M_SHELVES,
        \"Q\": $Q,
        \"distance\": $DISTANCE,
        \"q_require\": $Q_REQUIRE
      }" > "$TEMP_JSON_FILE"

      OUTPUT_PATH="${OUTPUT_DIR}/${SIZE}/${filename}.txt"
      TIME_PATH="${TIME_DIR}/${SIZE}/${filename}.txt"

      mkdir -p "$(dirname "$OUTPUT_PATH")"
      mkdir -p "$(dirname "$TIME_PATH")"

      # Chạy solver với output và time path
      python3 src/Greedy_Local_Search.py --input_json_file="$TEMP_JSON_FILE" --output_path="$OUTPUT_PATH" --time_path="$TIME_PATH"

      # Xóa file JSON tạm
      rm "$TEMP_JSON_FILE"

      echo "✅ Done $filename: output -> $OUTPUT_PATH, time -> $TIME_PATH"
    done
  done
fi

if [ "$stage" -le 2 ] && [ "$stop_stage" -ge 2 ]; then
    bash scripts/dist_cal.sh --model $model
    bash scripts/plot.sh $model
fi
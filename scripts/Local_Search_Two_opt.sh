#!/bin/bash

INPUT_DIR="test/input"
OUTPUT_DIR="test/Local_Search_Two_Opt/output"
TIME_DIR="test/Local_Search_Two_Opt/runtime"
META_DIR="test/meta/Local_Search_Two_Opt"

model=Local_Search_Two_Opt
stage=-1
stop_stage=-1
meta="none"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --stage) stage="$2"; shift ;;
    --stop_stage) stop_stage="$2"; shift ;;
    --meta) meta="$2"; shift ;;
    *) echo "❌ Unknown argument: $1"; exit 1 ;;
  esac
  shift
done

# Stage 1: Run algorithm and optionally apply metaheuristic
if [ "$stage" -le 1 ] && [ "$stop_stage" -ge 1 ]; then
  for SIZE in small medium large; do
    for input_file in "$INPUT_DIR/$SIZE"/*.txt; do
      filename=$(basename "$input_file" .txt)
      echo "📦 Processing $input_file ..."

      # Convert input to JSON
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

      python3 src/${model}.py --input_json_file="$TEMP_JSON_FILE" --output_path="$OUTPUT_PATH" --time_path="$TIME_PATH"

      # Metaheuristic refinement
      if [[ "$meta" == "GA" || "$meta" == "ACO" || "$meta" == "SA" ]]; then
        META_OUTPUT_PATH="${META_DIR}/${meta}/output/${SIZE}/${filename}.txt"
        META_TIME_PATH="${META_DIR}/${meta}/runtime/${SIZE}/${filename}.txt"

        mkdir -p "$(dirname "$META_OUTPUT_PATH")"
        mkdir -p "$(dirname "$META_TIME_PATH")"

        case "$meta" in
          GA)
            python3 src/GA.py "$OUTPUT_PATH" "$TEMP_JSON_FILE" "$META_OUTPUT_PATH" "$META_TIME_PATH"
            ;;
          ACO)
            python3 src/ACO.py "$OUTPUT_PATH" "$TEMP_JSON_FILE" "$META_OUTPUT_PATH" "$META_TIME_PATH"
            ;;
          SA)
            python3 src/SA.py "$OUTPUT_PATH" "$TEMP_JSON_FILE" "$META_OUTPUT_PATH" "$META_TIME_PATH"
            ;;
        esac
        echo "✨ Meta ($meta) done -> $META_OUTPUT_PATH"
      fi

      rm "$TEMP_JSON_FILE"
    done
  done
fi

# Stage 2: Evaluation and plot
if [ "$stage" -le 2 ] && [ "$stop_stage" -ge 2 ]; then 
  # Luôn chạy với meta=none
  bash scripts/dist_cal.sh --model $model --meta none
  bash scripts/plot.sh --model $model --meta none

  # Nếu meta khác none, chạy thêm với meta
  if [ "$meta" != "none" ]; then
    bash scripts/dist_cal.sh --model $model --meta $meta
    bash scripts/plot.sh --model $model --meta $meta
  fi
fi
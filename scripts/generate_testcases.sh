#!/bin/bash

NUM_CASE=5
OUT_DIR="test"

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --num_case) NUM_CASE="$2"; shift ;;
    *) echo "❌ Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

get_n() {
  case $1 in
    small) echo 10 ;;
    medium) echo 40 ;;
    large) echo 100 ;;
    *) echo "Unknown size $1" >&2; exit 1 ;;
  esac
}

get_m() {
  case $1 in
    small) echo 20 ;;
    medium) echo 100 ;;
    large) echo 400 ;;
    *) echo "Unknown size $1" >&2; exit 1 ;;
  esac
}

get_max_q() {
  case $1 in
    small) echo 20 ;;
    medium) echo 100 ;;
    large) echo 200 ;;
    *) echo "Unknown size $1" >&2; exit 1 ;;
  esac
}

get_num_visited() {
  case $1 in
    small) echo 6 ;;
    medium) echo 20 ;;
    large) echo 40 ;;
    *) echo "Unknown size $1" >&2; exit 1 ;;
  esac
}

for SIZE in small medium large; do
  echo "🚀 Generating $NUM_CASE test cases for $SIZE ..."

  mkdir -p "$OUT_DIR/input/${SIZE}"
  mkdir -p "$OUT_DIR/eval/${SIZE}"

  SIZE_N=$(get_n $SIZE)
  SIZE_M=$(get_m $SIZE)
  MAX_Q=$(get_max_q $SIZE)
  NUM_VISITED=$(get_num_visited $SIZE)

  echo "DEBUG: SIZE=$SIZE, SIZE_N=$SIZE_N, SIZE_M=$SIZE_M"

  for ((i=1; i<=NUM_CASE; i++)); do
    echo "  🔧 [$SIZE] Test case $i"

    json=$(python3 utils/test_gen.py generate_test_case \
      --N=$SIZE_N \
      --M=$SIZE_M \
      --max_quantity=$MAX_Q \
      --num_visited=$NUM_VISITED)

    json_N=$(echo "$json" | jq '.input.N')
    json_M=$(echo "$json" | jq '.input.M')
    echo "    -> JSON input.N=$json_N, input.M=$json_M (Expected: $SIZE_N, $SIZE_M)"

    {
      echo "$SIZE_N $SIZE_M"
      echo "$json" | jq -r '.input.Q[] | map(tostring) | join(" ")'
      echo "$json" | jq -r '.input.D[] | map(tostring) | join(" ")'
      echo "$json" | jq -r '.input.q | join(" ")'
    } > "$OUT_DIR/input/${SIZE}/${i}.txt"

    {
      echo "$json" | jq -r '.expected_output.d'
      echo "$json" | jq -r '.expected_output.m | join(" ")'
    } > "$OUT_DIR/eval/${SIZE}/${i}.txt"
  done
done

echo "✅ Đã sinh xong $NUM_CASE test case cho mỗi loại vào thư mục ./test"
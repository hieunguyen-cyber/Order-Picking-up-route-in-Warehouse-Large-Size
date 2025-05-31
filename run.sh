#!/bin/bash

stage=-1
stop_stage=-1
MODELS="Local_Search_Two_Opt,Greedy_Local_Search,DP_Greedy_Two_Opt,Greedy,DP_Greedy"

bash path.sh 
# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --stage) stage="$2"; shift ;;
    --stop_stage) stop_stage="$2"; shift ;;
    *) echo "❌ Unknown argument: $1"; exit 1 ;;
  esac
  shift
done

if [ "$stage" -le 1 ] && [ "$stop_stage" -ge 1 ]; then
    bash scripts/Greedy.sh --stage 1 --stop_stage 2
fi

if [ "$stage" -le 2 ] && [ "$stop_stage" -ge 2 ]; then
    bash scripts/DP_Greedy.sh --stage 1 --stop_stage 2
fi

if [ "$stage" -le 3 ] && [ "$stop_stage" -ge 3 ]; then
    bash scripts/DP_Greedy_Two_Opt.sh --stage 1 --stop_stage 2
fi

if [ "$stage" -le 4 ] && [ "$stop_stage" -ge 4 ]; then
    bash scripts/Greedy_Local_Search.sh --stage 1 --stop_stage 2
fi

if [ "$stage" -le 5 ] && [ "$stop_stage" -ge 5 ]; then
    bash scripts/Local_Search_Two_opt.sh --stage 1 --stop_stage 2
fi

if [ "$stage" -le 6 ] && [ "$stop_stage" -ge 6 ]; then
    python utils/plot.py plot_metrics --models="$MODELS"
    python utils/log_csv.py --models="$MODELS"
fi

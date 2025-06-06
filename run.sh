#!/bin/bash

stage=-1
stop_stage=-1
use_meta=false
MODELS="Local_Search_Two_Opt,Greedy_Local_Search,DP_Greedy_Two_Opt,Greedy,DP_Greedy"

bash path.sh 
pip install -r requirements.txt

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --stage) stage="$2"; shift ;;
    --stop_stage) stop_stage="$2"; shift ;;
    --meta) use_meta="$2"; shift ;;
    *) echo "❌ Unknown argument: $1"; exit 1 ;;
  esac
  shift
done

if [ "$stage" -le 1 ] && [ "$stop_stage" -ge 1 ]; then
    bash scripts/generate_testcases.sh --num_case 10
fi

if [ "$stage" -le 2 ] && [ "$stop_stage" -ge 2 ]; then
    bash scripts/Greedy.sh --stage 1 --stop_stage 2
    if [ "$use_meta" == "true" ]; then
        for meta in GA ACO SA; do
            bash scripts/Greedy.sh --stage 1 --stop_stage 2 --meta $meta
        done
        python utils/plot.py compare_meta_vs_base --model Greedy --output_dir result/figure/Greedy
    fi
fi

if [ "$stage" -le 3 ] && [ "$stop_stage" -ge 3 ]; then
    bash scripts/DP_Greedy.sh --stage 1 --stop_stage 2
    if [ "$use_meta" == "true" ]; then
        for meta in GA ACO SA; do
            bash scripts/DP_Greedy.sh --stage 1 --stop_stage 2 --meta $meta
        done
        python utils/plot.py compare_meta_vs_base --model DP_Greedy --output_dir result/figure/DP_Greedy
    fi
fi

if [ "$stage" -le 4 ] && [ "$stop_stage" -ge 4 ]; then
    bash scripts/DP_Greedy_Two_Opt.sh --stage 1 --stop_stage 2
    if [ "$use_meta" == "true" ]; then
        for meta in GA ACO SA; do
            bash scripts/DP_Greedy_Two_Opt.sh --stage 1 --stop_stage 2 --meta $meta
        done
        python utils/plot.py compare_meta_vs_base --model DP_Greedy_Two_Opt --output_dir result/figure/DP_Greedy_Two_Opt
    fi
fi

if [ "$stage" -le 5 ] && [ "$stop_stage" -ge 5 ]; then
    bash scripts/Greedy_Local_Search.sh --stage 1 --stop_stage 2
    if [ "$use_meta" == "true" ]; then
        for meta in GA ACO SA; do
            bash scripts/Greedy_Local_Search.sh --stage 1 --stop_stage 2 --meta $meta
        done
        python utils/plot.py compare_meta_vs_base --model Greedy_Local_Search --output_dir result/figure/Greedy_Local_Search
    fi
fi

if [ "$stage" -le 6 ] && [ "$stop_stage" -ge 6 ]; then
    bash scripts/Local_Search_Two_Opt.sh --stage 1 --stop_stage 2
    if [ "$use_meta" == "true" ]; then
        for meta in GA ACO SA; do
            bash scripts/Local_Search_Two_Opt.sh --stage 1 --stop_stage 2 --meta $meta
        done
        python utils/plot.py compare_meta_vs_base --model Local_Search_Two_Opt --output_dir result/figure/Local_Search_Two_Opt
    fi
fi

if [ "$stage" -le 7 ] && [ "$stop_stage" -ge 7 ]; then
    python utils/plot.py plot_metrics --models "$MODELS"
    python utils/log_csv.py generate_summary --models "$MODELS"
    if [ "$use_meta" == "true" ]; then
        python utils/plot.py compare_meta_across_models --models "$MODELS"
        python3 utils/log_csv.py generate_meta_summary --models "$MODELS"
    fi
fi

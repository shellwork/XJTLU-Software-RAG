#!/bin/bash
echo "[Start]:Step0 prepare team list"
python ./Step0_prepare/split.py
echo "[Complete]:Step0 prepare team list complete"

echo "[Start]: Step1 webspider"
python ./Step1_webspider/complete_webspider.py
echo "[Complete]:Step1 webspider complete"

echo "[Start]: Step2_cleaner"
python ./Step2_cleaner/cleaner.py
echo "[Complete]:Step2 cleaner complete"

echo "[Start]: Step3 transformer"
python ./Step3_transformer/transformer.py
echo "[Complete]:Step3 transformer complete"

echo "[Start]: Step4 generate output"
python ./Step4_generate_output/comb.py
echo "[Complete]:Step4 generate output complete"


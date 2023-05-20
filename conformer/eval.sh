#!/usr/bin/env bash

python speech_to_text_eval.py \
    model_path="/home/user/code/data/models/model_20230516_164600.nemo" \
    pretrained_name="model_first" \
    dataset_manifest="/home/user/code/data/sbb_test/manifest.json" \
    output_filename="out.txt" \
    batch_size=32 \
    amp=True \

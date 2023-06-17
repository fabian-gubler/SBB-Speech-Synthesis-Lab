import random
import json
import os
from datetime import datetime
from pytorch_lightning.callbacks import ModelCheckpoint
import wandb
from pytorch_lightning.loggers import WandbLogger
import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr

val_manifest_path = "./output/val_manifest.json"
test_manifest_path = "./output/test_manifest.json"
project_name = "conformer_test"

def load_manifests(train_manifest_path, val_manifest_path, test_manifest_path):
    train_manifest = []
    val_manifest = []
    test_manifest = []

    with open(train_manifest_path) as f:
        train_manifest = [json.loads(line) for line in f]

    with open(val_manifest_path) as f:
        val_manifest = [json.loads(line) for line in f]

    with open(test_manifest_path) as f:
        test_manifest = [json.loads(line) for line in f]

    return train_manifest, val_manifest, test_manifest


def sweep_iteration(train_manifest_path, synthetic_data_increment):
    if 'german' in train_manifest_path:
        run_name = f'conformer_german_{synthetic_data_increment * 10}'
    else:
        run_name = f'conformer_{synthetic_data_increment * 10}'

    wandb.init(project=project_name, name=run_name, reinit=True)
    wandb_logger = WandbLogger(log_model='all')

    checkpoint_callback = ModelCheckpoint(monitor='val_wer', mode='min')

    trainer = pl.Trainer(max_epochs=10, logger=wandb_logger, callbacks=[checkpoint_callback], gpus=[2], accelerator="gpu")

    model = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_de_conformer_ctc_large")

    min_wer = float('inf')

    model.cfg.train_ds.manifest_filepath = train_manifest_path
    model.cfg.validation_ds.manifest_filepath = val_manifest_path
    model.cfg.test_ds.manifest_filepath = test_manifest_path
    model.cfg.train_ds.is_tarred = False

    model.cfg.train_ds.batch_size = 32
    model.cfg.validation_ds.batch_size = 32
    model.cfg.test_ds.batch_size = 32

    model.setup_training_data(model.cfg.train_ds)
    model.setup_validation_data(model.cfg.validation_ds)
    model.setup_test_data(model.cfg.test_ds)

    trainer.fit(model)
    test_result = trainer.test(model)

    # Get the test word error rate
    test_wer = test_result[0]['test_wer']

    # Check if the current iteration has a lower word error rate
    if test_wer < min_wer:
        min_wer = test_wer

    # Save the minimum word error rate to a text file
    result_file = f"results/{project_name}_iteration_{synthetic_data_increment}.txt"
    with open(result_file, 'w') as f:
        f.write(f"Minimum Word Error Rate: {min_wer}")

    model_path = f"models/model_{run_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

# for i in range(0, 11):
for i in range(0, 1):
    train_manifest_path = f"./output/train_manifest_{i}.json"
    sweep_iteration(train_manifest_path, i)

# for i in range(0, 11):
#     synthetic_train_manifest_path = f"synthetic_german_train_manifest_{i}.json"
#     train_manifest = baseline_train_manifest + load_manifests(synthetic_train_manifest_path, [], [])[0]
#     with open("train_manifest.json", "w") as f:
#         for entry in train_manifest:
#             f.write(json.dumps(entry))
#             f.write('\n')
#     sweep_iteration(german_synthetic_manifest_path, i)

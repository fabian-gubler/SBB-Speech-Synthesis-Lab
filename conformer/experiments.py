import random
import json
import os
from datetime import datetime
from pytorch_lightning.callbacks import ModelCheckpoint
import wandb
from pytorch_lightning.loggers import WandbLogger
import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

val_manifest_path = "../sbb/conformer/output/val_manifest.json"
test_manifest_path = "../sbb/conformer/output/test_manifest.json"
project_name = "conformer_final_04"

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

    checkpoint_callback = ModelCheckpoint(
        monitor='val_loss',
        mode='min',
        dirpath='./checkpoints',
        filename=f'{run_name}' + '-{epoch:02d}-{val_loss:.2f}',
        save_top_k=1,
        save_last=True,
        verbose=True
    )

    early_stopping_callback = EarlyStopping(
        monitor='val_wer',
        mode='min',
        patience=2  # Number of epochs with no improvement after which training will be stopped
    )

    trainer = pl.Trainer(
        max_epochs=6,
        logger=wandb_logger,
        callbacks=[checkpoint_callback, early_stopping_callback],
        gpus=[2],
        accelerator="gpu"
    )

    model = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_de_conformer_ctc_large")

    min_wer = float('inf')

    model.cfg.train_ds.manifest_filepath = train_manifest_path
    model.cfg.validation_ds.manifest_filepath = val_manifest_path
    model.cfg.test_ds.manifest_filepath = test_manifest_path
    model.cfg.train_ds.is_tarred = False

    model.cfg.train_ds.batch_size = 16
    model.cfg.validation_ds.batch_size = 16
    model.cfg.test_ds.batch_size = 16
    model.cfg.train_ds.shuffle = True

    model.setup_training_data(model.cfg.train_ds)

    model.setup_validation_data(model.cfg.validation_ds)
    model.setup_test_data(model.cfg.test_ds)

    trainer.fit(model)
    trainer.test(model)

    model_path = f"models/{project_name}_model_{run_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

# Baseline without synthetic data
train_manifest_path = f"../sbb/conformer/output/train_manifest_0.json"
sweep_iteration(train_manifest_path, 0)

# Sweep over synthetic data for german
for i in range(1, 11):
    train_manifest_path = f"../sbb/conformer/output/train_manifest_german_{i}.json"
    sweep_iteration(train_manifest_path, i)

# Sweep over synthetic data
for i in range(1, 11):
    train_manifest_path = f"../sbb/conformer/output/train_manifest_{i}.json"
    sweep_iteration(train_manifest_path, i)


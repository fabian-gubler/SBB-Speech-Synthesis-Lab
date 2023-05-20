import nemo.collections.asr as nemo_asr

# model = nemo_asr.models.ASRModel.from_pretrained(model_name='stt_de_conformer_ctc_large')
model = nemo_asr.models.ASRModel.from_pretrained(
    model_name="stt_de_conformer_ctc_large"
)
model.cfg

# use all available samples for training
train_manifest = "/home/user/code/data/dataset_train/manifest.json"
eval_manifest = "/home/user/code/data/dataset_eval/manifest.json"

# only use german samples for training
# train_manifest = "../data/dataset_train/manifest_german.json"
# eval_manifest = "../data/dataset_eval/manifest_german.json"

test_manifest = "/home/user/code/data/sbb_test/manifest.json"

# default libraries
import copy
import datetime
import functools
from datetime import datetime
from pathlib import Path

import pytorch_lightning as pl
import torch
import wandb
from nemo.core.config import hydra_runner
from nemo.utils import logging
from nemo.utils.exp_manager import exp_manager
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.loggers import WandbLogger
from ruamel.yaml import YAML

# additional libraries - might need to implement myself
import jiwer


def sweep_iteration():
    trainer = pl.Trainer(max_epochs=10)

    # set up W&B logger
    wandb.init()    # required to have access to `wandb.config`
    wandb_logger = WandbLogger(log_model='all')  # log final model

    trainer = pl.Trainer(max_epochs=10, logger=wandb_logger, devices = [2], accelerator="gpu")

    # setup model 
    model = nemo_asr.models.ASRModel.from_pretrained(
        model_name="stt_de_conformer_ctc_large"
    )

    # trainer setup
    model.set_trainer(trainer)

    model.cfg.train_ds.is_tarred = False

    model.cfg.train_ds.manifest_filepath = train_manifest
    model.cfg.validation_ds.manifest_filepath = eval_manifest
    model.cfg.test_ds.manifest_filepath = test_manifest

    model.cfg.train_ds.max_duration = 45
    model.cfg.train_ds.batch_size = 8
    model.cfg.validation_ds.batch_size = 8
    model.cfg.test_ds.batch_size = 8

    model.setup_training_data(model.cfg.train_ds)
    model.setup_validation_data(model.cfg.validation_ds)
    model.setup_test_data(model.cfg.test_ds)
    model.setup_optimization(model.cfg.optim)

    # train
    trainer.fit(model)

    # create the models directory if it doesn't exist
    Path("models").mkdir(parents=True, exist_ok=True)

    # save model
    model_path = f"models/model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

# # other groups performed hyperparameter sweep
# sweep_id = wandb.sweep(sweep_config, project="ASR-Conformer-CTC")
# wandb.agent(sweep_id, function=sweep_iteration)


train_manifest = "/home/user/code/data/dataset_train/manifest.json"
eval_manifest = "/home/user/code/data/dataset_eval/manifest.json"
test_manifest = "/home/user/code/data/sbb_test/manifest.json"

sweep_iteration()

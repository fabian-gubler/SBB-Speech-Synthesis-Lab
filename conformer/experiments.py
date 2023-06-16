import random
import json
import os
from datetime import datetime
from pytorch_lightning.callbacks import ModelCheckpoint
import wandb
from pytorch_lightning.loggers import WandbLogger
import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr

SEED = 1337
train_percent = 0.7
val_percent = 0.15

human_manifest_path = '/home/user/code/data/dataset/human/manifest.json'
synthetic_manifest_path = '/home/user/code/data/dataset/synthetic/manifest.json'
german_synthetic_manifest_path = '/home/user/code/data/dataset/synthetic/manifest_german.json'

def baseline_iteration():
    # Create experiment name
    run_name = 'conformer_baseline'

    # Initiate W&B logger
    wandb.init(project='conformer_baseline', name=run_name, id=run_name)  # Set unique ID for the run
    wandb_logger = WandbLogger(log_model='all')

    # Load human data
    with open(human_manifest_path) as f:
        human_data = [json.loads(line) for line in f]

    random.seed(SEED)  # ensure consistent shuffling
    random.shuffle(human_data)

    # Consider all human data as test data for 0-shot baseline
    test_manifest_path = "temp_test_manifest.json"
    with open(test_manifest_path, 'w') as outfile:
        for entry in human_data:
            json.dump(entry, outfile)
            outfile.write('\n')

    # Prepare model
    trainer = pl.Trainer(logger=wandb_logger, gpus=[2], accelerator="gpu")
    model = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_de_conformer_ctc_large")
    model.set_trainer(trainer)

    model.cfg.test_ds.manifest_filepath = test_manifest_path
    model.cfg.test_ds.batch_size = 8

    model.setup_test_data(model.cfg.test_ds)

    # Test the model
    trainer.test(model)

    # Save model
    model_path = f"models/baseline_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

    # Clean up the temporary test manifest file
    if os.path.exists(test_manifest_path):
        os.remove(test_manifest_path)

def sweep_iteration(synthetic_manifest, synthetic_data_increment):
    if 'german' in synthetic_manifest:
        run_name = f'conformer_german_{synthetic_data_increment * 10}'
    else:
        run_name = f'conformer_{synthetic_data_increment * 10}'

    wandb.init(project='conformer_11', name=run_name, id=run_name)  # Set unique ID for the run
    wandb_logger = WandbLogger(log_model='all')

    checkpoint_callback = ModelCheckpoint(monitor='val_wer', mode='min')

    trainer = pl.Trainer(max_epochs=10, logger=wandb_logger, callbacks=[checkpoint_callback], gpus=[2], accelerator="gpu")

    model = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_de_conformer_ctc_large")

    with open(human_manifest_path) as f:
        human_data = [json.loads(line) for line in f]

    with open(synthetic_manifest) as f:
        synthetic_data = [json.loads(line) for line in f]

    random.seed(SEED)
    random.shuffle(human_data)
    # random.shuffle(synthetic_data)

    train_split = int(0.7 * len(human_data))
    val_split = int(0.85 * len(human_data))

    train_manifest = human_data[:train_split] + synthetic_data[:synthetic_data_increment * len(synthetic_data)]
    val_manifest = human_data[train_split:val_split]
    test_manifest = human_data[val_split:]

    # save each manifest to a json file
    def write_to_file(data, path):
        with open(path, 'w') as outfile:
            for entry in data:
                json.dump(entry, outfile)
                outfile.write('\n')

    train_manifest_path = "train_manifest.json"
    val_manifest_path = "val_manifest.json"
    test_manifest_path = "test_manifest.json"

    min_wer = float('inf')

    write_to_file(train_manifest, train_manifest_path)
    write_to_file(val_manifest, val_manifest_path)
    write_to_file(test_manifest, test_manifest_path)

    model.cfg.train_ds.manifest_filepath = train_manifest_path
    model.cfg.validation_ds.manifest_filepath = val_manifest_path
    model.cfg.test_ds.manifest_filepath = test_manifest_path
    model.cfg.train_ds.is_tarred = False

    model.cfg.train_ds.batch_size = 8
    model.cfg.validation_ds.batch_size = 8
    model.cfg.test_ds.batch_size = 8

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
    result_file = f"results/iteration_{synthetic_data_increment}.txt"
    with open(result_file, 'w') as f:
        f.write(f"Minimum Word Error Rate: {min_wer}")

    model_path = f"models/model_{run_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

    # Clean up temporary manifest files
    if os.path.exists(train_manifest_path):
        os.remove(train_manifest_path)
    if os.path.exists(val_manifest_path):
        os.remove(val_manifest_path)
    if os.path.exists(test_manifest_path):
        os.remove(test_manifest_path)

# baseline_iteration()

for i in range(0, 11):
    sweep_iteration(synthetic_manifest_path, i)

for i in range(0, 11):
    sweep_iteration(german_synthetic_manifest_path, i)

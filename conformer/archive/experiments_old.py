import random
import json
import os
from datetime import datetime
from pytorch_lightning.callbacks import ModelCheckpoint
import wandb
from pytorch_lightning.loggers import WandbLogger
import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr

# This is your random seed for reproducibility.
# You can set it to any integer you like.
SEED = 1337
train_percent = 0.7
val_percent = 0.15


# Define paths to manifest files
human_manifest_path = '/home/user/code/data/dataset/human/manifest.json'
synthetic_manifest_path = '/home/user/code/data/dataset/synthetic/manifest.json'
german_synthetic_manifest_path = '/home/user/code/data/dataset/synthetic/manifest_german.json'

def data_split(data, train_percent, val_percent):
    total_samples = len(data)
    train_samples = int(total_samples * train_percent)
    val_samples = int(total_samples * val_percent)
    
    train_data = data[:train_samples]
    val_data = data[train_samples:train_samples + val_samples]
    test_data = data[train_samples + val_samples:]
    
    return train_data, val_data, test_data

# Define the baseline iteration, where the model is tested without any training
def baseline_iteration():
    # Create experiment name
    run_name = 'conformer_baseline'

    # Initiate W&B logger
    wandb.init(project='conformer_sweeps', name=run_name)
    wandb_logger = WandbLogger(log_model='all')

    # Load human data and create splits
    with open(human_manifest_path) as f:
        human_data = [json.loads(line) for line in f]

    random.seed(SEED)  # ensure consistent shuffling
    random.shuffle(human_data)

    human_train, human_val, human_test = data_split(human_data, train_percent, val_percent)

    # Write test manifest
    test_manifest_path = "temp_test_manifest.json"
    with open(test_manifest_path, 'w') as outfile:
        for entry in human_test:
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

# Define the sweep iteration, where the model is trained and tested with different proportions of synthetic data
def sweep_iteration(synthetic_manifest, synthetic_data_increment):
    # Create experiment name based on synthetic_data_increment
    run_name = f'conformer_{synthetic_data_increment * 10}'

    # Set up W&B logger with the experiment name
    wandb.init(project='conformer_04', name=run_name)    
    wandb_logger = WandbLogger(log_model='all')

    # Set up model checkpointing to save the model with the lowest validation word error rate
    checkpoint_callback = ModelCheckpoint(monitor='val_loss')

    # Set up trainer with the logger and the checkpoint callback
    trainer = pl.Trainer(max_epochs=10, logger=wandb_logger, callbacks=[checkpoint_callback], gpus=[2], accelerator="gpu")

    # Load pre-trained model
    model = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_de_conformer_ctc_large")

    # Load manifest files and create splits
    with open(human_manifest_path) as f:
        human_data = [json.loads(line) for line in f]

    with open(synthetic_manifest) as f:
        synthetic_data = [json.loads(line) for line in f]

    # Shuffle data (using a fixed seed for reproducibility)
    random.seed(SEED)
    random.shuffle(human_data)
    random.shuffle(synthetic_data)

    # Split the human data into training, validation, and test sets
    train_split = int(0.7 * len(human_data))
    val_split = int(0.85 * len(human_data))

    # Create the manifests for the current iteration, including the synthetic data in the training set
    train_manifest = human_data[:train_split] + synthetic_data[:synthetic_data_increment * len(synthetic_data)]
    val_manifest = human_data[train_split:val_split]
    test_manifest = human_data[val_split:]

    # Setup data for the model
    model.cfg.train_ds.manifest_filepath = train_manifest
    model.cfg.validation_ds.manifest_filepath = val_manifest
    model.cfg.test_ds.manifest_filepath = test_manifest

    model.cfg.train_ds.batch_size = 8
    model.cfg.validation_ds.batch_size = 8
    model.cfg.test_ds.batch_size = 8

    model.setup_training_data(model.cfg.train_ds)
    model.setup_validation_data(model.cfg.validation_ds)
    model.setup_test_data(model.cfg.test_ds)

    # Train and test the model
    trainer.fit(model)
    trainer.test(model)

    # Save model
    model_path = f"models/model_{run_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

# Run the baseline experiment
baseline_iteration()

# Run the experiments with synthetic data increments, starting from 0% (human data only)
for i in range(0, 11):  # 0% to 100% increments
    sweep_iteration(synthetic_manifest_path, i)

# Run the experiments with German-accented synthetic data increments, starting from 0% (human data only)
for i in range(0, 11):  # 0% to 100% increments
    sweep_iteration(german_synthetic_manifest_path, i)

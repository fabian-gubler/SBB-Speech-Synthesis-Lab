import random
import json
from datetime import datetime
from pytorch_lightning.callbacks import ModelCheckpoint
import wandb
from pytorch_lightning.loggers import WandbLogger
import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr

# This is your random seed for reproducibility.
# You can set it to any integer you like.
SEED = 1337

# Define paths to manifest files
human_manifest_path = '/path/to/human_manifest.jsonl'  # replace with your actual path
synthetic_manifest_path = '/path/to/synthetic_manifest.jsonl'  # replace with your actual path
german_synthetic_manifest_path = '/path/to/german_synthetic_manifest.jsonl'  # replace with your actual path

# Define the baseline iteration, where no training is performed and the pretrained model is tested
def baseline_iteration():
    # Create experiment name
    run_name = 'conformer_baseline'

    # Set up W&B logger with the experiment name
    wandb.init(project='conformer_03', name=run_name)    
    wandb_logger = WandbLogger(log_model='all')

    # Set up trainer with the logger. No callbacks are needed since we're not training
    trainer = pl.Trainer(logger=wandb_logger, gpus=[2], accelerator="gpu")

    # Load pre-trained model and setup test data
    model = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_de_conformer_ctc_large")

    model.cfg.test_ds.manifest_filepath = test_manifest
    model.cfg.test_ds.batch_size = 8

    model.setup_test_data(model.cfg.test_ds)

    # Test the model (no training is performed)
    trainer.test(model)

# Define the sweep iteration, where the model is trained and tested with different proportions of synthetic data
def sweep_iteration(synthetic_manifest, synthetic_data_increment):
    # Create experiment name based on synthetic_data_increment
    run_name = f'conformer_{synthetic_data_increment * 10}'

    # Set up W&B logger with the experiment name
    wandb.init(project='conformer_03', name=run_name)    
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

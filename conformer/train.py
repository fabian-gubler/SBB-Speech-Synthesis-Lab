import jiwer
import nemo.collections.asr as nemo_asr
import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger
import wandb
from pathlib import Path
from datetime import datetime

def compute_metrics(hypotheses, references):
    # Compute metrics
    wer = jiwer.wer(references, hypotheses)
    ser = jiwer.sentence_error_rate(references, hypotheses)
    cer = jiwer.character_error_rate(references, hypotheses)

    return wer, ser, cer

# Update your model class to include these metrics during validation/test
# class MyASRModel(nemo_asr.models.ASRModel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def validation_step(self, batch, batch_idx):
#         # perform the default validation step
#         val_loss = super().validation_step(batch, batch_idx)
#
#         # compute metrics
#         references, hypotheses = self.transcribe(batch)
#         wer, ser, cer = compute_metrics(hypotheses, references)
#
#         # log metrics
#         self.log('val_wer', wer, on_step=True, on_epoch=True, prog_bar=True, logger=True)
#         self.log('val_ser', ser, on_step=True, on_epoch=True, prog_bar=True, logger=True)
#         self.log('val_cer', cer, on_step=True, on_epoch=True, prog_bar=True, logger=True)
#         
#         return val_loss
#
#     def test_step(self, batch, batch_idx):
#         # perform the default test step
#         test_loss = super().test_step(batch, batch_idx)
#
#         # compute metrics
#         references, hypotheses = self.transcribe(batch)
#         wer, ser, cer = compute_metrics(hypotheses, references)
#
#         # log metrics
#         self.log('test_wer', wer, on_step=True, on_epoch=True, prog_bar=True, logger=True)
#         self.log('test_ser', ser, on_step=True, on_epoch=True, prog_bar=True, logger=True)
#         self.log('test_cer', cer, on_step=True, on_epoch=True, prog_bar=True, logger=True)
#         
#         return test_loss

def sweep_iteration():
    # set up W&B logger
    wandb.init(project='conformer')    # replace with your actual project name
    wandb_logger = WandbLogger(log_model='all')  # log final model

    trainer = pl.Trainer(max_epochs=10, logger=wandb_logger, gpus=[2], accelerator="gpu")

    # setup model
    # model = MyASRModel.from_pretrained(
    #     model_name="stt_de_conformer_ctc_large"
    # )


    model = nemo_asr.models.ASRModel.from_pretrained(
        model_name="stt_de_conformer_ctc_large"
    )

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
    # test
    trainer.test(model)

    # create the models directory if it doesn't exist
    Path("models").mkdir(parents=True, exist_ok=True)

    # save model
    model_path = f"models/model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nemo"
    model.save_to(model_path)

# use all available samples for training
train_manifest = "/home/user/code/data/dataset_train/manifest.json"
test_manifest = "/home/user/code/data/external/sbb_test/manifest.json"
eval_manifest = "/home/user/code/data/dataset_eval/manifest.json"

sweep_iteration()

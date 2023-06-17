import torch
import nemo.collections.asr as nemo_asr

model_path = "./models/model.nemo"
model = nemo_asr.models.ASRModel.restore_from(model_path)

model.eval()

train_manifest_path = "./output/test_manifest.json"
with open(train_manifest_path, 'r') as f:
    train_manifest = [json.loads(line) for line in f]

for sample in train_manifest:
    audio_filepath = sample['audio_filepath']
    transcription = sample['text']

    # Perform inference
    audio_signal, _ = nemo_asr.AudioReader()(audio_filepath)
    transcript = model.transcribe([audio_signal])

    print("Ground Truth:", transcription)
    print("Prediction:", transcript[0])
    print()


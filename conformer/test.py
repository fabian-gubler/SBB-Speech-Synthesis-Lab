import nemo.collections.asr as nemo_asr

# Load the saved model
model_path = "models/model_20230521_090543.nemo"  # replace with the actual path of your saved model
model = nemo_asr.models.ASRModel.restore_from(model_path)

# Specify the path to the audio file you want to transcribe
audio_file = "sbb_test/Audios/0000ecac-d8aa-4653-9a75-8e9a9c47e77f.wav"  # replace with your actual audio file path

# Use the transcribe method to get the transcription
transcription = model.transcribe(paths2audio_files=[audio_file])
print(transcription)

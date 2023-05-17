import nemo.collections.asr as nemo_asr
import jiwer
import torch
from torch.utils.data import Dataset, DataLoader

# Load the model
model = nemo_asr.models.EncDecCTCModel.restore_from("/home/user/code/data/models/model_20230516_164600.nemo")

# Define the data layer
data_layer = nemo_asr.AudioToTextDataLayer(
    manifest_filepath='/home/user/code/data/sbb_test/manifest.json',
    labels=model.decoder.vocabulary,  # assuming `model` is your loaded model
    batch_size=32,  # adjust as needed
    sample_rate=16000,  # adjust as needed
    num_workers=4,  # adjust as needed
)

# Get the data loader from the data layer
data_loader = data_layer.data_iterator


def compute_accuracy(predictions, targets):
    correct = 0
    total = 0

    for prediction, target in zip(predictions, targets):
        # Splitting sentences into words
        prediction_words = prediction.split(' ')
        target_words = target.split(' ')

        # Check that lengths match
        if len(prediction_words) != len(target_words):
            continue

        # Counting correct words
        for pred_word, target_word in zip(prediction_words, target_words):
            if pred_word == target_word:
                correct += 1

        total += len(target_words)

    # Returning accuracy (or 0 if no words were processed)
    return correct / total if total > 0 else 0


def compute_wer(predictions, targets):
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.SentencesToListOfWords(),
        jiwer.RemovePunctuation(),
    ])

    wer = jiwer.wer(
        targets, 
        predictions, 
        truth_transform=transformation, 
        hypothesis_transform=transformation
    )

    return wer


# Assuming you have a DataLoader `data_loader` for your test data
# and a function `compute_accuracy` that computes accuracy given model's outputs and targets
model.eval()
with torch.no_grad():
    total_accuracy = 0
    num_samples = 0
    for batch in data_loader:
        audio_signal, audio_signal_len, transcript, transcript_len = batch
        log_probs, encoded_len, greedy_predictions = model(
            input_signal=audio_signal, input_signal_length=audio_signal_len
        )
        accuracy = compute_accuracy(greedy_predictions, transcript)
        # accuracy = compute_wer(greedy_predictions, transcript)
        total_accuracy += accuracy * audio_signal.size(0)
        num_samples += audio_signal.size(0)

    print(f"Test accuracy: {total_accuracy / num_samples}")

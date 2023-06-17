import json
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import nemo.collections.asr as nemo_asr
import jiwer

def load_model(model_path):
    # Load the trained ASR model from the NEMO file
    model = nemo_asr.models.EncDecCTCModelBPE.restore_from(model_path)
    return model

def evaluate(model, manifest_path, save_path=None):
    # Load the manifest file
    with open(manifest_path) as f:
        manifest = [json.loads(line) for line in f]

    references = []
    predictions = []

    for entry in manifest:
        audio_path = entry['audio_filepath']
        reference = entry['text']

        # Perform speech-to-text prediction
        predicted_text = model.transcribe([audio_path])[0]

        references.append(reference)
        predictions.append(predicted_text)

    # Calculate evaluation metrics
    wer = jiwer.wer(references, predictions)
    cer = jiwer.cer(references, predictions)
    ser = jiwer.ser(references, predictions)
    # word_accuracy = model.calc_word_errors(hypotheses=predictions, references=references, use_cer=False)

    # Print the evaluation results
    print(f"Word Error Rate (WER): {wer}")
    print(f"Character Error Rate (CER): {cer}")
    print(f"Sentence Error Rate (SER): {ser}")
    # print(f"Word-level Accuracy: {word_accuracy}")

    # Create a confusion matrix
    labels = sorted(list(set(references)))
    cm = confusion_matrix(references, predictions, labels=labels)

    # Plot the confusion matrix
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()

    # Save the plot as a PNG file if save_path is provided
    if save_path:
        plt.savefig(save_path)

    plt.show()

if __name__ == '__main__':
    # Define the paths to the model and manifest file
    model_path = './models/model_conformer_0_20230616_134433.nemo'
    manifest_path = './output/test_manifest.json'
    save_path = 'confusion_matrix.png'

    # Load the model
    model = load_model(model_path)

    # Evaluate the model and save the confusion matrix plot
    evaluate(model, manifest_path, save_path)

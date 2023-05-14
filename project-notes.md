# Notes SBB

## TODO

### DGX
1. Have data directory (relative link conformer to datadir)
2. Git clone repository
3. SCP to DGX -> unzip
4. Run model

### Data

Samples

- Gleis -> gleis
- x-ray -> xray

Testset

- convert current testset into manifest.json format
- test the model accuracy

### Training

German Training

- manipulate json to only have german entries
- load german manifest-de.json file and train model


Open Issues
- Having only a bag of words to test accuracy 
	? build-in into conformer or having to do this manually?

## Quicklinks

### AZURE Speech Services
- [Voice Gallery](https://speech.microsoft.com/portal/voicegallery)
- [Azure Samples](https://github.com/Azure-Samples/Cognitive-Speech-TTS)
- [T2S Overview](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech)
	- [T2S Coding Quickstart](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?pivots=programming-language-python&tabs=linux%2Cterminal)
	- [Fine-tune with SSML](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup)
	- [Speech from File](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-speech-synthesis?tabs=browserjs%2Cterminal&pivots=programming-language-python)

## Improve Set
- Add different pronounciations (e.g. zwo)
- Add background noise
- Foreign better at slow rate
- Filter foreign understandable voices

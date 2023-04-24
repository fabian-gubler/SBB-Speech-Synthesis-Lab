# Notes SBB

## Quicklinks

### Fliki
- [API Overview](https://fliki.ai/resources/api)
- [API Documentation](https://github.com/fliki-ai/documentation)

### AZURE Speech Services
- [Voice Gallery](https://speech.microsoft.com/portal/voicegallery)
- [Azure Samples](https://github.com/Azure-Samples/Cognitive-Speech-TTS)
- [T2S Overview](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech)
	- [T2S Coding Quickstart](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?pivots=programming-language-python&tabs=linux%2Cterminal)
	- [Fine-tune with SSML](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup)
	- [Speech from File](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-speech-synthesis?tabs=browserjs%2Cterminal&pivots=programming-language-python)

## Blockers
- Check prerequisites for samples for 2 Models
- @Tuesday Find out Presentation Guidelines / Project report for Note-taking & Preparation

## Current Tasks
- Introduce variations 
	- SSML fields + Noise
- Produce Text inputs

## TODOs

Architecture
- Fields in csv
- Files
	- Main File
		- Setup constants (file paths, output directory, amount, split etc.)
		- Handle creating access tokens, what to do upon failure
		- Handle entire process
	- Data Generator (Random Text, Parameters)
		- Should result in same output (change random seed)
		- Should be able to modify distribution based on output size
	- CSV (contains all fields)
	- Data Synthesizer (Creates Requests)

Manifest
- Randomization of parameters (with randomseed)
- Randomization of text, pauses
- Understand
	- Struktur (Rangierfahrt, Umstell)

Python file
- Load csv (e.g. as pandas df)
- Authorization
- Requests based on csv
- Save outputs in directory

## Strategy
Use ChatGPT to code / improve / guide

1. Create Prototype Murf Program
2. Data Generator file

Status Quo
- 3000 Samples classifiaction (verständlich / nicht verständlich)
- PPT guide on text
- Zero-Shot: 38% Fehlerarbeit

Selecting Geneartors
	- [Google T2S](https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3#0)
	- [Fliki](https://github.com/fliki-ai/documentation)
	- [Azure](https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/)

Fliki
- Must have a variety of pronunciations and accents
- Must have API to automate creation

Best Selection: Murph
- 120+ voices (20+ languages)
- Different Profiles (Terrified, Angry etc.)
- Pauses
- Pitch & Speed Setting
- 7 German Voices
- Extensive API Documentation & Features
- 39$ for 4 hours

Azure
- 15 German Voices
- Cheapest Option: estimated 10$ for 10K samples
- Most robust and extensible option for future projects

Input
- Variation in position, Wörter dazu und auslassen
- Zahlen einzeln ausgesprochen, (Zwo)

Training Set: 10'000 Samples (30% Variationen Wort, 30% Variationen Stimmen, 40% Slangs)
- (Automate) Randomisieren, verschiedene Sätze (-> für Stimmen, Slang)
- Must have variety to avoid overfitting
- (Automate) Good labeling (.csv) -> Stimmenart

Misc
- Gion (1. Mai) 1 Woche in Ferien

## Resources

- Pitch, Pronunciation etc. adjustements
- [Docker](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-container-howto?tabs=stt%2Ccsharp%2Csimple-format)
- Reproducible

## Outlook
- Fine-tune / Improve existing Models
- Productionalize the Models (e.g. Containerize, MlOps)
- Make it work on embedded Devices

## Presentation
- Learnings: Good to be true
	- Great for experimentation, falls down pretty fast for scalable entreprise
	  applications
	- Limited API access or none
	- Becomes very Costly for scalable projects (> 10K samples )

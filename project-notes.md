# Notes SBB

## Quicklinks
- [Murf API Documentation](https://murf.ai/api/docs/)

## Blockers
- Check prerequisites for samples for 2 Models
- Find out estimated length of synthesized samples

- @Tuesday Find out Presentation Guidelines / Project report for Note-taking & Preparation

## TODOs

General
- Create private git repo

Architecture
- Calculate expected # hours
- Fields in csv
- Files
	- Data Generator (Random Text, Parameters)
		- Should result in same output (change random seed)
		- Should be able to modify distribution based on output size
	- CSV (contains all fields)
	- Data Synthesizer (Creates Requests)

Manifest
- Randomization of parameters (with randomseed)
- Randomization of text, pauses

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
- Current: Murph, Azure, Fixit
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

[Azure](https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/)
- Pitch, Pronunciation etc. adjustements
- [Docker](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-container-howto?tabs=stt%2Ccsharp%2Csimple-format)
- Reproducible

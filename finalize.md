# Final Meeting

## General

- Submission: 19.06. 10.00 (incl. code & data)
- Strictly 8-12 Pages (No appendix)
	- Declaration on page 13
- IMRAD Structure

## Experiments

### TODO
- Create new SBB data set
- Ask ChatGPT to create
	0. Context
		- Provide Directory Structure
	1. Inference Script
		Conformer 0-Shot baseline training
	2. Batch Script for Experiments with different amounts
		Split:
		- Training set: 70% Human
		- Validation set: 15% Human
		- Test set: 15% Human
		Notes:
		- Name models according to experiment
		- Save model with lowest validation word error rate
		- Save results in wandb
		- Ensure shuffling of human recorded
	3. Run Experiments
		Increments:
		0% - 100% Synthetic Data (10% Increments)

### Important Notes
- Test loss !~ validation loss

## Report Writing

Contents

- Introduction (1) - Phil
- Method (2) - Fabian (Phil Conformer-CTC 1 site)
- Results (2) - Fabian
- Discussion (1) - Phil

Preparation

1. Adapt Metadata
2. Insert Phil Content into template
3. Insert Declaration of Authorship
4. Invite Phil to Overleaf

Ideation

- Think about what I want to write

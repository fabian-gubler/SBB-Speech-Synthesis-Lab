# Methodology
    Detail the process of creating the synthetic dataset:
        Describe the code used, including specific libraries and the reason for their selection.
        Explain the text-to-speech conversion process.
        Discuss how different accents were incorporated into the dataset.
    Explain how the Conformer-CTC model was chosen and how it was trained.
    Insights: Discuss any issues encountered during the dataset creation or model training and how they were resolved.
    Graphic/Table: Include a flowchart of the process, from creating synthetic data to training and testing the model.
    Questions: Were there any specific choices made regarding the text-to-speech process to better emulate real-world conditions? How was the training of the Conformer-CTC model set up?



---
Thank you for providing the initial draft of the methodology section. Followingly I will
answer your questions to develop the final version of this section.

# Questions - Commandos Generation:
1. Could you provide a code snippet or a more detailed explanation of how the randomness was introduced in the commando generation?
ANSWER: 
	def generate_random_part():
		# ...
		letter_prob = random.random()
		if letter_prob < 0.5:
			letter = random.choice(ascii_lowercase)
			nato_letter = nato_alphabet[letter]
			number = random.randint(1, 9)
			return f"{nato_letter} {german_numbers[str(number)]}"
		elif letter_prob < 0.75:
			letter = random.choice(ascii_lowercase)
			nato_letter = nato_alphabet[letter]
			number = random.randint(10, 99)
			digits = [german_numbers[d] for d in str(number)]
			return f"{nato_letter} {' '.join(digits)}"
		else:
			number = random.randint(1, 999)
			digits = [german_numbers[d] for d in str(number)]
			return ' '.join(digits)
		# ...

	def generate_commandos(n):
		# ...
	        via_part = ""
        if random.random() < 0.5:
            via_part = " via " + generate_random_part()
            while via_part == from_part or via_part == to_part:
                via_part = " via " + generate_random_part()

        # randomize vocabulary
        gleis = "gleis" if random.random() < 0.5 else ""
        operation = random.choice(["rangierfahrt", "umstellmanöver"])
        preposition1 = random.choices(["von", "vom"], weights=[0.7, 0.3], k=1)[0]
        preposition2 = random.choices(["nach", "ins"], weights=[0.8, 0.2], k=1)[0]

        # vom / ins
        commando = f"{operation} {preposition1} {gleis} {from_part} {via_part} {preposition2} {gleis} {to_part}"
        commando_nato_breaks_emphasis = add_breaks_and_emphasis(commando)
        commandos.append({"raw": commando, "breaks_emphasis": commando_nato_breaks_emphasis})
		# ...


2. Were there any specific constraints or rules you followed when generating the commandos?
ANSWER:
SBB (Project Client) has given us these constraints, which are followed by the personnell.
One interesting choice has been using "zwo" instead of "zwei", with which they received
better results. Some choices, such as the probabilities of "gleis" or words like "vom"
have been done by ourselves, but had been checked by our sbb supervisor, which told us
that these selections make sense.

# Questions - Speech Generation:
1. Could you share the code used to set up the Azure SDK for speech generation?
ANSWER:

The code has been shared in our previous discussion in the provided chunks

2. How were the specific values for the parameters like "male_to_female" and "language_distribution" decided?
ANSWER:

male to female has been proposed by our supervisor. the work force is primarily male.
languages used has been inspired by the swiss population (german, french and italian
distribution) other accents have been added either as they are typical foreign accents in
switzerland or the accents deemed useful in generalizing typical accents that could be
hard to pick up by the model.

# Questions - Training Set Creation

1. Could you provide an example of a line from the manifest.json file?
ANSWER:

{"audio_filepath": "dataset_train/samples/1_Male_de-AT-JonasNeural.wav", "text": "umstellman\u00f6ver vom gleis sechs zwo eins  nach gleis eins acht zwo", "duration": 4.9245}


2. What kind of error handling was implemented during the creation of the manifest.json file?
ANSWER:

- duplications have been discarded
- ensure that manifest.json line only is added if the sample exists

---

In addition, tell me what areas could be improved or added in order to achieve a perfect grade?

# Contents

Thank you for providing a high-level overview. Let's start with developing the methodology
section. This section will include a graphic which visualizes the entire process from
beginnig to end. The two main components are the "data pipeline" (~ 80% of workload) and the model training (~ 20% of workload). The data pipeline is split into a) commandos generation, b) speech generation, and c) training set creation and covers all necessary parts for the text-to speech conversion, whereas the model training focusses on speech-to-text conversion.

The first step (commandos generation) is required to have a rule-based generation of
commandos. Here randomness is introduced in several occassions (e.g. what alpha numeric
character, whether to include gleis 50% and several variations of words to be used) which
should properly reflect the commandos that are specified for the personnel to be used.
Once the commandos have been generated, they need to be transfored into speech in the next
step. Here Azure SDK has been chosen for the following three reasons: 1) large library of
text to speech voices (including many german, swiss and austrian voices), 2) fast and
cost-effective - as we generate 20k voices the process of conversion should not be a
bottle neck, having it priced attractively and the generation in a timely manner. 3)
Configuration possibilities using SSML - To have the model later on generalize well on the
test set, the voices should have variations. Having the ssml syntax provided by azure (xml
like) allows us to include various parameters, including breaks, pitch rate, speed. For
the creation of the speech, this was a important criterion.

The following parameters have been used for speech generation (aimed to reflect the real
life scenario): 
	"male_to_female": 0.7,
    "combinations_count": 20000,
    "language_distribution": {
		"de-DE": 0.70,
		"fr-FR": 0.15,
		"it-IT": 0.075,
		"en-US": 0.025,
		"pt-PT": 0.025,
		"es-ES": 0.025,
		"ta-IN": 0.025,
		"tr-TR": 0.025,
		"ar-EG": 0.025
    },
	"pitch_options": ["low", "medium" ],
    "rate_options": ["slow", "medium" ],


It is important to note that the AZURE SDK had a high learning curve, having a lot of
configuration options and necessary declarations was time consuming.

As a last step once the speech samples were generated further steps had been necessary to
create the final training set for the model. The model requires a manifest.json file that
includes (duration, file path, and label). In the text to speech step, lines for each
samples were added to the manifest.json file (including several error handling steps to
ensure consistency) and made use of command line utilities to efficiently calculate
duration. Furthermore a variant of the manifest.json file has also been made to only
include samples with german accent (which later will be compared to foreign accents in the
performance of the model).

---
Followingly guide me in developing this section, which should amount to 1.5 - 2.5 Pages.
Use my provided notes and the code for this section (excluding the model training
conformer code). This section should be written in an academic style and be inspired by
other academic methodology written papers in the natural language processing domain.

As this paper should receive a perfect grade ask me questions on the methodological
approach to improve the quality of this section.

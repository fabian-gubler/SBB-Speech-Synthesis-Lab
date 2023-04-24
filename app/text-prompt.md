I want generate random commandos for trains using a python script

This is an Example of such a commando: Rangierfahrt von Gleis a14 via Gleis 22 nach Gleis b523.

Rangierfahrt von [Random Part] via [Random Part] nach [Random Part]

Note that the "via [Random Part]" is optional. Also using the word "Gleis" is optional.

There should be a possibility to add a random part to the commando. 
This random part can be a letter from a until z followed by one or two numbers. (a1, a14, b523, z1, z22) with no zeros.

Possible random distributions could be 50% chance for a letter and a number, 25% chance for a letter and two numbers, 25% chance only numbers

The random part should be added to the commando at a random position. (Rangierfahrt von Gleis a14 via Gleis 22 nach Gleis b523.)

The probability of having a via [Random Part] should be 50%
The probability of using Gleis should be 50%. Meaning that either using Gleis for the entire sentence or not at all.

The user should be able to define the number of commandos to be generated. (100, 1000, 10000, ...)

Note that Letters should be transformed to its nato alphabet counterpart (a = alpha, b = bravo, c = charlie, ...)
Also note that Letters and numbers should always be separated by a white space
Commands should end with a punctuation mark.

In addition, breaks should be added always between letters and numbers
using the notiation <break strength=<value> /> notation (e.g. Gleis alpha <break strength=short/> 2). Strength could be either x-weak, weak, medium, or strong)

Also, zero to 3 words should be enclodes in an emphasis tag with the attribute "level"
which can be reduced, moderate or strong (e.g. Gleis <emphasis level=moderate> alpha
14</emphasis>)

Determine a suitable filetype for the output file including the commandos. (txt, csv, json, xml, ...). They will be later imported and used as input for generating text to speech.

Because they will later be used to train a neural network, containing the raw text
(without e.g. break notation) is vital for the output file.

If before generating the python script there are any clarification questions, please ask
before providing the code output.

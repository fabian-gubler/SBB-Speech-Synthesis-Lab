Great! Now that we have a nice results section we should continue with the discussion
section. In addition to the followingly provided notes it should include the
shortcomings of the dataset. For instance it could add that the dataset should be improved
regarding the variations of speakers and commandos in the dataset. This could be improved
through the introduction of synthetic data, but if possible should be also done on the
human recorded side. Also, it should be noted that conformer ctc gave pretty good
results with limited data. Based on the qualitative findings, it was shown that it got
a lot of things almost correct. If we introduce a second model that then parses
predictions with the limited classification set provided by the use case the model
could substantially be improved further. Also, highlight the novelty of our findings
indicating that using synthetic samples for a limited dataset can be a great method to
reduce shortcomings and represents a new perspective for speech recognition. As
outlook, In
addition to synthetic samples the performance might also be improved by altering existing
human samples (e.g. pitching them, speaker separation etc.). On the synthetic side
future work could be to look at the performance of specific accents applied to the use
case to find out which contributed the most to the performance. This could be then
compared to a test set that includes accented speakers to find out whether using text
to speech ultimately can resolve the issues of a heterogenous workforce.

# 4 Discussion
## 4.1 Recapitulation of Key Findings
Start this section by succinctly summarizing the primary outcomes of your experiments and re-
sults. Highlight the most significant findings, improvements over the baseline, the impacts of data
augmentation, and the model’s performance on different accents.
For example: “Our work successfully demonstrated that the application of synthetic data augmen-
tation can significantly enhance the performance of a Conformer-CTC model in automatic speech
recognition tasks. Specifically, we observed a significant reduction in Word Error Rate compared to
the baseline, particularly in instances where we incorporated German-accented synthetic samples. . . ”

## 4.2 Interpretation and Implications
In this section, provide your interpretations of the results and discuss the implications. Evaluate the
real-world impact and potential applications of your findings.
For instance: “The notable improvements in our model’s performance, particularly when trained with
synthetic data augmented with diverse accents, signal a significant breakthrough in overcoming the
challenges posed by multi-accented and diverse speech. This finding has profound implications for
industries and applications where. . . ”
## 4.3 Comparison with Existing Literature
Briefly compare your findings with existing literature. Discuss how your work aligns with or diverges
from previous studies.
7
For example: “While our results align with prior research indicating the effectiveness of data aug-
mentation in speech recognition tasks, our work further extends this understanding by demonstrating
that. . . ”

## 4.4 Strengths and Limitations
Acknowledge the strengths and limitations of your work. This could include aspects of the methodol-
ogy, the model used, or the generalizability of your findings.
For instance: “While our research effectively highlights the potential of synthetic data augmentation
in improving speech recognition performance, it is not without limitations. One potential limitation
is. . . ”

## 4.5 Recommendations for Future Research
Outline the opportunities for further research, based on your findings and experiences.
For instance: “Given the promising results achieved through the incorporation of synthetic data,
future research could explore the use of more sophisticated text-to-speech systems to generate even
more realistic synthetic speech. Additionally, the exploration of other models or hybrid models could
yield. . . ”

## 4.6 Conclusion
Conclude the discussion section by summarizing the main points, reaffirming the significance of your
findings, and providing a clear take-home message for the reader.
For instance: “In conclusion, our research illustrates the transformative potential of synthetic data
augmentation in advancing automatic speech recognition tasks. Despite the challenges of diverse
accents and limited data, we demonstrated that it’s possible to achieve significant improvements using
an innovative data augmentation strategy...""

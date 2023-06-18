# Results

The results section elucidates the findings from the project, with a particular emphasis on the performance of the Conformer-CTC model under various training conditions. It explores how the inclusion of different amounts of synthetic data impacts the model's performance and contrasts this with both the baseline model and the model trained solely with human-recorded samples.

## Model Performance with Data Augmentation

To analyze the effects of synthetic data augmentation on the model's performance, we first established a baseline using the pretrained Conformer-CTC model, which achieved a Word Error Rate (WER) of 39.48% without any training on our dataset.

From there, we trained the model on the human-recorded samples alone, which constituted 70% of our entire dataset. This resulted in a significant improvement over the baseline, reducing the WER to 10.07%.

We then incrementally added synthetic data to the training set and assessed the model's performance. This led to further improvements in performance, with WER decreasing as synthetic data increased, although with some fluctuations at certain increments.

[Insert Table 1 Here: Comparison of WER at various levels of synthetic data inclusion]

A visual representation of the WER trend as synthetic data increased is also presented.

[Insert Figure 7 Here: Graph of change in performance (WER) as synthetic data increases]

## Comparison with Human-Recorded Samples

When comparing the model trained with synthetic data against the model trained only with human-recorded samples, it's evident that the inclusion of synthetic data contributed significantly to performance enhancement. 

While the model trained with human-recorded samples achieved a WER of 10.07%, the model trained with synthetic data demonstrated lower WER percentages across different increments of synthetic data inclusion, with the lowest WER of 5.395% observed at 40% synthetic data inclusion.

[Insert Comparative Table Here: Difference in performance metrics between models trained with and without synthetic data]

## Accent-Specific Performance

Our experiment also tested the model's proficiency in recognizing speech with diverse accents, specifically focusing on German accents. The preliminary results indicate a trend towards improved performance when German-accented synthetic samples were included, although the experiments are still ongoing.

[Insert Accent-Specific Performance Table Here: Performance metrics for each type of accent]

## Contributions of Synthetic Data

With a comprehensive analysis of the performance data, it's evident that the inclusion of synthetic data substantially improved the model's performance. While specific aspects of the synthetic dataset that contributed most to the performance improvement have not yet been fully identified, it's clear that data augmentation with synthetic samples played a crucial role.

[Insert Further Analysis Here: Investigation of the specific features of synthetic data that contributed most to performance improvement]

## Qualitative Analysis

To complement the performance metrics, this subsection will provide specific examples of the model's predictions, highlighting its strengths and weaknesses. This will include instances where the model excelled or struggled in recognizing specific accents or commandos.

[Insert Qualitative Analysis Examples Here: Case studies of model's predictions]

---

*In this draft, placeholders and descriptions of the figures, tables, and analysis are provided. Once the final results, analysis, and figures are complete, these can be inserted into the document at the indicated positions.*

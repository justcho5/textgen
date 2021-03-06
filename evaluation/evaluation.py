#
# NIST Test for NLG text evaluation
#
# Implementation based on:
# Papineni, K., Roukos, S., Ward, T. and Zhu, W.J., 2002, July. BLEU: a method for automatic evaluation of machine
# translation. In Proceedings of the 40th annual meeting on association for computational linguistics (pp. 311-318).
# Association for Computational Linguistics.
#
# Strong correlation with human expert evaluation for natural language generation (NLG) shown by
# Belz, A. and Reiter, E., 2006, April. Comparing Automatic and Human Evaluation of NLG Systems. In EACL.
#
# See '__main__' for usage explanation
#

import io
import numpy as np
import math
from fractions import Fraction
from collections import Counter
from nltk.util import ngrams

# Dictionary to memoize/cache information value of various n-grams
info_value = {}

# List of words in reference document
reference_data = None


def strip_non_ascii(utf_str):
    """
    Convert utf-8 strings to ASCII codec
    :param utf_str: utf-8 string
    :return: string without non ASCII characters
    """

    stripped = (c for c in utf_str if 0 < ord(c) < 127)
    return ''.join(stripped).encode(encoding='ascii', errors='ignore')


def pre_process(str_text):
    """
    Perform all pre-processing steps on input string
    :param str_text: input
    :return: pre-processed list of tokens for training
    """

    str_text = str(str_text)

    # Uncomment to remove punctuation from all texts
    # import string
    # replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    # str_text = str_text.translate(replace_punctuation)

    str_text = strip_non_ascii(str_text).lower().replace('\n', ' ').replace('\r', ' ')
    return ' '.join(str_text.split())


def get_information_value(words):
    """
    Calculate information value from reference document
    Let words = [w_1, w_2, ..., w_n], n-gram,
    k_1 = Number of occurrences of (n-1)-gram [w_1, w_2, ..., w_{n-1}] in text
    k_2 = Number of occurrences of n-gram [w_1, w_2, ..., w_n] in text
    then Info(words) = log_2 (k_1 / k_2)
    :param words: list of words (n-gram)
    :return: Information value of words
    """

    if reference_data is None:
        raise ValueError("No reference data found")

    words_k1 = ' '.join(words)
    words_k2 = ' '.join(words[:-1])
    try:
        return info_value[words_k1]
    except KeyError:
        pass

    k1 = 0.1 + reference_data.count(words_k1)
    k2 = 0.1 + reference_data.count(words_k2)
    info_count = np.log2(k1 / k2)

    info_value[words_k1] = info_count
    return info_count


def modified_bleu(references, hypothesis, weights=tuple([0.25] * 8), pivot=4):
    """
    Calculate single modified version of the system BLEU score (aka. system-level BLEU)
    The original BLEU metric (Papineni et al. 2002) accounts for micro-average precision
    :param references: lists of reference split list sentences (human produced texts, training text for system)
    :param hypothesis: hypothesis sentence (system generated text) split list for evaluation
    :param weights: weighting scheme (n values, 8 by default) corresponding to 1-grams to n-grams
    :param pivot: index to break weights values around for quality and overfitting metrics
    :return: modified BLEU score value, accounting for over-fitting
    :return: over-fitting penalty value
    """

    # Check if pivot value is a valid index to break the weights array around
    assert len(weights) > pivot

    # Counter instance for numerators (Number of n-gram matches vs n-gram n value as key)
    numerators = Counter()
    # Counter instance for denominator (Number of n-gram in references vs n-gram n value as key)
    denominators = Counter()

    # For each order of n-gram, calculate the numerator and
    # denominator for the corpus-level modified precision.
    for i, _ in enumerate(weights, start=1):
        precision = modified_precision(references, hypothesis, i)
        numerators[i] += precision.numerator
        denominators[i] += precision.denominator

    # No brevity penalty is applied - different lengths of hypothesis and reference strings are irrelevant
    # in the case of evaluating text generation results
    # Collect various precision values for the different n-gram orders, default n = 1 to n = 4
    precision_values = [Fraction(numerators[i], denominators[i]) for i, _ in enumerate(weights, start=1)]

    # Check if no matching 1-grams found, implying no matching n-grams found
    if numerators[1] == 0:
        return 0

    # Do not perform smoothing as per typical BLEU functions, values remain in the form of fractions.Fraction
    s = (weight * math.log(precision) for i, (weight, precision) in enumerate(zip(weights, precision_values))
         if precision.numerator != 0)

    # Extract list of values from generator s
    weighted_precision = list(s)

    # Over-fitting measured by considering modified BLEU score values of weights and precision values after pivot
    # Presence of significantly higher order n-gram matches, against training set imply over-fitting
    overfitting_penalty = math.exp(math.fsum(weighted_precision[pivot:]))
    if len(weighted_precision) <= pivot:
        overfitting_penalty = 0

    return math.exp(math.fsum(weighted_precision[:pivot])), overfitting_penalty


def modified_precision(references, hypothesis, n):
    """
    Modified precision calculation implemented with minor modifications to baseline implementation in NLTK toolkit BLEU
    Calculate modified ngram precision for a single pair of hypothesis and references, cast the Fraction to float
    :param references: list of reference texts (originals and human written)
    :param hypothesis: hypothesis text split list (generated by LSTM-RNN system)
    :param n: n-gram order (value of n in n-gram)
    :return: BLEU's modified precision for n-gram.
    """

    # Extracts all ngrams in hypothesis
    ngrams_counts = Counter(ngrams(hypothesis, n)) if len(hypothesis) >= n else Counter()

    max_counts = {}
    for reference in references:
        reference_counts = Counter(ngrams(reference, n)) if len(reference) >= n else Counter()
        for ngram in ngrams_counts:
            max_counts[ngram] = max(max_counts.get(ngram, 0), reference_counts[ngram])

    # Clip words count matching between the intersection between hypothesis and references counts
    clip_ngrams_counts = {ngram: min(count, max_counts[ngram]) for ngram, count in ngrams_counts.items()}

    numerator = sum(clip_ngrams_counts.values())
    denominator = max(1, sum(ngrams_counts.values()))
    return Fraction(numerator, denominator)


def evaluate_nlg(evaluation_file, reference_file='training/1.txt'):
    """
    Compute evaluation score based of BLEU evaluation metrics for machine translation
    :param evaluation_file: Text for evaluation
    :param reference_file: File with human generated reference text
    :return: Evaluated score for file (Text Quality metric, Over-fitting metric)
    """

    global reference_data

    # Read reference and evaluations files
    # Convert all text from files to ascii characters from the utf-8 codec and pre-process text
    with io.open(evaluation_file, 'r', encoding='utf-8') as evaluation:
        evaluation_data = evaluation.read().encode('ascii', errors='ignore')
        eval_data_char_len = len(evaluation_data)
        evaluation_data = pre_process(evaluation_data).split()

    with io.open(reference_file, 'r', encoding='utf-8') as reference:
        reference_data = reference.read().encode('ascii', errors='ignore')
        reference_data = pre_process(reference_data)

    # Reference text splitting
    # Divide large reference text into multiple smaller reference texts each (except possibly the last)
    # of length exactly equal to that of the evaluation (LSTM-RNN generated text)
    # Modified BLEU evaluation metric scores are calculated against each of the multiple similar length
    # reference texts and averaged geometrically to give the final score
    n = eval_data_char_len
    reference_data = [reference_data[i:i + n].split() for i in range(0, len(reference_data), n)]

    return modified_bleu(reference_data, evaluation_data)


if __name__ == '__main__':
    # Below is an example to evaluate the basefile 'sherlock-4-1l-512n' and the epochs listed. 
    #
    # Modify basefile and epochs accordingly to evaluate text generated for a particular LSTM-RNN configuration
    # (based on basefile) and different numbers of epochs. Text files should be found in output/ be named with the 
    # format output/output-[basefile]-[epoch-number].txt. Text files in this format can be generated
    # by scripts/odyssey-generate-generic.sh calling src/generate-generic.py for weights generated by
    # scripts/odyssey-train-generic.sh calling src/train-generic.py
    #
    # The example is from a configuration with 1 layer and 512 nodes. Epochs were hand-selected (they are
    # not nice numbers because weights are only saved when an epoch has improved on the loss function).
    basefile = 'sherlock-4-1l-512n'
    epochs = ['10', '25', '50', '100', '153', '203', '251', '304', '356', '406', '458', '503', '551', '602', '653', '704', '755', '800', '870', '905', '950', '991']
    
    quality = []
    overfit = []
    # Calculate the quality and overfit metrics for each text file and append the results to the quality
    # and overfit arrays
    for epoch in epochs:
        modified_bleu_scores = evaluate_nlg(evaluation_file='output/output-' + basefile + '-' + epoch + '.txt', reference_file='training/4-mod.txt')
        quality.append(modified_bleu_scores[0])
        overfit.append(modified_bleu_scores[1])

    # Print the list of epoch numbers, quality metrics, and overfit metrics to eval-results/eval-[basefile].txt
    # The printed format is easily adapted to generate a plot with evaluation/plot.py
    with open('eval-results/eval-' + basefile + '.txt', 'w') as output_file:
        output_file.write(str(map(int, epochs)))
        output_file.write('\n')
        output_file.write(str(quality))
        output_file.write('\n')
        output_file.write(str(overfit))

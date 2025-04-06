from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab', quiet=True)

def calculate_bleu(candidate_doc: str, reference_doc: str) -> float:
    """
    Calculates the BLEU score comparing the candidate documentation against a reference.

    :param candidate_doc: Generated documentation text.
    :param reference_doc: Reference documentation text.
    :return: The BLEU score as a float.
    """
    candidate_tokens = word_tokenize(candidate_doc)
    reference_tokens = word_tokenize(reference_doc)
    score = sentence_bleu([reference_tokens], candidate_tokens)
    return score

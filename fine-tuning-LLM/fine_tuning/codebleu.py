# codebleu.py (standalone)
import os
from collections import Counter
from fractions import Fraction
import math

def make_weights(tokens, keywords):
    return {token: 1.0 if token in keywords else 0.2 for token in tokens}

def modified_precision(references, hypothesis, n):
    counts = Counter([tuple(hypothesis[i:i+n]) for i in range(len(hypothesis)-n+1)])
    if not counts:
        return Fraction(0, 1)

    max_counts = {}
    for reference in references:
        ref_counts = Counter([tuple(reference[i:i+n]) for i in range(len(reference)-n+1)])
        for ngram in counts:
            max_counts[ngram] = max(max_counts.get(ngram, 0), ref_counts[ngram])

    clipped_counts = {ngram: min(count, max_counts.get(ngram, 0)) for ngram, count in counts.items()}
    return Fraction(sum(clipped_counts.values()), max(1, sum(counts.values())))

def brevity_penalty(references, hyp_len):
    ref_lens = [len(ref) for ref in references]
    closest_ref_len = min(ref_lens, key=lambda ref_len: (abs(ref_len - hyp_len), ref_len))
    if hyp_len > closest_ref_len:
        return 1
    elif hyp_len == 0:
        return 0
    else:
        return pow(2.718, 1 - closest_ref_len / hyp_len)

def corpus_bleu(list_of_references, hypotheses, weights=(0.25, 0.25, 0.25, 0.25)):
    p_n = [Fraction(0, 1) for _ in weights]
    hyp_len = 0
    ref_len = 0

    for refs, hyp in zip(list_of_references, hypotheses):
        hyp_len += len(hyp)
        ref_len += min(len(r) for r in refs)
        for i, weight in enumerate(weights, start=1):
            p_n[i-1] += modified_precision(refs, hyp, i)

    log_p_n = [
        0.0 if p_n[i].numerator == 0
        else math.log(p_n[i].numerator / p_n[i].denominator)
        for i in range(len(weights))
    ]

    bp = brevity_penalty([r for refs in list_of_references for r in refs], hyp_len)
    score = bp * pow(2.718, sum(w * lp for w, lp in zip(weights, log_p_n)))
    return float(score)

def compute_codebleu(preds, refs, lang="python", weights=(0.5, 0.5), keywords_path="keywords"):
    assert len(preds) == len(refs), "Predictions and references must be same length"
    tokenized_hyps = [x.split() for x in preds]
    tokenized_refs = [[r.split() for r in ref_set] for ref_set in refs]

    # Load keywords
    keywords_file = os.path.join(keywords_path, f"{lang}.txt")
    with open(keywords_file, 'r', encoding='utf-8') as f:
        keywords = [line.strip() for line in f]

    # BLEU score
    bleu_score = min(1.0, corpus_bleu(tokenized_refs, tokenized_hyps))


    # Weighted BLEU
    weighted_refs = []
    for refs in tokenized_refs:
        weighted = []
        for ref in refs:
            ref_weights = make_weights(ref, keywords)
            weighted.append([ref, ref_weights])
        weighted_refs.append(weighted)

    weighted_bleu = min(1.0, weighted_ngram_bleu(weighted_refs, tokenized_hyps))

    final_score = weights[0] * bleu_score + weights[1] * weighted_bleu
    #print(f"[DEBUG] BLEU: {bleu_score}, Weighted BLEU: {weighted_bleu}, CodeBLEU: {final_score}")

    return {
        "bleu": bleu_score,
        "weighted_bleu": weighted_bleu,
        "codebleu": final_score
    }



def weighted_ngram_bleu(weighted_references, hypotheses, weights=(0.25, 0.25, 0.25, 0.25)):
    score_total = 0.0
    for refs, hyp in zip(weighted_references, hypotheses):
        hyp_ngrams = [Counter(tuple(hyp[i:i+n]) for i in range(len(hyp)-n+1)) for n in range(1, 5)]
        ref_ngrams = []
        for ref_tokens, ref_weights in refs:
            ngram_weights = []
            for n in range(1, 5):
                ngram_weight = Counter()
                for i in range(len(ref_tokens) - n + 1):
                    ngram = tuple(ref_tokens[i:i+n])
                    weight = sum(ref_weights.get(tok, 0.0) for tok in ngram) / n
                    ngram_weight[ngram] += weight
                ngram_weights.append(ngram_weight)
            ref_ngrams.append(ngram_weights)

        precisions = []
        for n in range(4):
            match = 0.0
            total = sum(hyp_ngrams[n].values())
            if total == 0:
                precisions.append(0.0)
                continue
            for ngram in hyp_ngrams[n]:
                max_ref = max((r[n].get(ngram, 0.0) for r in ref_ngrams), default=0.0)
                match += min(hyp_ngrams[n][ngram], max_ref)
            precisions.append(match / total)

        bp = brevity_penalty([r[0] for r in refs], len(hyp))
        score = bp * pow(2.718, sum(w * (0 if p == 0 else math.log(p)) for w, p in zip(weights, precisions)))
        score_total += score

    return score_total / len(hypotheses)

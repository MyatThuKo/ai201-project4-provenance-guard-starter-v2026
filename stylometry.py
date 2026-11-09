"""
Signal two: stylometric analysis of writing.

This module measures writing characteristics without analyzing
the meaning of the text.

It uses three measurements:
    - Sentence-length variation
    - Vocabulary diversity
    - Punctuation density

These measurements are normalized and combined into an
AI-likelihood score between 0 and 1.

Higher scores indicate more AI-like writing patterns,
not proof that AI generated the text.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Calculate the coefficient of variation of sentence lengths.

    Returns:
        A nonnegative float representing sentence-length variation.
        Higher values indicate greater variation.

        Returns 0.0 when fewer than two usable sentences exist.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]

    if len(lengths) < 2:
        return 0.0

    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Measure vocabulary diversity using a moving-window TTR.

    Uses 50-word windows for longer text and ordinary TTR
    for shorter text.

    Returns:
        A float between 0 and 1.
        Higher values indicate greater vocabulary diversity.
    """
    tokens = words(text)

    if not tokens:
        return 0.0

    window = 50

    if len(tokens) <= window:
        return round(len(set(tokens)) / len(tokens), 4)

    ratios = [
        len(set(tokens[i:i + window])) / window
        for i in range(len(tokens) - window + 1)
    ]

    return round(statistics.mean(ratios), 4)



def punctuation_density(text: str) -> float:
    """
    Measure stylistic punctuation marks per word.

    Counts commas, semicolons, colons, parentheses,
    quotation marks, question marks, exclamation marks,
    and dashes.

    Excludes sentence-ending periods, apostrophes within
    words, and hyphens within compound words.

    Returns:
        A nonnegative float representing punctuation per word.
    """
    tokens = words(text)

    if not tokens:
        return 0.0

    marks = re.findall(r'[,;:!?()"“”‘’—–]', text)
    marks += re.findall(r"(?<!\w)'|'(?!\w)", text)
    marks += re.findall(r"(?<!\w)-(?!\w)", text)

    return round(len(marks) / len(tokens), 4)



# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    Calculate a normalized AI-likelihood score from writing style.

    Three normalized features contribute:

        Sentence-length spread: 30%
        Vocabulary diversity:   70%
        Punctuation density:    not used

    Lower sentence-length variation is treated as more AI-like.

    Higher vocabulary diversity is treated as more AI-like,
    based on initial exploratory samples. This is a heuristic,
    not a universally valid distinction.

    Lower punctuation density is treated as more AI-like.

    For fewer than two usable sentences, sentence-length
    variation contributes a neutral score of 0.5.

    Returns:
        A float between 0.0 and 1.0.
        Higher values indicate stronger AI-like patterns.

    Limitations:
        The score cannot establish authorship and is sensitive
        to text length, formatting, and writing conventions.
    """
    spread = sentence_length_spread(text)
    usable_sentences = [
        sentence for sentence in sentences(text)
        if words(sentence)
    ]

    if len(usable_sentences) < 2:
        spread_ai = 0.5
    else:
        spread_ai = 1.0 / (1.0 + (spread / 0.35) ** 2)

    ttr_ai = min(max((type_token_ratio(text) - 0.75) / 0.20, 0.0), 1.0)

    punct_ai = 1.0 / (1.0 + (punctuation_density(text) / 0.05) ** 2)

    score = 0.3 * spread_ai + 0.7 * ttr_ai
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")

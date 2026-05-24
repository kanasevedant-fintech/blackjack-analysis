"""
combinatorics.py — Phase 2: Exact two-card probabilities
========================================================

This module computes exact probabilities for the first two cards in blackjack.
It uses counting and combinations only; there is no simulation here.

Reference: "Blackjack: the math behind the cards".
"""
from math import comb

from src.cards import CARD_VALUES, RANKS, SUITS


def value_counts(num_decks: int) -> dict[int, int]:
    """Return the number of cards of each blackjack value in the shoe."""
    counts = {value: 0 for value in range(2, 12)}

    for _ in range(num_decks):
        for _ in SUITS:             # each rank appears once per suit
            for rank in RANKS:
                card_value = CARD_VALUES[rank]
                counts[card_value] += 1

    return counts


def total_cards(num_decks: int) -> int:
    """Total number of cards in a shoe with num_decks decks."""
    return 52 * num_decks


def prob_blackjack(num_decks: int) -> float:
    """Probability of a natural blackjack on the first two cards."""
    counts = value_counts(num_decks)
    total = comb(total_cards(num_decks), 2)

    # One Ace and one ten-value card form a natural blackjack.
    favourable = counts[11] * counts[10]
    return favourable / total if total > 0 else 0.0


def prob_two_card_total(target: int, num_decks: int) -> float:
    """Probability that the first two cards sum to the given target."""
    counts = value_counts(num_decks)
    favourable = 0

    # Loop over all valid blackjack card values a <= b.
    for a in range(2, 12):
        b = target - a
        if b < a or b > 11:
            continue

        count_a = counts.get(a, 0)
        count_b = counts.get(b, 0)
        if count_a == 0 or count_b == 0:
            continue

        if a == b:
            favourable += comb(count_a, 2)
        else:
            favourable += count_a * count_b

    total = comb(total_cards(num_decks), 2)
    return favourable / total if total > 0 else 0.0

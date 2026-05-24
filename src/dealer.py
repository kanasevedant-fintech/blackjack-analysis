"""
dealer.py — Phase 3: Dealer outcome distribution
================================================
The dealer follows a fixed rule: hit on 16 or less, stand on 17+.
(Flip hit_soft_17=True later for the common "H17" casino rule.)

Goal: for each dealer upcard, find P(final total = 17/18/19/20/21/bust).
Do it TWO ways and confirm they agree:
  - simulate_dealer(...)      -> Monte Carlo
  - dealer_distribution(...)  -> exact recursion (advanced, optional at first)
"""
from collections import Counter
from functools import lru_cache
from .cards import Deck, Hand, Card, RANKS


def dealer_should_hit(total: int, is_soft: bool, hit_soft_17: bool = False) -> bool:
    """Encodes the casino rule. (Given to you.)"""
    if total < 17:
        return True
    if total == 17 and is_soft and hit_soft_17:
        return True
    return False


def simulate_dealer(upcard_rank: str, num_decks: int = 6,
                    trials: int = 100_000, hit_soft_17: bool = False) -> dict:
    """Monte Carlo. For each trial: start a Hand with the given upcard, draw a
    hole card, then keep hitting per dealer_should_hit until standing/busting.
    Tally the final totals across all trials and return probabilities, e.g.
        {17: .., 18: .., 19: .., 20: .., 21: .., "bust": ..}

    Steps per trial:
      1. deck = Deck(num_decks); deck.shuffle()
      2. hand = Hand(); add the upcard, then deck.deal() for the hole card
         (simplest start: just build a fresh shoe each trial)
      3. while dealer_should_hit(hand.value, hand.is_soft, hit_soft_17):
             hand.add_card(deck.deal())
      4. record "bust" if hand.is_bust else hand.value
    """
    tally: Counter = Counter()
    upcard = Card(upcard_rank, "S")   # suit doesn't affect value

    for _ in range(trials):
        deck = Deck(num_decks)
        deck.shuffle()

        hand = Hand()
        hand.add_card(upcard)
        hand.add_card(deck.deal())    # hole card from the shoe

        while dealer_should_hit(hand.value, hand.is_soft, hit_soft_17):
            hand.add_card(deck.deal())

        outcome = "bust" if hand.is_bust else hand.value
        tally[outcome] += 1

    return {outcome: count / trials for outcome, count in tally.items()}


def dealer_distribution(upcard_value: int, hit_soft_17: bool = False) -> dict:
    """ADVANCED / OPTIONAL: exact distribution using an infinite-deck
    approximation (each draw is value 1..9 with prob 1/13, value 10 with
    prob 4/13, Ace with prob 1/13). Recurse over the dealer's running total.
    Compare its output to simulate_dealer() — they should be very close.
    """
    # Infinite-deck draw probabilities: 13 equally likely ranks,
    # but 10-value covers four ranks (10, J, Q, K) → 4/13.
    DRAW_PROBS: dict[int, float] = {v: 1 / 13 for v in [2, 3, 4, 5, 6, 7, 8, 9, 11]}
    DRAW_PROBS[10] = 4 / 13

    @lru_cache(maxsize=None)
    def recurse(total: int, soft: bool) -> dict:
        """Return probability distribution over final outcomes from (total, soft)."""
        if not dealer_should_hit(total, soft, hit_soft_17):
            return {"bust": 1.0} if total > 21 else {total: 1.0}

        result: dict = {}
        for v, prob in DRAW_PROBS.items():
            new_total = total + v
            new_soft = soft or (v == 11)
            # Burn the soft Ace if we'd bust with it
            if new_total > 21 and new_soft:
                new_total -= 10
                new_soft = False
            for outcome, p in recurse(new_total, new_soft).items():
                result[outcome] = result.get(outcome, 0.0) + prob * p

        return result

    return dict(recurse(upcard_value, upcard_value == 11))

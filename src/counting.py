"""
counting.py — Phase 6: Card counting (Hi-Lo)
============================================
Reference: the PyCount paper (Hi-Lo, running count, true count).

Hi-Lo tag values (given):
    2,3,4,5,6  -> +1     (low cards gone => good for player)
    7,8,9      ->  0
    10,J,Q,K,A -> -1     (high cards gone => bad for player)

running_count = sum of tags of all cards seen so far
true_count    = running_count / decks_remaining
"""

HI_LO = {
    2: +1, 3: +1, 4: +1, 5: +1, 6: +1,
    7: 0, 8: 0, 9: 0,
    10: -1, 11: -1,   # 11 represents the Ace
}


def tag(card_value: int) -> int:
    """Hi-Lo tag for a card's blackjack value (2..11). (Given.)"""
    return HI_LO[card_value]


def true_count(running_count: int, cards_remaining: int) -> float:
    """Convert running count to true count.
    decks_remaining = cards_remaining / 52; true = running / decks_remaining.
    Guard against dividing by zero / tiny deck remnants.
    """
    if cards_remaining <= 0:
        return 0.0
    decks_remaining = cards_remaining / 52
    return running_count / decks_remaining


def bet_from_count(tc: float, base_bet: float = 1.0,
                   max_bet: float = 8.0) -> float:
    """A simple bet ramp: bet more when the true count is high (favourable).
    A common starting rule: bet = base_bet * max(1, tc - 1), capped at max_bet.
    This is a DESIGN CHOICE — experiment and plot how it changes results.
    """
    bet = base_bet * max(1.0, tc - 1)
    return min(bet, max_bet)

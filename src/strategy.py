"""
strategy.py — Phase 4: Expected value & basic strategy
======================================================
Reference: Thorp — basic strategy drops the house edge from ~4% to ~0.5%.

For every (player total, dealer upcard) you compute the EV of each action and
keep the best. Start SMALL: only HIT vs STAND on hard totals. Get that working
and validated, THEN add DOUBLE and SPLIT.

You'll lean on the dealer distribution from Phase 3.
"""
from .dealer import dealer_distribution
from .cards import CARD_VALUES

ACTIONS = ["stand", "hit", "double", "split"]

# Infinite-deck draw probabilities — same approximation used in dealer.py.
DRAW_PROBS: dict[int, float] = {v: 1 / 13 for v in [2, 3, 4, 5, 6, 7, 8, 9, 11]}
DRAW_PROBS[10] = 4 / 13


def ev_stand(player_total: int, dealer_dist: dict) -> float:
    """EV of standing, in betting units, given the dealer outcome probabilities.

    For each dealer outcome:
        dealer busts  -> you win  (+1)
        dealer < you  -> you win  (+1)
        dealer == you -> push     ( 0)
        dealer > you  -> you lose (-1)
    Return the probability-weighted sum.
    """
    ev = 0.0
    for outcome, prob in dealer_dist.items():
        if outcome == "bust" or outcome < player_total:
            ev += prob * (+1.0)
        elif outcome == player_total:
            ev += prob * 0.0
        else:                      # outcome > player_total
            ev += prob * (-1.0)
    return ev


def ev_hit(player_total: int, dealer_dist: dict, draw_probs: dict) -> float:
    """EV of taking one more card, then playing optimally afterwards.

    Recursive: after the new card you again choose the better of hit/stand.
    Ace counts as 1 if 11 would bust (standard hard-total assumption).
    """
    ev = 0.0
    for v, prob in draw_probs.items():
        # Treat a drawn Ace as 1 when 11 would bust.
        effective_v = 1 if (v == 11 and player_total + 11 > 21) else v
        new_total = player_total + effective_v

        if new_total > 21:
            branch_ev = -1.0
        else:
            stand_ev = ev_stand(new_total, dealer_dist)
            hit_ev = ev_hit(new_total, dealer_dist, draw_probs)
            branch_ev = max(stand_ev, hit_ev)

        ev += prob * branch_ev
    return ev


# Cache dealer distributions so we don't recompute for every cell of the table.
_DEALER_DIST_CACHE: dict[int, dict] = {}


def _get_dealer_dist(upcard_value: int) -> dict:
    if upcard_value not in _DEALER_DIST_CACHE:
        _DEALER_DIST_CACHE[upcard_value] = dealer_distribution(upcard_value)
    return _DEALER_DIST_CACHE[upcard_value]


def best_action(player_total: int, dealer_upcard: str, **kwargs) -> str:
    """Return the action with the highest EV for this situation."""
    upcard_value = CARD_VALUES[dealer_upcard]
    dealer_dist = _get_dealer_dist(upcard_value)

    stand_ev = ev_stand(player_total, dealer_dist)
    hit_ev = ev_hit(player_total, dealer_dist, DRAW_PROBS)

    return "stand" if stand_ev >= hit_ev else "hit"


def build_basic_strategy_table(num_decks: int = 6):
    """Loop over player totals x dealer upcards, return a pandas DataFrame of
    the best action in each cell. Compare it to the published chart — they
    should match for the hard totals."""
    import pandas as pd

    # Hard totals 5..20 (21 always stands; below 5 impossible with two cards).
    player_totals = list(range(5, 21))
    dealer_upcards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]

    table = {
        upcard: [best_action(total, upcard) for total in player_totals]
        for upcard in dealer_upcards
    }
    return pd.DataFrame(table, index=player_totals)

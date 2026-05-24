"""
kelly.py — Phase 7: Kelly criterion & bankroll
==============================================
Reference: Thorp (2006).
Kelly: wager a fraction f* of your bankroll proportional to your edge.
For an (approximately) even-money bet:  f* ~= edge / variance.

Goal: compare bankroll growth and risk of ruin for Kelly vs flat betting.
"""
import random


def kelly_fraction(edge: float, variance: float = 1.0) -> float:
    """Optimal fraction of bankroll to bet. Start simple: f* = edge / variance.
    (For blackjack, variance per unit bet is roughly ~1.3; refine later.)
    Never return a negative fraction — if edge <= 0, you bet 0 (or table min).
    """
    if edge <= 0:
        return 0.0
    return edge / variance


def simulate_bankroll(start: float, edge_per_hand: float, n_hands: int,
                      fraction: float, seed: int | None = None) -> list[float]:
    """Return the bankroll trajectory (a list of length n_hands+1) when betting
    `fraction` of the current bankroll each hand with the given per-hand edge.

    Model each hand as a +1/-1 unit outcome with win prob p where the expected
    value equals edge_per_hand, scaled by the bet. Compare a Kelly `fraction`
    against a small fixed one.
    """
    rng = random.Random(seed)

    # For a +1/-1 bet: E[outcome] = p*(+1) + (1-p)*(-1) = 2p - 1 = edge
    # => win probability p = (1 + edge) / 2
    p_win = (1.0 + edge_per_hand) / 2.0

    bankroll = start
    trajectory = [bankroll]

    for _ in range(n_hands):
        if bankroll <= 0:
            trajectory.append(0.0)
            continue

        bet = bankroll * fraction
        outcome = +1 if rng.random() < p_win else -1
        bankroll += bet * outcome
        bankroll = max(bankroll, 0.0)   # floor at zero (can't go negative)
        trajectory.append(bankroll)

    return trajectory


def risk_of_ruin(edge: float, fraction: float, ruin_threshold: float = 0.0,
                 start: float = 1000.0, n_hands: int = 10_000,
                 trials: int = 5_000, seed: int | None = None) -> float:
    """Estimate the probability the bankroll hits ruin_threshold.
    Runs simulate_bankroll `trials` times and counts how often it
    drops to/below the threshold at any point during the run.
    """
    rng = random.Random(seed)
    ruined = 0

    for i in range(trials):
        trajectory = simulate_bankroll(
            start=start,
            edge_per_hand=edge,
            n_hands=n_hands,
            fraction=fraction,
            seed=rng.randint(0, 2**31),
        )
        if min(trajectory) <= ruin_threshold:
            ruined += 1

    return ruined / trials

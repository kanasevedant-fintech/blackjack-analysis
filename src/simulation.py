"""
simulation.py — Phase 5: Monte Carlo engine
===========================================
Play many hands following a strategy; measure win/push/loss, EV, variance.
The simulated edge should CONVERGE to your Phase 2-4 exact numbers. That
agreement is your validation and the headline result of the project.
"""
from dataclasses import dataclass
from .cards import Deck, Hand
from .dealer import dealer_should_hit


@dataclass
class SimResult:
    hands: int = 0
    wins: int = 0
    pushes: int = 0
    losses: int = 0
    net_units: float = 0.0      # cumulative profit in betting units

    @property
    def edge(self) -> float:
        """Average profit per hand, from the player's perspective."""
        return self.net_units / self.hands if self.hands else 0.0

    @property
    def win_rate(self) -> float:
        return self.wins / self.hands if self.hands else 0.0


def play_one_hand(deck: Deck, strategy_fn, bet: float = 1.0,
                  hit_soft_17: bool = False) -> float:
    """Deal player + dealer, play the player via strategy_fn, play the dealer,
    settle, and return the NET result for this hand.
    Blackjack pays 1.5×; player bust loses regardless of dealer.
    """
    player = Hand()
    dealer = Hand()
    # Standard deal order: player, dealer, player, dealer.
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())

    upcard = dealer.cards[0]    # dealer's visible card

    # 1) Naturals settled immediately.
    if player.is_blackjack and dealer.is_blackjack:
        return 0.0
    if player.is_blackjack:
        return +1.5 * bet
    if dealer.is_blackjack:
        return -bet

    # 2) Player turn — strategy_fn returns "hit" or "stand".
    while True:
        action = strategy_fn(player, upcard)
        if action != "hit":
            break
        player.add_card(deck.deal())
        if player.is_bust:
            return -bet

    # 3) Dealer turn — fixed casino rule.
    while dealer_should_hit(dealer.value, dealer.is_soft, hit_soft_17):
        dealer.add_card(deck.deal())

    # 4) Settle.
    if dealer.is_bust:
        return +bet
    if player.value > dealer.value:
        return +bet
    if player.value < dealer.value:
        return -bet
    return 0.0


def run_simulation(num_hands: int, strategy_fn, num_decks: int = 6,
                   bet: float = 1.0, hit_soft_17: bool = False,
                   show_progress: bool = False) -> SimResult:
    """Repeatedly call play_one_hand and aggregate into a SimResult.
    Reshuffles the shoe when fewer than 25% of cards remain.
    """
    deck = Deck(num_decks)
    deck.shuffle()
    full_size = num_decks * 52
    reshuffle_at = int(full_size * 0.25)

    result = SimResult()

    iterator = range(num_hands)
    if show_progress:
        try:
            from tqdm import tqdm
            iterator = tqdm(iterator)
        except ImportError:
            pass

    for _ in iterator:
        # Reshuffle when penetration deep enough or not enough cards left.
        if len(deck) < max(reshuffle_at, 15):
            deck = Deck(num_decks)
            deck.shuffle()

        net = play_one_hand(deck, strategy_fn, bet, hit_soft_17=hit_soft_17)

        result.hands += 1
        result.net_units += net
        if net > 0:
            result.wins += 1
        elif net < 0:
            result.losses += 1
        else:
            result.pushes += 1

    return result

"""Card / Deck / Hand primitives.

Hand.value implements the soft/hard Ace rule: an Ace counts as 11 unless
that would bust the hand, in which case it counts as 1. A hand is "soft"
while at least one Ace still counts as 11.
"""
from __future__ import annotations
import random
from dataclasses import dataclass

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["S", "H", "D", "C"]  # spades, hearts, diamonds, clubs

# Aces are 11 here; the "Ace can also be 1" rule lives in Hand.value so
# the per-card value remains a single integer.
CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11,
}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def value(self) -> int:
        return CARD_VALUES[self.rank]

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class Deck:
    """A shoe made of `num_decks` standard 52-card decks."""

    def __init__(self, num_decks: int = 1) -> None:
        self.num_decks = num_decks
        self.cards: list[Card] = []
        self.reset()

    def reset(self) -> None:
        """Rebuild a full, ordered shoe of num_decks * 52 cards."""
        self.cards = []
        for _ in range(self.num_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """Remove and return one card from the shoe."""
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards)


class Hand:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def value(self) -> int:
        """
        Best total that is <= 21 when possible.
        Aces count as 11 unless that busts, in which case they drop to 1.
        """
        total = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    @property
    def is_soft(self) -> bool:
        """True if the hand still has an Ace being counted as 11.

        Hint: a hand is soft if (raw sum with all aces = 11) <= 21 AND it
        contains at least one Ace. Useful later for dealer rules & strategy.
        """
        raw_total = sum(card.value for card in self.cards)
        has_ace = any(card.rank == "A" for card in self.cards)
        return has_ace and raw_total <= 21

    @property
    def is_bust(self) -> bool:
        return self.value > 21

    @property
    def is_blackjack(self) -> bool:
        """A natural: exactly two cards totalling 21."""
        return len(self.cards) == 2 and self.value == 21

    def __str__(self) -> str:
        inside = " ".join(str(c) for c in self.cards)
        return f"[{inside}] = {self.value}"

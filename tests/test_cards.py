"""Test spec for src/cards.py."""
from src.cards import Deck, Hand, Card


def test_single_deck_has_52_cards():
    assert len(Deck(1)) == 52


def test_six_deck_shoe_has_312_cards():
    assert len(Deck(6)) == 312


def test_deal_reduces_deck_by_one():
    d = Deck(1)
    before = len(d)
    d.deal()
    assert len(d) == before - 1


def test_ace_king_is_blackjack():
    h = Hand()
    h.add_card(Card("A", "S"))
    h.add_card(Card("K", "H"))
    assert h.value == 21
    assert h.is_blackjack


def test_two_aces_is_12_not_22():
    h = Hand()
    h.add_card(Card("A", "S"))
    h.add_card(Card("A", "H"))
    assert h.value == 12          # one ace must drop from 11 to 1


def test_soft_seventeen():
    h = Hand()
    h.add_card(Card("A", "S"))
    h.add_card(Card("6", "H"))
    assert h.value == 17
    assert h.is_soft


def test_hard_hand_busts():
    h = Hand()
    for r in ("K", "Q", "5"):
        h.add_card(Card(r, "S"))
    assert h.value == 25
    assert h.is_bust

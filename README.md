# Blackjack Probability & Strategy Analysis

A statistics / probability project that quantifies the **house edge** in blackjack
and the **value of card counting**, using two independent approaches that should
agree with each other:

1. **Exact probability** (combinatorics + recursion)
2. **Monte Carlo simulation**

> The whole point of the project: compute the same quantity *both ways* and show
> they match. That cross-validation is what makes this a rigorous portfolio piece.

This is **not** a playable game — it is an analytical engine + a narrative notebook.

## Reference papers (in the project)
- *Blackjack: the math behind the cards* -> exact combinatorial probabilities (Phase 2)
- *A New ... Card Counting Strategy for Blackjack using Python* (PyCount) -> counting (Phase 6)
- *Thorp (2006)* -> Kelly criterion & bankroll (Phase 7)

## Project structure
```
blackjack-analysis/
├── README.md
├── requirements.txt
├── conftest.py            # makes `src` importable from tests
├── notebooks/
│   └── blackjack_analysis.ipynb   <- your story: explanations, math, plots
└── src/                   <- the engine (you fill in the TODOs here)
    ├── cards.py           Phase 1 — card / deck / hand model
    ├── combinatorics.py   Phase 2 — exact two-card probabilities
    ├── dealer.py          Phase 3 — dealer outcome distribution
    ├── strategy.py        Phase 4 — expected value & basic strategy
    ├── simulation.py      Phase 5 — Monte Carlo engine
    ├── counting.py        Phase 6 — Hi-Lo card counting
    └── kelly.py           Phase 7 — Kelly criterion & bankroll
└── tests/
    └── test_cards.py      <- the spec for Phase 1: make these pass first
```

## How to start
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
pytest                # Phase 1 tests will FAIL until you write cards.py
jupyter lab           # then open notebooks/blackjack_analysis.ipynb
```

## Suggested order (do NOT skip ahead — each phase needs the last)
- [ ] Phase 1 — cards.py  (make `pytest` green)
- [ ] Phase 2 — combinatorics.py  (reproduce the paper's pair table)
- [ ] Phase 3 — dealer.py  (dealer bust % by upcard)
- [ ] Phase 4 — strategy.py  (derive the basic-strategy chart)
- [ ] Phase 5 — simulation.py  (sim edge ~= theoretical edge)
- [ ] Phase 6 — counting.py  (EV rises with the true count)
- [ ] Phase 7 — kelly.py  (bankroll growth: Kelly vs flat)
- [ ] Phase 8 — polish the notebook (narrative, charts, conclusions)

# Blackjack — Probability & Strategy Analysis

A quantitative study of the blackjack house edge, computed two
independent ways — exact combinatorial probability and Monte Carlo
simulation — and validated against each other with χ² hypothesis tests.
Includes basic-strategy derivation, Hi-Lo card counting, and
Kelly-criterion bet sizing.

All simulations are seeded (`random.seed(42)` + `np.random.seed(42)`), so
re-running the notebook produces bit-identical outputs.

---

## What's inside

| Section | Output |
|---------|--------|
| Exact two-card probabilities | Heatmap of opening-total probability across shoe sizes |
| Dealer outcome distribution | Per-upcard final-total heatmap + bust-rate bar chart |
| Expected value & basic strategy | Auto-derived basic-strategy chart (heatmap) |
| Monte Carlo simulation | 30,000-hand canonical run with a running 95% CI band |
| Statistical validation | χ² goodness-of-fit · Sharpe / drawdown · CLT histogram + Q-Q plot |
| Card counting (Hi-Lo) | True-count buckets + flat-vs-ramp betting on the same hands |
| Kelly criterion | Bankroll trajectories (Kelly / half-Kelly / double-Kelly) + risk-of-ruin |

---

## Key findings

- **P(natural blackjack)** decreases from **4.83%** (1 deck) to **4.74%**
  (8 decks) — the deck-removal effect, quantified exactly.
- **Dealer bust rate** peaks at **~42%** when the upcard is 5 or 6 — the
  classical "stiff" cards.
- **Hit/stand-only basic strategy** achieves an edge of **−3.75%** with
  95% CI **[−4.87%, −2.64%]** over 30,000 hands — **1.7× better** than
  mimic-dealer play. (Full basic strategy with doubles/splits would
  reach the textbook −0.5%.)
- **χ² validation** of the Monte Carlo simulator vs the exact
  dealer-distribution recursion **passes** for upcards 2, 5, 6, 10
  (p > 0.05) but **rejects for Ace** (p ≈ 0) — a genuine Ace-removal
  effect between the finite 6-deck shoe and the infinite-deck
  approximation.
- **Central Limit Theorem** confirmed empirically: empirical /
  theoretical standard-error ratio ≈ **1.0**.
- **Kelly fraction** for a 1%-edge counter: **0.77%** of bankroll per
  hand (≈ $7.69 on a $1,000 stake).

---

## Project layout

```
blackjack-analysis/
├── notebooks/
│   └── blackjack_analysis.ipynb     # Main analysis (39 cells, ~50s end-to-end)
├── src/
│   ├── cards.py            # Card / Deck / Hand primitives (soft/hard Ace logic)
│   ├── combinatorics.py    # Exact two-card probabilities
│   ├── dealer.py           # simulate_dealer (MC) + dealer_distribution (exact)
│   ├── strategy.py         # EV computation + basic-strategy table
│   ├── simulation.py       # play_one_hand + run_simulation engine
│   ├── counting.py         # Hi-Lo tags + true count + bet ramp
│   └── kelly.py            # Kelly fraction + bankroll sim + risk of ruin
├── tests/
│   └── test_cards.py
├── conftest.py
├── requirements.txt
└── README.md
```

---

## Quick start

```bash
pip install -r requirements.txt
jupyter lab notebooks/blackjack_analysis.ipynb
```

Then click **Run → Run All Cells**. The notebook runs top-to-bottom in
about 50 seconds. Every output is reproducible thanks to seeded RNGs.

To execute headlessly and embed outputs:

```bash
jupyter nbconvert --to notebook --execute \
    notebooks/blackjack_analysis.ipynb \
    --output blackjack_analysis_executed.ipynb
```

---

## Methodology notes

- **Reproducibility.** The deck shuffle uses Python's `random` module
  (not numpy's), so the notebook seeds *both* `random` and `np.random`
  with 42. Two consecutive `Restart Kernel → Run All` runs produce
  identical output.
- **Canonical dataset.** The Monte Carlo cell collects
  `nets, tcs = collect_run(30_000)` as the single canonical sample.
  That same array is reused by the convergence plot, the validation
  tests, the true-count buckets, and the flat-vs-ramp comparison.
  Runtime assertions guarantee internal consistency
  (e.g. `assert flat_edge == edge`).
- **Strategy scope.** Player decisions are HIT/STAND only — no doubles
  or splits — so the simulated edge sits around −3% rather than the
  textbook −0.5% for full basic strategy.
- **Dealer rule.** S17 by default (dealer stands on all 17s).
  H17 (dealer hits soft 17) is available via the `hit_soft_17=True`
  flag throughout the engine.

---

## Tech

Python · NumPy · pandas · matplotlib · seaborn · SciPy (χ² + Q-Q) · pytest

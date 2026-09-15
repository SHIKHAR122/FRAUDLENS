# FraudLens

**A statistical, fully-explainable anomaly detection system for flagging fraudulent financial transactions — built on classical statistics (z-score, IQR, Benford's Law) and SQL, not black-box ML.**

> **Status: In development.** This is currently a design/build plan, not a finished system. v1 has not been built yet. See [Roadmap](#roadmap) below for what's done vs. planned.

---

## Why this project exists

Most ML-based fraud detection systems are expensive to build, need large labelled datasets, and act as black boxes — which is a real problem in fintech, where compliance and audit teams need to know *exactly why* a transaction was flagged, not just that a model scored it 0.87.

FraudLens deliberately avoids ML in favor of classical, interpretable statistical techniques that are actually used by real auditors and forensic accountants — so every flagged transaction comes with a human-readable reason, not a confidence score.

## How it works

Three independent statistical signals are combined into a single explainable composite risk score per transaction/entity:

| Signal | Technique | What it catches |
|---|---|---|
| **Velocity fraud** | SQL window functions | Multiple rapid transactions from the same entity in a short window |
| **Spending anomaly** | Per-entity z-score + IQR | Transactions unusual relative to that entity's own history |
| **Digit-distribution anomaly** | Benford's Law | Transaction amounts whose leading digits deviate from the expected natural distribution — a technique used to catch fabricated or manipulated values |

Results are visualized in an interactive dashboard (Power BI / Tableau) showing flagged transactions, risk trends, and the Benford's Law comparison chart.

## Tech stack

- **Data layer:** SQL (MySQL/SQLite) for storage and window-function queries
- **Analysis:** Python — Pandas, NumPy for z-score/IQR/Benford's Law computation
- **Visualization:** Power BI / Tableau
- **Environment:** Jupyter Notebook, Git/GitHub

## Design principle: swappable data layer

The detection logic is written against a generic schema (`entity_id`, `tx_timestamp`, `amount` — not dataset-specific column names), so the data source underneath can be swapped without rewriting the detection logic. This is what makes the v1 → v2 upgrade below possible.

## Roadmap

### v1 — Synthetic dataset (PaySim)
- Build and validate the full detection pipeline (velocity, z-score/IQR, Benford's Law, composite risk score) against **PaySim**, a synthetic mobile-money dataset with real origin/destination account fields and labeled fraud.
- Labeled data means v1 produces real precision/recall numbers — used to prove the detection logic actually works before adding the complexity of a live data source.
- *Chosen over the classic Kaggle "Credit Card Fraud Detection" dataset because it has no per-user/account identifier, which the velocity and per-user z-score methods both depend on.*

### v2 — Live data (public blockchain APIs)
- Swap the data layer to pull real, live transactions via the Etherscan API for a seed set of wallet addresses.
- No fraud labels exist for live data, so evaluation shifts to a pseudo-validation approach: checking whether the composite risk score ranks publicly known flagged/scam addresses (via Etherscan's labeled list or chainabuse.com) higher than random addresses.
- "Per-user" becomes "per-wallet-address" — wallets are pseudonymous, not identity-linked, and this is called out explicitly as a limitation rather than glossed over.
- Benford's Law behavior on crypto transaction amounts will be tested empirically rather than assumed to transfer cleanly from fiat-currency fraud literature.

**Upgrade trigger:** v2 is attempted only if v1 is complete and validated with sufficient time remaining before the deadline. v1 is the guaranteed deliverable; v2 is the stretch goal.

## Known limitations

- Statistical thresholds (z-score cutoff, IQR multiplier) are not learned — they're set and tuned manually, which is a deliberate explainability tradeoff, not an oversight.
- v2's evaluation is necessarily weaker than v1's (no ground-truth labels for live data).
- v2 requires sufficient transaction history per wallet before a per-address baseline is statistically meaningful; low-activity addresses are filtered out.

## Requirements

**Hardware:** Intel i5 (10th gen) / Ryzen 5 or better, 8GB RAM minimum (16GB recommended), 10GB free storage. No GPU needed — no ML training involved.

**Software:** Python 3.x, MySQL/SQLite, Power BI or Tableau, modern web browser, stable internet connection (dataset download / live API calls / dashboard publishing).

## Author

Shikhar Sharma — B.Tech CS (Batch 2027), PSIT Kanpur. Built as an individual project; submitted under a team designation for academic formality.
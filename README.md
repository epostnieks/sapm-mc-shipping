# SAPM Monte Carlo — Shipping & Maritime / Flag State Evasion Floor

**Public replication repository for quantitative results in:**

> Postnieks, E. (2026). *Shipping & Maritime (Flag State Evasion Floor).* SAPM Working Paper. SSRN.

This repository provides everything needed to independently reproduce, audit,
and extend the Monte Carlo simulation underlying the paper's core results.
The paper is available on SSRN.

---

## Results (N = 100,000 draws, seed = 42)

| Statistic | Value |
|-----------|-------|
| **β_W median** | **1.34** |
| β_W mean | 1.35 |
| β_W std | 0.14 |
| **90% CI** | **[1.1, 1.6]** |
| 99% CI | [1.1, 1.7] |
| P(β_W < 1) | 0.1870% |
| **ΔW median** | **$1,299.8B/yr** |
| Π (revenue) | $969.0B/yr |

**β_W = 1.34** means the shipping & maritime industry destroys **$1.34 in system
welfare for every $1.00 in revenue** — across 6 channels and 100,000 Monte Carlo draws.

**Classification**: Class 1 — Impossibility

---

## What Is β_W?

```
β_W = ΔW / Π
```

- **ΔW** = total annualized welfare destruction ($B/yr) across all channels
- **Π** = annual industry **revenue** ($B/yr) — not profit

β_W > 1: industry destroys more welfare than it captures in revenue.
β_W > 3: Strong Intractability threshold — reform requires structural replacement.

---

## Quick Start

```bash
git clone https://github.com/epostnieks/sapm-mc-shipping.git
cd sapm-mc-shipping
pip install numpy scipy
python mc_simulation.py
```

Expected output: `β_W median : 1.34` and `ΔW median : $1,299.8B/yr`

---

## Welfare Channels

| Channel | Median ($B/yr) | 90% CI | Distribution |
|---------|---------------|--------|--------------|
| C1_co2_climate_damages | $189.8B | [$150.2B, $239.8B] | Lognormal |
| C2_air_pollution_mortality | $813.7B | [$662.1B, $1,001.5B] | Lognormal |
| C3_scrubber_ecotoxicity | $65.0B | [$52.8B, $80.0B] | Lognormal |
| C4_invasive_species | $81.0B | [$62.4B, $104.9B] | Lognormal |
| C5_underwater_noise | $17.5B | [$12.3B, $24.9B] | Lognormal |
| C6_governance_failure | $126.9B | [$94.9B, $170.0B] | Lognormal |
| **Total ΔW** | **$1,299.8B** | **[$1,097.6B, $1,540.0B]** | Correlated (ρ=0.3) |

---

## Impossibility Floor

The floor β_W ≥ 0.8 cannot be breached by any policy while the
industry continues to operate. In 100,000 draws, only **0.0000%**
fall below this floor — confirming the structural constraint.

## Repository Contents

| File | Description |
|------|-------------|
| `mc_simulation.py` | Self-contained simulation — no private pipeline imports |
| `mc_results.json` | Pre-run results (100K draws, seed=42) — matches paper |
| `mc_histogram.json` | Binned β_W distribution (80 bins) for companion chart |
| `assumptions.md` | Every parameter: value, derivation, source |
| `data_sources.md` | Full citation list for all empirical inputs |

---

## Replication Notes

Results are seeded and deterministic. Tested with:
```
numpy==1.26.4  scipy==1.12.0  Python 3.11.9
```

The `median` and `ci_90` (to 1 decimal) match exactly across compatible versions.

---

## License

CC BY 4.0. Cite as:

> Postnieks, E. (2026). *SAPM Monte Carlo — Shipping & Maritime (Flag State Evasion Floor)*.
> GitHub: epostnieks/sapm-mc-shipping.
> https://github.com/epostnieks/sapm-mc-shipping

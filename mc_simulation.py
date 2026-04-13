#!/usr/bin/env python3
"""
SAPM Monte Carlo Simulation — Shipping & Maritime / Flag State Evasion Floor
==============================================

Reproduces all quantitative results in:

  Postnieks, E. (2026). SAPM Working Paper: Shipping & Maritime (Flag State Evasion Floor).
  Available: SSRN.

This script is self-contained. Dependencies: numpy, scipy only.
Seeded at seed=42 — produces bit-identical results on any machine
with numpy>=1.24, scipy>=1.10.

Usage
-----
  pip install numpy scipy
  python mc_simulation.py

Theory
------
β_W = ΔW / Π  where:
  Π  = annual industry revenue ($B/yr) — never profit
  ΔW = total annualized welfare destruction ($B/yr)
     = Σ_i W_i across all channels, sampled with correlation ρ=0.3

Classification: Class 1 — Impossibility
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats

CONFIG = {
    "paper_id": "shipping",
    "domain_name": "Shipping & Maritime",
    "theorem": "Flag State Evasion Floor",
    "classification": "Class 1 \u2014 Impossibility",
    "seed": 42,
    "n_draws": 100000,
    "correlation_rho": 0.3,
    "private_payoff_B": 969.0,
    "channels": {
        "C1_co2_climate_damages": {
            "dist": "lognormal",
            "low": 150.0,
            "mid": 190.0,
            "high": 240.0,
            "weight": 0.14,
            "description": "~1Gt CO\u2082/yr \u00d7 EPA SCC $190/t. 2.7-3.1% of global emissions. Sources: EPA SCC 2023, IMO GHG Study 2020."
        },
        "C2_air_pollution_mortality": {
            "dist": "lognormal",
            "low": 600.0,
            "mid": 814.0,
            "high": 1000.0,
            "weight": 0.6,
            "description": "250K premature deaths/yr (Sofiev et al. 2018 Nature Comms) \u00d7 $3-4M income-adjusted global VSL. Plus 6.4M childhood asthma cases. Sources: Sofiev et al. 2018, WHO, Lancet."
        },
        "C3_scrubber_ecotoxicity": {
            "dist": "lognormal",
            "low": 50.0,
            "mid": 65.0,
            "high": 80.0,
            "weight": 0.05,
            "description": "35Mt toxic scrubber washwater dumped annually. Compliance arbitrage \u2014 transfers pollution from atmosphere to ocean. Heavy metal bioaccumulation. Sources: ICCT, CSC, IMO MEPC."
        },
        "C4_invasive_species": {
            "dist": "lognormal",
            "low": 60.0,
            "mid": 81.0,
            "high": 105.0,
            "weight": 0.06,
            "description": "Ballast water and biofouling transport of invasive species. $81B/yr global cost. Sources: IMO BWM Convention, Lovell et al., CBD."
        },
        "C5_underwater_noise": {
            "dist": "lognormal",
            "low": 10.0,
            "mid": 17.5,
            "high": 25.0,
            "weight": 0.013,
            "description": "Propeller cavitation noise shrinks cetacean communication space. North Atlantic right whale population decline. Sources: NOAA, IWC, Erbe et al."
        },
        "C6_governance_failure": {
            "dist": "lognormal",
            "low": 90.0,
            "mid": 127.0,
            "high": 170.0,
            "weight": 0.09,
            "description": "IMO capture (31% corporate reps), flag-of-convenience arbitrage (73% tonnage), <2% effective tax (Maersk 1.9% on $18B), OECD shipping exemption, 6,223 abandoned seafarers. Sources: T&E, ITF, OECD, IMO."
        }
    },
    "impossibility_floor": 0.8
}

# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION ENGINE (identical across all SAPM domains)
# ─────────────────────────────────────────────────────────────────────────────

def generate_correlated_draws(config, rng):
    channels = config["channels"]
    n_draws  = config["n_draws"]
    rho      = config["correlation_rho"]
    n_ch     = len(channels)
    corr     = np.full((n_ch, n_ch), rho)
    np.fill_diagonal(corr, 1.0)
    L        = np.linalg.cholesky(corr)
    Z        = rng.standard_normal((n_draws, n_ch))
    Z_corr   = Z @ L.T
    draws    = np.zeros((n_draws, n_ch))
    names    = list(channels.keys())
    for i, (name, p) in enumerate(channels.items()):
        U    = stats.norm.cdf(Z_corr[:, i])
        dist, low, mid, high = p["dist"], p["low"], p["mid"], p["high"]
        if dist == "lognormal":
            sigma = np.log(high / mid) / 1.645
            draws[:, i] = stats.lognorm.ppf(U, s=sigma, scale=mid)
        elif dist == "normal":
            sigma = (high - low) / (2 * 1.645)
            draws[:, i] = stats.norm.ppf(U, loc=mid, scale=sigma)
        elif dist == "triangular":
            c = (mid - low) / (high - low)
            draws[:, i] = stats.triang.ppf(U, c, loc=low, scale=high - low)
        else:
            raise ValueError(f"Unknown distribution: {dist}")
    return draws, names


def build_sensitivity_matrix(config):
    channels = config["channels"]
    names    = list(channels.keys())
    mids     = [channels[n]["mid"] for n in names]
    vsl_idx  = mids.index(max(mids))
    pi       = config["private_payoff_B"]
    matrix   = []
    for vm in [0.5, 0.75, 1.0, 1.25, 1.5]:
        row = {"vsl_multiplier": vm, "values": {}}
        for dc in [0.0, 0.10, 0.20, 0.30, 0.40]:
            total = sum(mids[i] * (vm if i == vsl_idx else 1.0) for i in range(len(names)))
            row["values"][f"dc_{int(dc*100)}pct"] = round(total * (1 - dc) / pi, 2)
        matrix.append(row)
    return matrix


def build_histogram(beta_draws, n_bins=80):
    counts, edges = np.histogram(beta_draws, bins=n_bins)
    return [
        {"bin_low": round(float(edges[i]),3), "bin_high": round(float(edges[i+1]),3),
          "bin_mid": round(float((edges[i]+edges[i+1])/2),3),
          "count": int(counts[i]), "density": round(float(counts[i]/len(beta_draws)),6)}
        for i in range(len(counts))
    ]


def run():
    cfg = CONFIG
    rng = np.random.default_rng(seed=cfg["seed"])
    print(f"SAPM Monte Carlo — {cfg['domain_name']} ({cfg['theorem']})")
    print(f"  N={cfg['n_draws']:,}  seed={cfg['seed']}  ρ={cfg['correlation_rho']}  Π=${cfg['private_payoff_B']:,}B")
    draws, names = generate_correlated_draws(cfg, rng)
    total       = np.sum(draws, axis=1)
    beta        = total / cfg["private_payoff_B"]
    p5, p95     = np.percentile(beta, [5, 95])
    p1, p99     = np.percentile(beta, [1, 99])
    pi_sa       = total - cfg["private_payoff_B"]
    floor       = cfg.get("impossibility_floor")
    p_floor     = float(np.mean(beta < floor)) if floor else None
    ch_stats    = {
        n: {"median": round(float(np.median(draws[:,i])),1),
             "mean":   round(float(np.mean(draws[:,i])),1),
             "p5":     round(float(np.percentile(draws[:,i],5)),1),
             "p95":    round(float(np.percentile(draws[:,i],95)),1),
             "std":    round(float(np.std(draws[:,i])),1)}
        for i, n in enumerate(names)
    }
    results = {
        "paper_id": cfg["paper_id"],
        "domain_name": cfg["domain_name"],
        "theorem": cfg["theorem"],
        "classification": cfg["classification"],
        "seed": cfg["seed"], "n_draws": cfg["n_draws"],
        "n_channels": len(cfg["channels"]),
        "correlation_rho": cfg["correlation_rho"],
        "private_payoff_B": cfg["private_payoff_B"],
        "beta_w": {
            "median": round(float(np.median(beta)),2),
            "mean":   round(float(np.mean(beta)),2),
            "std":    round(float(np.std(beta)),2),
            "p1":  round(float(p1),2), "p5":  round(float(p5),2),
            "p95": round(float(p95),2), "p99": round(float(p99),2),
            "ci_90": [round(float(p5),1), round(float(p95),1)],
            "ci_99": [round(float(p1),1), round(float(p99),1)],
            "p_below_1": round(float(np.mean(beta < 1.0)),6),
            "p_below_1_pct": f"{np.mean(beta < 1.0)*100:.4f}%",
        },
        "impossibility_floor": {
            "floor_value": floor,
            "p_below_floor": round(p_floor,6) if p_floor is not None else None,
            "p_below_floor_pct": f"{p_floor*100:.4f}%" if p_floor is not None else None,
        } if floor else None,
        "welfare_cost": {
            "total_median_B": round(float(np.median(total)),1),
            "total_mean_B":   round(float(np.mean(total)),1),
            "total_p5_B":     round(float(np.percentile(total,5)),1),
            "total_p95_B":    round(float(np.percentile(total,95)),1),
        },
        "pi_sa": {
            "median_B": round(float(np.median(pi_sa)),1),
            "mean_B":   round(float(np.mean(pi_sa)),1),
            "p5_B":     round(float(np.percentile(pi_sa,5)),1),
            "p95_B":    round(float(np.percentile(pi_sa,95)),1),
        },
        "channel_statistics": ch_stats,
        "sensitivity_matrix": build_sensitivity_matrix(cfg),
    }
    bw = results["beta_w"]
    wc = results["welfare_cost"]
    print(f"  β_W median : {bw['median']}")
    print(f"  90% CI     : {bw['ci_90']}")
    print(f"  P(β_W < 1) : {bw['p_below_1_pct']}")
    print(f"  ΔW median  : ${wc['total_median_B']:,.1f}B/yr")
    return results


if __name__ == "__main__":
    results = run()
    out = Path(__file__).parent / "mc_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  Wrote: {out}")
    rng2 = np.random.default_rng(seed=CONFIG["seed"])
    d2, _ = generate_correlated_draws(CONFIG, rng2)
    t2    = np.sum(d2, axis=1)
    b2    = t2 / CONFIG["private_payoff_B"]
    hist  = build_histogram(b2)
    hout  = Path(__file__).parent / "mc_histogram.json"
    hout.write_text(json.dumps(hist, indent=2), encoding="utf-8")
    print(f"  Wrote: {hout}")
    bw = results["beta_w"]
    print(f"\nVerify: beta_w.median = {bw['median']}  ci_90 = {bw['ci_90']}")

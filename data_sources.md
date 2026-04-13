# Data Sources — Shipping & Maritime Monte Carlo Simulation

Channel parameters in `mc_simulation.py` trace to the sources listed here.
The paper (Shipping & Maritime: Flag State Evasion Floor) is available on SSRN and contains the full
reference list and §4 calibration narrative.

---

## Channel Sources

### `C1_co2_climate_damages`

~1Gt CO₂/yr × EPA SCC $190/t. 2.7-3.1% of global emissions. Sources: EPA SCC 2023, IMO GHG Study 2020.

*Full citations: paper §4 (available SSRN).*

### `C2_air_pollution_mortality`

250K premature deaths/yr (Sofiev et al. 2018 Nature Comms) × $3-4M income-adjusted global VSL. Plus 6.4M childhood asthma cases. Sources: Sofiev et al. 2018, WHO, Lancet.

*Full citations: paper §4 (available SSRN).*

### `C3_scrubber_ecotoxicity`

35Mt toxic scrubber washwater dumped annually. Compliance arbitrage — transfers pollution from atmosphere to ocean. Heavy metal bioaccumulation. Sources: ICCT, CSC, IMO MEPC.

*Full citations: paper §4 (available SSRN).*

### `C4_invasive_species`

Ballast water and biofouling transport of invasive species. $81B/yr global cost. Sources: IMO BWM Convention, Lovell et al., CBD.

*Full citations: paper §4 (available SSRN).*

### `C5_underwater_noise`

Propeller cavitation noise shrinks cetacean communication space. North Atlantic right whale population decline. Sources: NOAA, IWC, Erbe et al.

*Full citations: paper §4 (available SSRN).*

### `C6_governance_failure`

IMO capture (31% corporate reps), flag-of-convenience arbitrage (73% tonnage), <2% effective tax (Maersk 1.9% on $18B), OECD shipping exemption, 6,223 abandoned seafarers. Sources: T&E, ITF, OECD, IMO.

*Full citations: paper §4 (available SSRN).*

---

## Industry Revenue (Π)

The private payoff Π = $969.0B/yr is global annual industry revenue.
Source: paper §2 and §4. See paper §DA-1 (Decision Audit Field 7) for full
revenue source documentation.

---

## SAPM Framework

- Postnieks, E. (2026). *The Private Pareto Theorem*. SAPM Foundation Paper. SSRN.
- Postnieks, E. (2026). *Shipping & Maritime (Flag State Evasion Floor)*. SAPM Working Paper. SSRN.

---

## Distribution Methodology

- Iman, R. L., & Conover, W. J. (1982). A distribution-free approach to
  inducing rank correlation among input variables. *Communications in
  Statistics — Simulation and Computation*, 11(3), 311–334.
- Cooke, R. M. (1991). *Experts in Uncertainty*. Oxford University Press.

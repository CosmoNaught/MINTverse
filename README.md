# MINTverse

**MINTverse** is a small, fast toolkit for malaria intervention modelling — from simulation to ML emulation — built across R and Python. It lets you **ingest** _malariasimulation_ outputs, **estimate** EIR/cases from routine data, and **emulate** scenarios in seconds for decision support. [WEBSITE](https://CosmoNaught.github.io/MINTverse) CURRENTLY UNDER DEVELOPMENT! 

---

## Core Libraries

1. **[MINTs](https://github.com/CosmoNaught/MINTs)** _(COMING SOON)_ — Malaria Intervention Simulator, primary database generator and agent-based system wrapper.
2. **[segMINT](https://github.com/CosmoNaught/segMINT)** — Ingest large *malariasimulation* outputs, build DuckDBs, and plot/query results fast.
3. **[MINTed](https://github.com/CosmoNaught/MINTed)** — Documentation, tutorials, and reproducible examples for the ecosystem.
4. **[estiMINT](https://github.com/CosmoNaught/estiMINT)** — ML models to estimate initial **EIR** and annual **cases/1000** from surveillance + coverage.
5. **[MINTe](https://github.com/CosmoNaught/minte)** — Python RNN forecaster/emulator (GRU/LSTM) for prevalence & cases with CLI + API.
6. **[MINTer](https://github.com/CosmoNaught/MINTer)** — Orchestrator for full MINTverse simulation pipelines and scenario runs. R emulator for prevalence/cases with pre‑trained LSTM/GRU; integrates with *malariasimulation*. 

---

## Support Libraries

- **[spearMINT](https://github.com/CosmoNaught/spearMINT)** — Shared utilities, experiment helpers, and developer tooling for MINTverse R based packages.
- **[pepperMINT](https://github.com/CosmoNaught/pepperMINT)** _(COMING SOON)_ —  Shared utilities, experiment helpers, and developer tooling for MINTverse Python based packages.

---

### Notes
- Items marked **COMING SOON** are planned and may be private or under active development.
- All repositories are under **CosmoNaught** on GitHub

## Architecture

![MINTverse architecture](./architecture.svg)
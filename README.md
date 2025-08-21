
<div align="center">

# MINTverse

**200,000× faster.**  
**96 hours → 90 seconds.**  
From simulation to ML emulation — decisions at the speed of thought.

[**Website**](https://CosmoNaught.github.io/MINTverse) · [**Docs (WIP)**](https://CosmoNaught.github.io/MINTverse) · **London • Imperial College London**

</div>

---

<div align="center">

### Why MINTverse

**Ingest. Estimate. Emulate.**  
One toolkit across **R** and **Python** to go from raw *malariasimulation* outputs to live, queryable dashboards and ML surrogates — fast.

</div>

---

## ✨ What you get

- **Ingest at scale** — turn bulky *malariasimulation* outputs into a lean, queryable store (DuckDB-ready).
- **Estimation models** — infer **EIR** and **cases/1000** from routine surveillance + coverage.
- **Emulators** — GRU/LSTM forecasters that run **in seconds** for scenario planning.
- **End-to-end orchestration** — reproducible pipelines from simulation to decision support.
- **Built for speed** — CPU/GPU-aware, minimal overhead, designed to ship.

---

## 🧭 Ecosystem

> Core libraries live under **CosmoNaught** on GitHub. Items marked **COMING SOON** are planned or in private development.

| Package | What it does | Status |
|---|---|---|
| **[MINTs](https://github.com/CosmoNaught/MINTs)** | Malaria Intervention **Simulator** — primary DB generator & agent-based wrapper. | **COMING SOON** |
| **[segMINT](https://github.com/CosmoNaught/segMINT)** | Ingest large *malariasimulation* outputs, build **DuckDBs**, plot/query fast. | ✅ Stable (active) |
| **[MINTed](https://github.com/CosmoNaught/MINTed)** | Docs, tutorials, and reproducible examples for the ecosystem. | ✅ Stable (active) |
| **[estiMINT](https://github.com/CosmoNaught/estiMINT)** | ML to estimate **EIR** and annual **cases/1000** from surveillance + coverage. | 🚧 Growing |
| **[MINTe](https://github.com/CosmoNaught/minte)** | Python **RNN** forecaster/emulator (GRU/LSTM) for prevalence & cases with CLI + API. | ✅ Active |
| **[MINTer](https://github.com/CosmoNaught/MINTer)** | Orchestrator for full pipelines & scenarios; R emulator (pre‑trained GRU/LSTM); integrates with *malariasimulation*. | ✅ Active |

**Support**

- **[spearMINT](https://github.com/CosmoNaught/spearMINT)** — Shared utilities & experiment helpers for R packages.  
- **[pepperMINT](https://github.com/CosmoNaught/pepperMINT)** — Shared utilities for Python packages. **COMING SOON**


---

## 🧱 Architecture

The ecosystem is modular: **simulate → ingest → estimate → emulate → orchestrate**.

![MINTverse architecture](./architecture.svg)

---

## 🧪 Design principles

- **Simple first.** Opinionated defaults; escape hatches everywhere.  
- **Fast by design.** Columnar storage, vectorized ops, and GPU where it counts.  
- **Reproducible.** Deterministic pipelines, documented seeds, and versioned data.  
- **Composable.** Small libraries that play well together (and alone).

---

## 📌 Status & roadmap

- [x] Core ingestion (segMINT)  
- [x] Python emulator (MINTe)  
- [x] Orchestration glue (MINTer)  
- [x] Public docs site polish (MINTed)  
- [ ] Public Simulator wrapper (MINTs)  
- [ ] Python utilities (pepperMINT)

---

## 🙌 Acknowledgements

Built from the ground up for public health decision‑making.  
Made possible by the help of all the wonderful people and hard work across the **MRC Centre for Global Infectious Disease Analysis** at **Imperial College London**.

---

<div align="center">

**MINTverse** — designed for researchers, engineered for impact.  
Questions? Reach out via the website above.

</div>

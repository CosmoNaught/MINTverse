<div align="center">

# MINTverse

**12 minutes → 12 milliseconds (≈60,000×).**  
From agent-based simulation to neural emulation — decisions faster than the blink of an eye.

[**Website**](https://CosmoNaught.github.io/MINTverse) · [**Docs**](https://CosmoNaught.github.io/MINTverse/docs) · **London • Imperial College London**

</div>

---

<div align="center">

### Why MINTverse

**Ingest. Estimate. Emulate.**  
One toolkit across **R** and **Python** to go from raw *malariasimulation* outputs to live, queryable dashboards and ML surrogates — fast.

</div>


---

## ✨ What you get

- **Ingest at scale** — turn bulky *malariasimulation* outputs into a lean, queryable **DuckDB** store.
- **Estimation models** — infer **EIR** and **cases/1000** from routine surveillance + coverage.
- **Emulators** — GRU/LSTM surrogates that run **in milliseconds** for scenario planning.
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

## ⚡ Benchmarks (reproducible)

| Metric | Claim | Test setup |
|---|---:|---|
| Per‑simulation latency | **12 ms** | PyTorch→CUDA, batch=1, fp16 |
| Speedup vs ABM | **≈60,000×** | 12 min ABM → 12 ms emulation |
| Throughput | **100 sims/sec** | Consumer GPU (e.g., RTX 4070/3080) |
| Fit accuracy | **R² = 0.998** | 250k sequences, held‑out eval |

---

## 🔒 Security & data integrity

- Deterministic seeds and version‑pinned pipelines for reproducibility.
- Data stays local by default; no PII is required.
- Optional hashed run manifests for audit trails (`runs/manifest.json`).

---

## 📚 Cite MINTverse

If you use MINTverse in academic or policy work, please cite:

```bibtex
@software{mintverse_2025,
  author  = {Santoni, Cosmo},
  title   = {MINTverse: Neural Emulation for Infectious Disease Models},
  year    = {2025},
  url     = {https://CosmoNaught.github.io/MINTverse},
  note    = {Version 0.8.0}
}
```

---

## 🤝 Contributing

- Open issues with the corresponding MINTverse package.
- Please add/extend tests and docs for any new behavior.

---

## 🙌 Acknowledgements

Built from the ground up for public health decision‑making.  
Made possible by the help of all the wonderful people and hard work across the **MRC Centre for Global Infectious Disease Analysis** at **Imperial College London**.

---

<div align="center">

**MINTverse — designed for researchers, engineered for impact.**  
Questions? Open an issue or reach out via the website above.

</div>
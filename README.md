<div align="center">

# MINTverse

**12 minutes → 12 milliseconds (≈125,000×).**  
From agent-based simulation to neural emulation — decisions faster than the blink of an eye.

[**Website**](https://CosmoNaught.github.io/MINTverse) · [**Docs**](https://github.com/CosmoNaught/MINTverse) · **London • Imperial College London**

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

## ⚡ Benchmarks (summary)

| Metric | Claim | Test setup |
|---|---:|---|
| Per‑simulation latency | **12 ms** | PyTorch→CUDA, batch=1, fp16 |
| Speedup vs ABM | **≈125,000×** | 12 min ABM → 12 ms emulation |
| Throughput | **100 sims/sec** | Consumer GPU (e.g., RTX 4070/3080) |
| Fit accuracy | **R² = 0.998** | 250k sequences, held‑out eval |

> **Details:** See [full benchmark methodology](#benchmark-methodology).

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

## Appendix

## Benchmark methodology

**Emulator (LSTM) timings.**  
`run_benchmarks(run_sizes = {1,2,4,8,16,32,64,128,256,512}, cpu_cores = {1,2,4,8,16}, gpu_ids = {0}, model_types = {LSTM}, repeats = 9, discard = 1, warmup_gpu_runs = 3)`

**ABM (MalariaSim) timings.**  
`run_benchmarks_malariasim(run_sizes = {1,2,4,8,16}, cpu_cores = {1,2,4}, sim_reps = 8, repeats = 1, discard = 0, scenarios_dir = "benchmark_out/scenarios")`

**Run definition & comparability.**  
- ABM: one “run” = **8 stochastic replicates per scenario** (`sim_reps = 8`) executed sequentially; reported wall time is for the full 8-rep bundle.  
- Emulator: one “run” = one full-horizon forward pass per scenario.  
- Both systems share the **same time horizon** and the **same scenarios** (MalariaSim reuses the emulator’s saved CSVs in `benchmark_out/scenarios/N_*.csv`) for 1:1 comparability.

**CPU/GPU setup.**  
- CPU-single: `torch.set_num_threads(1)`  
- CPU-parallel: `future::multisession` with chunking ≈ `N/(2×workers)`  
- GPU: single device (`CUDA_VISIBLE_DEVICES=0`) with 3 warm-up runs; **no multi-GPU**.

**Statistics.**  
- Emulator results are **p50 (median)** across 9 repetitions with the **fastest repetition discarded**.  
- ABM used a lighter harness (`repeats = 1`), so CIs are not reported.

**Example anchors from raw runs.**  
- ABM (CPU, N=1) **1,414.762 s** (≈23.6 min) vs LSTM-GPU (N=1) **0.012 s** → **117,897×**  
- ABM (CPU, N=16) **22,366.091 s** (≈6.21 h) vs LSTM-GPU **0.168 s** → **133,131×**

**Environment capture.**  
Full environment (OS; R/Python/Torch/CUDA; CPU/GPU model; core counts) is captured per run in `benchmark_out/environment_*.json`.

**Deterministic configuration.**  
`torch.backends.cudnn.deterministic = TRUE`, `torch.backends.cudnn.benchmark = FALSE`.  
A non-deterministic “turbo” profile (`benchmark = TRUE`) exists for exploratory runs but is **not** used for the reported numbers unless explicitly stated.

**Hardware (single-machine, laptop class).**  
Intel Core Ultra 9 185H (16C/22T), 62 GiB LPDDR5-7467, NVIDIA RTX 3500 Ada (12 GiB VRAM), Fedora Linux 41 (kernel 6.15.7), NVIDIA driver 575.64.03.  
ABM CPU workers are capped (≤4) to avoid thermal throttling on laptop CPUs; replicates are executed sequentially because each replicate takes ~3–5 minutes and we deploy/consume 8-rep bundles operationally. We can provide alternative “equal-budget” ABM runs (e.g., higher-core CPU or cloud) on request to show how ABM wall-clock changes under greater parallelism.

**Data pipeline (DuckDB).**  
Simulation outputs are flattened from RDS and materialised into a single DuckDB table (`simulation_results`) in memory by default, with optional persistence to a `.duckdb` file via `write_database()`. Training/validation queries run locally (no external DB), with `PRAGMA threads` and `PRAGMA memory_limit` set per machine. Query shapes use window functions and aggregations; derived targets (*prevalence*, *cases per 1000*) are computed at load time.  
*Empirical performance (full corpus ≈ 574,095,360 rows; DuckDB v1.1.3-dev165; Intel Core Ultra 9 185H, 62 GiB RAM; `threads=16`, `memory_limit='24GB'`):*  
p50 ≈ **0.50 s** for `COUNT(*)`, **1.46 s** for a 30-day aggregated cases query (`GROUP BY`), and **11.4 s** for a 7-step rolling prevalence window.  
<sub>Note: `COUNT(*)` may benefit from metadata; the aggregation/window figures reflect typical workloads.</sub>

---

## Glossary

- **ABM** — Agent-Based Model.
- **LSTM / GRU** — Recurrent neural network architectures (Long Short-Term Memory / Gated Recurrent Unit).
- **R²** — Coefficient of determination.
- **p50** — Median (50th percentile).
- **CI** — Confidence interval.
- **sMAPE** — Symmetric Mean Absolute Percentage Error.
- **MAE / RMSE / MSE** — Mean Absolute Error / Root Mean Squared Error / Mean Squared Error.
- **Bias** — Mean(pred − true).
- **CUDA** — NVIDIA’s GPU compute platform.
- **VRAM** — GPU memory.
- **DuckDB** — In-process analytical database (single file or in-memory).
- **PRAGMA** — DuckDB engine settings (e.g., `threads`, `memory_limit`).
- **HFT** — High-Frequency Trading (latency reference point).

---

<div align="center">

**MINTverse — designed for researchers, engineered for impact.**  
Questions? Open an issue or reach out via the website above.

</div>
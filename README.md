<div align="center">

# MINTverse

**Malaria intervention modelling from Python.**

[**Documentation**](https://cosmonaught.github.io/MINTverse)

</div>

---

## What MINTverse is

MINTverse is two Python packages, estiMINT and stateMINT. A single call, `run_scenarios`, runs them end to end.

| Package | Import | What it does |
|---|---|---|
| [estiMINT](https://github.com/mrc-ide/estiMINT-python) | `estimint` | Maps a measured prevalence to the entomological inoculation rate (EIR), relates EIR to the human biting rate (HBR), and estimates how EIR shifts when mosquito density changes. |
| [stateMINT](https://github.com/mrc-ide/stateMINT) | `stateMINT` | Emulates the individual-based model. Given a setting and an intervention package, returns the prevalence and case trajectories over the campaign. |

`stateMINT` is trained on a large library of runs of an individual-based malaria
transmission model of the same lineage as
[`malariasimulation`](https://mrc-ide.github.io/malariasimulation/). The simulation
takes minutes per scenario, and the emulator reproduces its output in milliseconds.

`estimint` clamps out-of-range covariates and raises nothing, so a setting outside the training
range still returns an answer. The documentation gives the ranges.

## Install

```bash
pip install "estimint[scenarios]"
```

Both packages require Python 3.12 or newer, and the command above installs both. You
install `mintstate` but import `stateMINT`. A GPU is optional
(`pip install "mintstate[gpu]"`, CUDA 12). On a CPU a scenario costs about 6 ms in a
batch, and about 1 ms on a GPU.

## Example

The example below considers a district at 45% under-5 prevalence, with 70%
pyrethroid-only net coverage and 30% pyrethroid resistance, and compares three options
for the next campaign.

```python
from estimint import Scenario, EirTarget, run_scenarios

setting = dict(
    res_use=0.30, Q0=0.85, phi=0.80, seasonal=0.0, irs=0.0,
    eir_target=EirTarget(0.45, "prevalence"), py_only=0.70,
)

results = run_scenarios([
    Scenario(name="withdraw", **setting),
    Scenario(name="like-for-like", **setting, itn_future=0.70, net_type_future="pyrethroid_only"),
    Scenario(name="switch to PBO", **setting, itn_future=0.70, net_type_future="pyrethroid_pbo"),
])

print(results[["name", "eir_baseline", "prev_y9", "prev_endline", "cases_endline"]])
```

```text
            name  eir_baseline   prev_y9  prev_endline  cases_endline
0       withdraw     31.960129  0.456028      0.498149       2.127164
1  like-for-like     31.960129  0.456028      0.483688       2.433113
2  switch to PBO     31.960129  0.456028      0.470118       2.412444
```

All three scenarios start from the same baseline EIR of 31.96, so the differences
between rows come only from the campaign. Each row also carries `prevalence` and
`cases` as 157-element arrays of fortnightly values spanning three years before the
campaign and three years after.

The `_future` fields describe the campaign, not the status quo. If `net_type_future`
and `itn_future` are omitted, the nets are *withdrawn* at the campaign, which is what
the first scenario above does deliberately.

## Run it in Colab

A companion notebook runs the whole pipeline in the browser, with no local install. It builds
four net campaigns in one region, plots the prevalence and case trajectories, totals the cases
each upgrade averts, sweeps mosquito density, and exports the results to CSV.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CosmoNaught/MINTverse/blob/main/MINTverse-tutorial.ipynb)

## Documentation

<https://cosmonaught.github.io/MINTverse>

The documentation is seven chapters, running from a standing start in Python through to
the internals of the two packages.

## Cite MINTverse

```bibtex
@software{santoni2026mintverse,
  author = {Santoni, Cosmo and Thapar, Anmol},
  title  = {MINTverse: estiMINT and stateMINT for malaria intervention modelling},
  year   = {2026},
  url    = {https://github.com/CosmoNaught/MINTverse}
}
```

## Licence

MIT. See [LICENSE](LICENSE).

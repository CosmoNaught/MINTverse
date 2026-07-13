"""Export malariasimulation ground truth for the docs figures.

    python misc/export_truth.py

Run this by hand, once, on a machine with the simulation database. It is not part of the
render. Quarto reads the CSVs it writes, so the docs never depend on DuckDB, and `duckdb` is
deliberately absent from pyproject.toml for that reason. Install it into the render venv only
when you need to re-export:

    uv pip install duckdb --python .venv/bin/python

For each of three held-out parameter sets it writes four series. The simulator's own
stochastic runs and their average are the ground truth. The pipeline series is what a user
gets, a measured year-9 prevalence inverted to an EIR by estiMINT and then run forward by
stateMINT. The emulator series is stateMINT given the simulator's own EIR, which separates
the cost of the inversion from the cost of the emulation.

Ported from statemint_estimint_test/edge_case_validation.py, narrowed to three cases and
with the mosquito-density sweep removed.
"""

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, "/home/cosmo/Documents/Repos/statemint_estimint_test")
import common as C  # noqa: E402
import emulator as E  # noqa: E402
from estimint.run import run_xgb_model  # noqa: E402
from estimint.storage import load_xgb_model  # noqa: E402

# common.py points at a network mount. The MINT_DATA copy is the same database.
DB = "/home/cosmo/Documents/Repos/MINT_DATA/malaria_simulations_4096.duckdb"
EDGE_CASES = f"{C.OUTPUTS}/edge_cases_tagged.csv"
OUT = Path("data/truth")

# Three parameter sets held out of training on both the prevalence and the cases split, so
# every trajectory below is a setting the emulator never saw. They span a seasonal setting
# under nets, a perennial setting under spraying, and a perennial setting under both.
CASES = [16, 20, 27]


def pick_cases() -> pd.DataFrame:
    edge = pd.read_csv(EDGE_CASES).set_index("case_id")
    for cid in CASES:
        row = edge.loc[cid]
        assert "train" not in (row.prev_split, row.cases_split), f"case {cid} is in training"
    return edge.loc[CASES].reset_index()


def main() -> int:
    model = load_xgb_model()  # prevalence -> EIR
    cases = pick_cases()
    print(f"{len(cases)} held-out cases selected")

    con = duckdb.connect(DB, read_only=True)
    con.execute("PRAGMA memory_limit='8GB';")
    con.execute("PRAGMA threads=4;")

    long_rows, meta_rows = [], []

    for _, case in cases.iterrows():
        cid, param, desc = int(case.case_id), int(case.parameter_index), case.description
        true_eir = float(case.actual_eir)
        print(f"\ncase {cid}: {desc}  (param {param}, split {case.prev_split})")

        for predictor in ("prevalence", "cases"):
            tcol = predictor
            sims = [r[0] for r in con.execute(
                f"SELECT DISTINCT simulation_index FROM {C.TABLE_NAME} "
                f"WHERE parameter_index={param} ORDER BY 1").fetchall()]

            all_y, df0 = [], None
            for s in sims:
                d = C.fetch_sim(con, param, s, predictor)
                if len(d) == 0:
                    continue
                if df0 is None:
                    df0 = d
                all_y.append(d[tcol].values.astype(np.float32))
            if df0 is None:
                continue

            n = min(len(y) for y in all_y)
            avg_y = np.mean([y[:n] for y in all_y], axis=0)
            years = (df0["abs_timesteps"].values[:n] - C.INTERVENTION_DAY) / 365.0

            # estiMINT inverts the year-9 prevalence into the EIR the user would deploy with.
            prev_y9 = C.prev_y9_from_df(df0)
            before = df0[df0.abs_timesteps < C.INTERVENTION_DAY]
            row_b = before.iloc[-1] if len(before) else df0.iloc[0]
            cov_xgb = dict(
                prev_y9=prev_y9,
                dn0_use=float(row_b["dn0_use"]),
                Q0=float(case.actual_Q0),
                phi_bednets=float(case.actual_phi),
                seasonal=1.0 if "Seasonal" in desc else 0.0,
                itn_use=float(row_b["itn_use"]),
                irs_use=float(row_b["irs_use"]),
            )
            est_eir = float(run_xgb_model(pd.DataFrame({k: [v] for k, v in cov_xgb.items()}), model)[0])

            covs = [
                E.covars_from_scenario_row(df0, desc, eir=est_eir, Q0=cov_xgb["Q0"],
                                           phi=cov_xgb["phi_bednets"], lsm=float(case.actual_lsm)),
                E.covars_from_scenario_row(df0, desc, eir=true_eir, Q0=cov_xgb["Q0"],
                                           phi=cov_xgb["phi_bednets"], lsm=float(case.actual_lsm)),
            ]
            preds = E.predict(covs, predictor)
            pipeline = C.align_pred(preds[0], n)
            emulated = C.align_pred(preds[1], n)

            y2 = C.year2_index(n)
            mae_pipe, _ = C.mae_rmse(pipeline[y2:], avg_y[y2:])
            mae_emu, _ = C.mae_rmse(emulated[y2:], avg_y[y2:])

            def add(series, values, run_id=""):
                for yr, v in zip(years, values):
                    long_rows.append(dict(case_id=cid, predictor=predictor, series=series,
                                          run_id=run_id, years_from_campaign=round(float(yr), 4),
                                          value=round(float(v), 6)))

            for i, y in enumerate(all_y):
                add("run", y[:n], run_id=str(i))
            add("malariasim", avg_y)
            add("pipeline", pipeline)
            add("emulator", emulated)

            meta_rows.append(dict(
                case_id=cid, predictor=predictor, description=desc,
                split=case.prev_split if predictor == "prevalence" else case.cases_split,
                true_eir=round(true_eir, 4), est_eir=round(est_eir, 4),
                prev_y9=round(float(prev_y9), 4), n_runs=len(all_y),
                mae_pipeline=round(mae_pipe, 5), mae_emulator=round(mae_emu, 5),
            ))
            print(f"  {predictor:10s} runs={len(all_y):2d}  true EIR {true_eir:6.2f} -> "
                  f"est {est_eir:6.2f}   MAE pipeline {mae_pipe:.4f}  emulator {mae_emu:.4f}")

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(long_rows).to_csv(OUT / "edge_cases.csv", index=False)
    pd.DataFrame(meta_rows).to_csv(OUT / "edge_cases_meta.csv", index=False)
    print(f"\nwrote {OUT}/edge_cases.csv ({len(long_rows)} rows) and edge_cases_meta.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())

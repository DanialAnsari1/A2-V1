# -------------------------------------------------
# EDIT THIS FILE FOR TASK C ONLY.
# Main script for the operation. For Task C you may edit this file
# to set up, run, and time your experiments; your Task A, B, and D
# code must still work with the original version, because that is
# how it is marked.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

import sys

if sys.version_info < (3, 13):
    print("[ERROR] Python 3.13 or higher is required.")
    print(f"        You are running Python {sys.version_info.major}."
          f"{sys.version_info.minor}.{sys.version_info.micro}")
    print("        Please upgrade your Python installation and try again.")
    sys.exit(1)

from utils.timer import start, stop
from utils.operation_utils import (
    setup,
    build_fold,
    run_mst_solver,
    run_loader,
    run_visualiser,
)

# -------------------------------------------------------------------
# Task C experiment (Danial Ansari, s4119075).
# Run with:  python initiateOperation.py --experiment <base_config>.json
# The base config supplies the fixed settings (firewall range etc.);
# the values below override what the experiment varies or holds fixed.
# -------------------------------------------------------------------
import csv
import gc
import json
import random
import statistics

EXP_NUM_NODES = 200                     # |V| held fixed
EXP_DENSITIES = ([0.0]                                    # bare tree
                 + [round(0.01 * k, 2) for k in range(2, 11)]   # sparse
                 + [round(0.1 * k, 1) for k in range(2, 10)]    # middle
                 + [0.95, 1.0])                                 # dense
EXP_SEEDS = [11, 22, 33, 44, 55, 66, 77, 88]   # networks per density
# Robustness check: does the ranking hold at a larger |V|?
EXP_CHECK_NODES = 400
EXP_CHECK_DENSITIES = [0.0, 0.02, 0.05, 0.1, 0.5, 0.9, 1.0]
EXP_CHECK_SEEDS = EXP_SEEDS[:4]
EXP_REPEATS = 15                        # interleaved timing rounds
EXP_MAX_FIREWALLS = 100                 # held fixed for every run
EXP_COMBOS = [("kruskals", "list"), ("kruskals", "matrix"),
              ("prims", "list"), ("prims", "matrix")]
EXP_CSV = "visuals/task_c_results.csv"


def edges_for_density(num_nodes: int, d: float) -> int:
    """
    Converts a target density into a connection count, clamped to the
    connected range [|V|-1, |V|(|V|-1)/2].

    @param num_nodes: |V|.
    @param d: Target density in [0, 1].
    @returns: The number of connections |E|.
    """
    max_e = num_nodes * (num_nodes - 1) // 2
    return max(num_nodes - 1, min(max_e, round(d * max_e)))


def time_combos(runs: dict, rng: random.Random) -> dict:
    """
    Times several solver calls on the same network, interleaved: every
    round runs each call once, in a freshly shuffled order, so a burst
    of background load slows all of them alike instead of one whole
    block. One untimed warm-up of each comes first; garbage collection
    is paused while a call is timed. Only the solver call is timed (it
    includes its own get_edges / get_neighbours calls), never the
    construction of the graph.

    @param runs: name -> zero-argument callable running one solver.
    @param rng: Random source for the shuffles.
    @returns: name -> (minimum, median) seconds over EXP_REPEATS rounds.
              The minimum is the least-disturbed run, since background
              noise can only ever add time.
    """
    for call in runs.values():
        call()                                      # warm-up
    times = {name: [] for name in runs}
    names = list(runs)
    for _ in range(EXP_REPEATS):
        rng.shuffle(names)
        for name in names:
            gc.collect()
            gc.disable()
            t0 = start()
            runs[name]()
            times[name].append(stop(t0))
            gc.enable()
    return {n: (min(t), statistics.median(t)) for n, t in times.items()}


def run_experiment(base_config_path: str) -> None:
    """
    Density sweep for Task C. For every density and seed, builds the
    SAME network once as a list and once as a matrix (same seed, so the
    same connections and firewalls), checks all four combinations find
    the same MST total, times them interleaved, and writes one CSV row
    per (density, seed, combination).

    @param base_config_path: Path to a valid base configuration file.
    @returns: None
    """
    from fold.the_fold import TheFold
    from mst.prims import prims
    from mst.kruskals import kruskals
    solvers = {"prims": prims, "kruskals": kruskals}

    with open(base_config_path) as f:
        base = json.load(f)
    order_rng = random.Random(2026)
    rows = []
    sweeps = [(EXP_NUM_NODES, d, EXP_SEEDS) for d in EXP_DENSITIES]
    sweeps += [(EXP_CHECK_NODES, d, EXP_CHECK_SEEDS)
               for d in EXP_CHECK_DENSITIES]
    for v, d, seeds in sweeps:
        e = edges_for_density(v, d)
        actual_d = e / (v * (v - 1) / 2)
        for seed in seeds:
            cfg = dict(base, seed=seed, num_databricks=v - 3, num_edges=e,
                       max_firewalls=EXP_MAX_FIREWALLS, run_loader=False,
                       visualise=False, print_struct=False)
            graphs = {gt: TheFold(dict(cfg, graph_type=gt)).get_graph()
                      for gt in ("list", "matrix")}
            totals = {solvers[s](graphs[g])[1] for s, g in EXP_COMBOS}
            assert len(totals) == 1, "combinations disagree on MST total"
            runs = {(s, g): (lambda s=s, g=g: solvers[s](graphs[g]))
                    for s, g in EXP_COMBOS}
            for (s, g), (t_min, t_med) in time_combos(runs, order_rng).items():
                rows.append({"V": v, "E": e, "density": round(actual_d, 4),
                             "seed": seed, "solver": s, "graph": g,
                             "min_s": t_min, "median_s": t_med})
        print(f"  |V|={v}  d={actual_d:.3f}  |E|={e:>6}  done")

    with open(EXP_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  wrote {len(rows)} rows to {EXP_CSV}")


def plot_experiment(out_path: str = "visuals/task_c_density.png") -> None:
    """
    Plots the Task C sweep from EXP_CSV: run-time against density for
    the four combinations. Each point is the median over the networks
    (seeds) of each network's minimum run; bars span the interquartile
    range over the networks. Left: the full density range. Right: the sparse band
    d <= 0.1, where the ranking changes.

    @param out_path: Where to save the figure.
    @returns: None
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from collections import defaultdict

    data = defaultdict(list)
    with open(EXP_CSV) as f:
        for row in csv.DictReader(f):
            if int(row["V"]) != EXP_NUM_NODES:
                continue                        # check sweep: table only
            key = (row["solver"], row["graph"])
            data[key].append((float(row["density"]),
                              float(row["min_s"]) * 1000))

    style = {("kruskals", "list"):   ("#0072B2", "-",  "o", "Kruskal + list"),
             ("kruskals", "matrix"): ("#0072B2", "--", "s", "Kruskal + matrix"),
             ("prims", "list"):      ("#D55E00", "-",  "o", "Prim + list"),
             ("prims", "matrix"):    ("#D55E00", "--", "s", "Prim + matrix")}

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, d_max in zip(axes, (1.0, 0.1)):
        for key, (colour, ls, marker, label) in style.items():
            by_d = defaultdict(list)
            for d, ms in data[key]:
                if d <= d_max + 1e-9:
                    by_d[d].append(ms)
            ds = sorted(by_d)
            med = [statistics.median(by_d[d]) for d in ds]
            q = [statistics.quantiles(by_d[d], n=4) for d in ds]
            lo = [m - qq[0] for m, qq in zip(med, q)]
            hi = [qq[2] - m for m, qq in zip(med, q)]
            ax.errorbar(ds, med, yerr=[lo, hi], color=colour, ls=ls,
                        marker=marker, ms=4, lw=1.4, capsize=2,
                        label=label)
        ax.set_xlabel("density d = |E| / (|V|(|V|-1)/2)")
        ax.set_ylabel("run-time (ms)")
        ax.grid(alpha=0.3)
        ax.set_xlim(0, d_max * 1.02)
        ax.set_ylim(bottom=0)
    axes[0].set_title(f"(a) Full range, |V| = {EXP_NUM_NODES}")
    axes[1].set_title("(b) Sparse band, d ≤ 0.1")
    axes[0].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    print(f"  saved {out_path}")


def main():
    """
    Entry point for the operation.

    Runs each stage in order:
        1. Load and validate the configuration
        2. Build The Fold
        3. Find the safe path (MST — Task B)
        4. Load the freighter (Task D)
        5. Draw the operation report (optional)

    The timer wraps the whole program — use utils/timer.py to time
    individual stages for your Task C experiments.
    """
    program_start = start()

    if len(sys.argv) == 3 and sys.argv[1] == "--experiment":
        run_experiment(sys.argv[2])                 # Task C
        plot_experiment()
        return
    if len(sys.argv) == 2 and sys.argv[1] == "--plot":
        plot_experiment()                           # re-plot saved CSV
        return

    if len(sys.argv) != 2:
        print("Usage: python initiateOperation.py <config_file>.json")
        sys.exit(1)

    config = setup(sys.argv[1])
    fold = build_fold(config)
    mst_result = run_mst_solver(config, fold)
    load_result = run_loader(config, fold)
    run_visualiser(config, fold, mst_result, load_result)

    elapsed = stop(program_start)
    print("==========================================")
    print("   Operation complete. Vanish, Slyce.")
    print(f"   Total time: {elapsed:.4f}s")
    print("==========================================")


if __name__ == "__main__":
    main()

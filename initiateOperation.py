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

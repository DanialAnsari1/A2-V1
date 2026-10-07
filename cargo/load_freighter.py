# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK D.
# The freighter loader.
#
# __author__ = 'your_name_here'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from fold.databrick import Databrick

# A memo maps a sub-problem key to a (records, weight) pair: the most
# records achievable for that sub-problem, and the smallest weight that
# achieves it. Keys are (i, c) for the weight-only loader and (i, c, l)
# for the weight-and-volume loader.
Memo = dict[tuple, tuple[int, int]]


def load_freighter(bricks: list[Databrick],
                   weight_capacity: int,
                   volume_capacity: int | None = None
                   ) -> tuple[list[Databrick], int, int, int, Memo]:
    """
    Chooses which databricks to load onto the freighter.

    This function is the entry point the tests and the operation report
    call. It dispatches to one of the two loaders you implement below,
    depending on whether the volume limit is switched on. You should not
    need to change this function.

    @param bricks: The recovered databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @param volume_capacity: The freighter's volume limit in litres, or
                            None for no volume limit.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load;
              - int: total records freed;
              - int: total weight loaded;
              - int: total volume loaded;
              - Memo: the sub-problem answers computed along the way.
    """
    if volume_capacity is None:
        selected, memo = load_weight_only(bricks, weight_capacity)
    else:
        selected, memo = load_weight_and_volume(
            bricks, weight_capacity, volume_capacity)

    value = sum(b.records for b in selected)
    weight = sum(b.weight for b in selected)
    volume = sum(b.volume for b in selected)
    return selected, value, weight, volume, memo


def load_weight_only(bricks: list[Databrick],
                     weight_capacity: int
                     ) -> tuple[list[Databrick], Memo]:
    """
    The single-limit loader (Task D.1): choose the load that frees the
    most records within the weight limit, breaking ties toward the
    lightest load.

    @param bricks: The databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load;
              - Memo: the sub-problem answers, keyed (i, c).

    HINT: a sub-problem is "the best you can do using the first i bricks
    with c kg of capacity left" --- decide whether brick i is taken.
    """
    # IMPLEMENT ME! (Task D.1)
    # Return the chosen databricks and the memo of sub-problems you
    # computed. The empty return below is a valid placeholder so the
    # program runs before you start: it loads nothing.
    return [], {}


def load_weight_and_volume(bricks: list[Databrick],
                           weight_capacity: int,
                           volume_capacity: int
                           ) -> tuple[list[Databrick], Memo]:
    """
    The dual-limit loader (Task D.2): choose the load that frees the
    most records within both the weight and volume limits, breaking ties
    toward the lightest load.

    @param bricks: The databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @param volume_capacity: The freighter's volume limit in litres.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load;
              - Memo: the sub-problem answers, keyed (i, c, l).

    HINT: this is load_weight_only with one extra coordinate to track.
    """
    # IMPLEMENT ME! (Task D.2)
    # Return the chosen databricks and the memo of sub-problems you
    # computed. The empty return below is a valid placeholder so the
    # program runs before you start: it loads nothing.
    return [], {}

# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK D.
# The freighter loader.
#
# __author__ = 'Danial Ansari (s4119075)'
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
    return _solve(bricks, (weight_capacity,))


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
    # TODO (Task D.2): add the volume coordinate.
    return [], {}


def _costs(brick: Databrick, dims: int) -> tuple[int, ...]:
    """
    The capacity a databrick uses up in each active dimension.

    @param brick: The databrick.
    @param dims: 1 for weight only, 2 for weight and volume.
    @returns: (weight,) or (weight, volume).
    """
    return (brick.weight,) if dims == 1 else (brick.weight, brick.volume)


def _better(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """
    Whether load summary a beats load summary b: more records wins;
    equal records are broken toward the lighter load.

    @param a: A (records, weight) pair.
    @param b: A (records, weight) pair.
    @returns: True if a is strictly better than b.
    """
    return a[0] > b[0] or (a[0] == b[0] and a[1] < b[1])


def _solve(bricks: list[Databrick],
           capacities: tuple[int, ...]) -> tuple[list[Databrick], Memo]:
    """
    Top-down (memoised) dynamic programming for the 0/1 loading problem
    with one capacity (weight) or two (weight and volume).

    Sub-problem key (i, *rem): the best load using only the first i
    databricks when rem capacity is left in each dimension. Its answer
    is (records, weight): the most records achievable, and the smallest
    weight achieving them. Recurrence, with brick i the last of the i:

        best(0, rem)  = (0, 0)
        best(i, rem)  = better of
            skip: best(i-1, rem)
            take: best(i-1, rem - cost_i) + (v_i, w_i)   if cost_i <= rem

    Only sub-problems reachable from best(N, capacities) are computed.
    An explicit stack replaces recursion so large hauls cannot exceed
    Python's recursion limit.

    @param bricks: The databricks to choose from.
    @param capacities: (C,) or (C, L).
    @returns: The chosen databricks (in input order) and the memo.
    """
    dims = len(capacities)
    memo: Memo = {}
    if any(cap < 0 for cap in capacities):
        return [], memo                    # nothing can ever fit
    costs = [_costs(b, dims) for b in bricks]

    def children(key: tuple) -> tuple[tuple, tuple | None]:
        """The skip sub-problem, and the take sub-problem if brick fits."""
        i, rem = key[0], key[1:]
        skip = (i - 1,) + rem
        cost = costs[i - 1]
        if all(c <= r for c, r in zip(cost, rem)):
            take = (i - 1,) + tuple(r - c for r, c in zip(rem, cost))
            return skip, take
        return skip, None

    root = (len(bricks),) + tuple(capacities)
    stack = [root]
    while stack:
        key = stack[-1]
        if key in memo:
            stack.pop()
            continue
        if key[0] == 0:                    # base case: no bricks left
            memo[key] = (0, 0)
            stack.pop()
            continue
        skip, take = children(key)
        missing = [k for k in (skip, take) if k is not None and k not in memo]
        if missing:
            stack.extend(missing)          # solve children first
            continue
        stack.pop()
        best = memo[skip]
        if take is not None:
            brick = bricks[key[0] - 1]
            r, w = memo[take]
            taken = (r + brick.records, w + brick.weight)
            if _better(taken, best):
                best = taken
        memo[key] = best

    # Walk back from the root: brick i was taken exactly when skipping
    # it does not reproduce the stored (records, weight) answer.
    selected: list[Databrick] = []
    key = root
    while key[0] > 0:
        skip, take = children(key)
        if memo[key] == memo[skip]:
            key = skip
        else:
            selected.append(bricks[key[0] - 1])
            key = take
    selected.reverse()
    return selected, memo

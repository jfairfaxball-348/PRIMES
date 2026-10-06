"""Small deterministic helpers for converting exact counts into scan summaries."""

from __future__ import annotations

from collections import Counter
from collections.abc import Hashable
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


def ranked_counts(counter: Counter[T], limit: int = 20) -> list[tuple[T, int]]:
    """Return deterministic count ranking: descending count, then repr key."""
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return sorted(counter.items(), key=lambda item: (-item[1], repr(item[0])))[:limit]


def occupancy_extrema(
    blocks: list[tuple[int, int, int]],
) -> dict[str, tuple[int, int, int] | None]:
    """Return first minimum and maximum occupancy blocks."""
    if not blocks:
        return {"minimum": None, "maximum": None}

    minimum = min(blocks, key=lambda row: (row[2], row[0]))
    maximum = min(blocks, key=lambda row: (-row[2], row[0]))
    return {"minimum": minimum, "maximum": maximum}

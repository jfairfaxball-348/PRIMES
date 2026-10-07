from __future__ import annotations

from experiments.E009_unit_action_cover_shapes import factor_exact, reconstruct_factors
from experiments.E009_unit_action_cover_shapes_runtime import factor_exact_runtime
from primes_lab.core import sieve


def test_runtime_factorization_matches_frozen_exact_trial_division() -> None:
    base = sieve(400)
    for value in (1, 11, 121, 143, 11**2 * 13, 3**3 * 5**2 * 11, 99991):
        expected = factor_exact(value, base)
        actual, reconstruction_ok, canonical_ok = factor_exact_runtime(value, base, 400)
        assert actual == expected
        assert reconstruction_ok is True
        assert canonical_ok is True
        assert reconstruct_factors(actual) == value


def test_runtime_factorization_fails_closed_on_insufficient_support() -> None:
    factors, reconstruction_ok, canonical_ok = factor_exact_runtime(101 * 103, [2, 3, 5, 7], 7)
    assert factors == ((10403, 1),)
    assert reconstruction_ok is True
    assert canonical_ok is False

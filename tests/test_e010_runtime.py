from collections import Counter

import pytest

from experiments.E010_quadratic_surd_cycle_shapes_runtime import (
    FAMILY_ORDER,
    OCCURRENCE_FLOOR,
    POPULATION_FLOOR,
    PROMOTION_CAP,
    CycleProfileError,
    IntegerRootDomainError,
    PrematureRepeatError,
    RecurrenceArithmeticError,
    RecurrenceQuotientError,
    apply_duplicate_suppression,
    cycle_signatures,
    cycle_signatures_from_denominators,
    denominator_cycle,
    enrichment_numerator,
    exact_nonsquare_root,
    family_row,
    frequency_table,
    mode_summary,
    multiplicity_profile,
    record_nonterminal_state,
    recurrence_step,
    validate_quotient_bounds,
)


def test_exact_isqrt_bracketing_and_square_rejection() -> None:
    assert exact_nonsquare_root(2) == 1
    assert exact_nonsquare_root(58_999_999) == 7681
    with pytest.raises(IntegerRootDomainError, match="nonsquare"):
        exact_nonsquare_root(121)


def test_integer_recurrence_arithmetic_and_quotient_bounds() -> None:
    assert recurrence_step(x=7, a0=2, m=0, d=1, a=2) == (2, 3, 1)
    assert recurrence_step(x=7, a0=2, m=2, d=3, a=1) == (1, 2, 1)
    with pytest.raises(RecurrenceArithmeticError, match="positive"):
        recurrence_step(x=2, a0=1, m=0, d=2, a=1)
    with pytest.raises(RecurrenceArithmeticError, match="divisible"):
        recurrence_step(x=10, a0=3, m=0, d=3, a=1)
    validate_quotient_bounds(numerator=7, denominator=3, quotient=2)
    with pytest.raises(RecurrenceQuotientError, match="bounds"):
        validate_quotient_bounds(numerator=7, denominator=3, quotient=1)


def test_first_canonical_terminal_state_and_denominator_cycle() -> None:
    assert denominator_cycle(2) == (1,)
    assert denominator_cycle(3) == (2, 1)
    assert denominator_cycle(7) == (3, 2, 3, 1)
    with pytest.raises(IntegerRootDomainError):
        denominator_cycle(9)


def test_nonterminal_repeat_rejection() -> None:
    seen = {(0, 1)}
    record_nonterminal_state(seen, m=2, d=3)
    with pytest.raises(PrematureRepeatError, match="repeated"):
        record_nonterminal_state(seen, m=2, d=3)


def test_denominator_multiplicity_profile_and_l1_l4_identities() -> None:
    cycle = (3, 2, 3, 1)
    assert multiplicity_profile(cycle) == (2, 1)
    assert cycle_signatures_from_denominators(cycle) == {
        "L1": 4, "L2": 3, "L3": 2, "L4": (2, 1)
    }
    assert cycle_signatures(2) == {"L1": 1, "L2": 1, "L3": 1, "L4": (1,)}
    assert cycle_signatures(3) == {"L1": 2, "L2": 2, "L3": 1, "L4": (2,)}
    assert tuple(cycle_signatures(7)) == FAMILY_ORDER
    with pytest.raises(CycleProfileError):
        multiplicity_profile(())


def test_canonical_frequency_ordering() -> None:
    scalar = frequency_table("L1", Counter({4: 1, 2: 3, 3: 2}))
    assert [row["signature"] for row in scalar] == [2, 3, 4]
    profile = frequency_table("L4", Counter({(2, 1): 3, (1, 2): 2, (2,): 1}))
    assert [row["signature"] for row in profile] == [[1, 2], [2], [2, 1]]


def test_strict_unique_mode_and_tie_handling() -> None:
    unique = mode_summary("L1", Counter({3: 5, 2: 4, 1: 1}))
    assert unique == {
        "prime_mode_count": 5,
        "prime_maximizing_signatures": [3],
        "runner_up_count": 4,
        "strict_unique_prime_mode": True,
    }
    tied = mode_summary("L4", Counter({(2, 1): 5, (1, 2): 5, (1,): 1}))
    assert tied["prime_maximizing_signatures"] == [[1, 2], [2, 1]]
    assert tied["runner_up_count"] == 5
    assert tied["strict_unique_prime_mode"] is False


def test_exact_enrichment_positive_zero_negative() -> None:
    assert enrichment_numerator(n_prime=3, n_composite=1, N_prime=10, N_composite=10) == 20
    assert enrichment_numerator(n_prime=1, n_composite=1, N_prime=10, N_composite=10) == 0
    assert enrichment_numerator(n_prime=1, n_composite=2, N_prime=10, N_composite=10) == -10


def test_population_and_occurrence_floors() -> None:
    assert POPULATION_FLOOR == 1000
    assert OCCURRENCE_FLOOR == 32
    passing, _ = family_row(
        family="L1", prime_counter=Counter({9: 32, 8: 31}),
        composite_counter=Counter({9: 1}), N_prime=1000, N_composite=1000,
    )
    assert passing["population_floor_passed"]
    assert passing["occurrence_floor_passed"]
    assert passing["enrichment_passed"]
    failing, _ = family_row(
        family="L1", prime_counter=Counter({9: 31, 8: 30}),
        composite_counter=Counter({9: 1}), N_prime=999, N_composite=1000,
    )
    assert not failing["population_floor_passed"]
    assert not failing["occurrence_floor_passed"]


def _eligible_row(family: str, signature: object) -> dict[str, object]:
    return {
        "family": family, "prime_frequency_table": [], "composite_frequency_table": [],
        "prime_mode_count": 40, "prime_maximizing_signatures": [signature],
        "runner_up_count": 39, "strict_unique_prime_mode": True,
        "unique_mode_composite_count": 1, "unique_mode_enrichment_numerator": 1,
        "population_floor_passed": True, "occurrence_floor_passed": True,
        "enrichment_passed": True, "mechanically_eligible": False,
    }


def test_duplicate_suppression_family_order_and_cap() -> None:
    rows = [
        _eligible_row("L1", 4), _eligible_row("L2", 3),
        _eligible_row("L3", 2), _eligible_row("L4", [2, 1]),
    ]
    sets = {
        "L1": frozenset({0, 1}), "L2": frozenset({0, 1}),
        "L3": frozenset({2}), "L4": frozenset({3}),
    }
    promotions = apply_duplicate_suppression(rows, sets)
    assert [row["family"] for row in promotions] == ["L1", "L3", "L4"]
    assert rows[0]["mechanically_eligible"] is True
    assert rows[1]["mechanically_eligible"] is False
    assert len(promotions) <= PROMOTION_CAP == 4


def test_native_runtime_matches_python_reference_exactly() -> None:
    for value in (2, 3, 7, 13, 23, 94, 991, 1009, 10007):
        assert cycle_signatures(value) == cycle_signatures_from_denominators(denominator_cycle(value))

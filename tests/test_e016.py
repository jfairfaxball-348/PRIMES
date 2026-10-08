"""E016 D16 only: no real prime generator is entered by any test."""
import copy
import importlib.util
from collections import Counter
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "experiments" / "E016_central_binomial_odd_valuation_carry_shapes.py"
SPEC = importlib.util.spec_from_file_location("e016", PATH)
e = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(e)


def test_provenance_metadata_not_prime_data():
    assert len(e.EARLY_ROLES) == 53
    assert len(e.LATER_ROLES) == 15
    assert len(e.historical_intervals()) == 74
    assert e.audit_partition() == (380, 30, 150)
    assert len(e.R210) == 48
    assert e.ROLES[4][1] == 2 * e.ROLES[1][1]


def test_legendre_terms_and_independent_carry_check():
    for x in range(0, 140):
        for q in e.BASES:
            power = q
            total = 0
            while power <= 2 * x:
                term = 2 * x // power - 2 * (x // power)
                assert term in (0, 1)
                total += term
                power *= q
            assert total == e.valuation(x, q) == e.carry_count(x, q)
    assert e.valuation(1, 3) == 0
    assert (e.valuation(5, 3), e.valuation(5, 5), e.valuation(5, 7)) == (2, 0, 1)
    assert any(e.valuation(x, 3) > 4 for x in range(1, 2000))
    for x in (0, 1, 2, 5, 100, 2000):
        s = e.signatures(x)
        assert s[0] == sum(s[2]) and s[1] == sum(v > 0 for v in s[2])
        assert all(0 <= v <= 4 for v in s[2])


def test_finite_complete_domains_and_lexical_ranking():
    assert [len(x) for x in e.DOMAINS] == [13, 4, 125]
    assert e.DOMAINS[0] == tuple(range(13))
    assert e.DOMAINS[1] == tuple(range(4))
    assert e.DOMAINS[2][0] == (0, 0, 0)
    assert e.DOMAINS[2][-1] == (4, 4, 4)
    assert tuple(sorted(e.DOMAINS[2])) == e.DOMAINS[2]
    assert e.strict_mode(Counter({(0, 0, 1): 7, (0, 1, 0): 5}), e.DOMAINS[2]) == ((0, 0, 1), 7, 5)
    assert e.strict_mode(Counter({(0, 0, 1): 7, (0, 1, 0): 7}), e.DOMAINS[2]) == (None, 7, 7)
    assert e.strict_mode(Counter(), e.DOMAINS[2]) == (None, 0, 0)


def synthetic_tables(target_p=22, target_c=12, labels_per_class=30):
    """Invented labels and signatures, no prime testing and no high numbers."""
    pp, cc = [Counter() for _ in range(3)], [Counter() for _ in range(3)]
    pb = [[Counter() for _ in range(48)] for _ in range(3)]
    cb = [[Counter() for _ in range(48)] for _ in range(3)]
    supports = [dict() for _ in range(3)]
    # Two alternate coarsening-consistent full-domain triples.
    triples = ((1, 0, 0), (0, 0, 0), (1, 1, 0))
    for r in range(48):
        for isprime in (True, False):
            target = target_p if isprime else target_c
            if not 0 <= target <= labels_per_class:
                raise ValueError("fabricated counts")
            rem = labels_per_class - target
            counts = (target, rem // 2, rem - rem // 2)
            for triple, n in zip(triples, counts):
                sigs = (sum(triple), sum(v > 0 for v in triple), triple)
                for i, sig in enumerate(sigs):
                    (pp if isprime else cc)[i][sig] += n
                    (pb if isprime else cb)[i][r][sig] += n
                    if isprime:
                        prior = len(supports[i].get(sig, set()))
                        supports[i].setdefault(sig, set()).update({r * 1000 + v for v in range(prior, prior + n)})
    return pp, cc, pb, cb, [labels_per_class] * 48, [labels_per_class] * 48, supports


def test_signed_enrichment_mixing_and_positive_class_controls():
    pp, cc, pb, cb, np_by, nc_by, supports = synthetic_tables()
    assert e.exact_enrichment(22, 12, 30, 30) == 300
    assert e.exact_enrichment(12, 22, 30, 30) == -300
    assert e.exact_enrichment(5, 5, 30, 30) == 0
    assert e.class_metrics((1, 0, 0), pb[2], cb[2], np_by, nc_by) == (48, 48)
    rows, promos = e.summarize(pp, cc, pb, cb, np_by, nc_by, supports)
    assert len(rows) == 3
    assert rows[0]["aggregate_enrichment_numerator"] > 0
    assert all(row["positive_class_count"] == 48 and row["mixed_class_count"] == 48 for row in rows)
    assert [p["family"] for p in promos] == ["T1"]  # three equal exact supports suppressed
    assert rows[0]["mechanically_eligible"]
    assert not rows[1]["mechanically_eligible"] and not rows[2]["mechanically_eligible"]


def test_class_positive_threshold_30_and_mixed_36_exact():
    pp, cc, pb, cb, np_by, nc_by, supports = synthetic_tables()
    # Class metrics inspect all 48 classes, not a favourable subset.
    target = (1, 0, 0)
    for r in range(48):
        cb[2][r][target] = 10 if r < 30 else 25
    assert e.class_metrics(target, pb[2], cb[2], np_by, nc_by) == (48, 30)
    for r in range(12):
        pb[2][r][target] = np_by[r]
    assert e.class_metrics(target, pb[2], cb[2], np_by, nc_by)[0] == 36
    for r in range(13):
        pb[2][r][target] = np_by[r]
    assert e.class_metrics(target, pb[2], cb[2], np_by, nc_by)[0] == 35


def test_floor_failures_ties_and_empty_discovery():
    pp, cc, pb, cb, np_by, nc_by, supports = synthetic_tables()
    rows, promos = e.summarize(pp, cc, pb, cb, [9] * 48, nc_by) if False else (None, None)
    # A self-consistent smaller synthetic population fails both 1000 and class-10 floors.
    p2, c2, pb2, cb2, pn, cn, sup2 = synthetic_tables(8, 3, 9)
    rows, promos = e.summarize(p2, c2, pb2, cb2, [9] * 48, [9] * 48, sup2)
    assert promos == []
    assert all(not r["population_floor_passed"] and not r["class_floor_passed"] for r in rows)
    blank = [Counter() for _ in range(3)]
    by = [[Counter() for _ in range(48)] for _ in range(3)]
    rows, promos = e.summarize(blank, blank, by, by, [0] * 48, [0] * 48, [{}, {}, {}])
    assert promos == [] and all(r["unique_mode_signature"] is None for r in rows)
    assert all(r["prime_mode_count"] == r["highest_competing_count"] == 0 for r in rows)


def test_support_set_equality_not_cardinality():
    assert e.select_duplicates([("T1", {1, 2}), ("T2", {2, 1}), ("T3", {3, 4})]) == ["T1", "T3"]
    assert e.select_duplicates([("T1", {1, 2}), ("T2", {3, 4}), ("T3", {5, 6})]) == ["T1", "T2", "T3"]
    with pytest.raises(ValueError):
        e.select_duplicates([("T1", [1, 2])])


def sample_payload():
    blank = [Counter() for _ in range(3)]
    by = [[Counter() for _ in range(48)] for _ in range(3)]
    rows, promos = e.summarize(blank, blank, by, by, [0] * 48, [0] * 48, [{}, {}, {}])
    return dict(experiment="E016", implementation_commit="a" * 40,
                band=dict(name="D16", range=[86_000_000, 87_000_000], interval_semantics="half-open"),
                partition=[dict(name=n, range=[a, b], role=role) for n, a, b, role in e.ROLES],
                parameters=e.PARAMETERS, generation_plan=e.expected_plan(),
                anchor_summary=dict(wheel_anchor_count=0, prime_count=0, composite_count=0,
                                    prime_counts_by_R210=[0] * 48, composite_counts_by_R210=[0] * 48),
                validation=dict.fromkeys(e.VALIDATION_KEYS, 0), families=rows, promotions=promos)


def test_narrow_empty_schema_byte_determinism_and_extra_fields():
    p = sample_payload()
    raw = e.serialize(p)
    assert raw.endswith(b"\n") and raw == e.serialize(copy.deepcopy(p))
    assert b'"promotions": []' in raw
    for change in (lambda x: x.update(extra="forbidden"),
                   lambda x: x["validation"].update(plan_failure_count=1),
                   lambda x: x["anchor_summary"]["prime_counts_by_R210"].append(0),
                   lambda x: x["families"][0].update(extra=1),
                   lambda x: x["parameters"].update(valuation_cap=5),
                   lambda x: x["promotions"].append(dict(family="T1"))):
        altered = copy.deepcopy(p)
        change(altered)
        with pytest.raises(ValueError):
            e.serialize(altered)


def test_poison_generator_malformed_and_off_phase_all_exclusions():
    def poison(_):
        raise AssertionError("PRIME GENERATOR ENTERED")

    good = e.expected_plan()
    assert e.validate_plan("D16", good)
    malformed = [None, (), [], good[:1], good + [good[-1]], good[::-1],
                 [good[0], good[0]], [good[1], good[1]],
                 [dict(good[0], stop=9327), good[1]],
                 [dict(good[0], stop=9329), good[1]],
                 [dict(good[0], start=1), good[1]],
                 [dict(good[0], strategy="segmented"), good[1]],
                 [good[0], dict(good[1], start=86_000_001)],
                 [good[0], dict(good[1], stop=86_999_999)],
                 [good[0], dict(good[1], stop=87_000_001)],
                 [good[0], dict(good[1], strategy="whole_prefix")],
                 [good[0], dict(good[1], purpose="base_sieve_support")],
                 [good[0], dict(good[1], high_helper=True)],
                 [dict(good[0], stop=87_000_000), good[1]],
                 [good[0], dict(good[1], start=85_999_999)],
                 [good[0], dict(good[1], start=True)],
                 [good[0], dict(good[1], start=86_000_000.0)]]
    for _, a, b in e.historical_intervals():
        malformed.append([good[0], dict(good[1], start=a, stop=b)])
    for _, a, b, _ in e.ROLES:
        if (a, b) != (86_000_000, 87_000_000):
            malformed.append([good[0], dict(good[1], start=a, stop=b)])
    for a in e.CALIBRATION_STARTS:
        for width in e.WIDTHS:
            malformed.append([good[0], dict(good[1], start=a, stop=a + width)])
    for plan in malformed:
        with pytest.raises(ValueError):
            e.generator_entry("D16", plan, 0, poison)
    for phase in ("H16", "A16", "D15", "", None):
        with pytest.raises(ValueError):
            e.generator_entry(phase, good, 0, poison)
    with pytest.raises(ValueError):
        e.generator_entry("D16", good, 2, poison)
    with pytest.raises(AssertionError, match="PRIME GENERATOR ENTERED"):
        e.generator_entry("D16", good, 0, poison)


def test_unchanged_d16_sole_allowed_plan_and_root():
    assert e.D16_PLAN == (("base_sieve_support", 0, 9328, "whole_prefix"),
                          ("segmented_target", 86_000_000, 87_000_000, "segmented"))
    assert e.isqrt(86_999_999) == 9327
    assert e.audit_partition() == (380, 30, 150)

"""E020 D20-only, frozen noncommutative S3 endpoint-word residue discovery.

Only source-free synthetic preflight is available through self_check(). Prime
entry exists exclusively inside execute_d20(), protected by the entire plan.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
from json import dumps, loads
from math import gcd, isqrt
from pathlib import Path

STATES = ("123", "132", "213", "231", "312", "321")
INDEX = {g: i for i, g in enumerate(STATES)}
IDENTITY, A, B = "123", "213", "231"
R210 = (1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127,
        131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173,
        179, 181, 187, 191, 193, 197, 199, 209)
M = 1_000_000
NEW = (("G20-pre", 102*M, 103*M), ("D20", 103*M, 104*M),
       ("G20-mid", 104*M, 105*M), ("H20", 105*M, 106*M),
       ("A20", 206*M, 207*M))
# Individually named E013 early provenance, frozen integer roles only.
EARLY = (
    ("D0", 0, 1), ("H0", 1, 2), ("E002-S1", 2, 3),
    ("E002-S2", 4, 5), ("E002-S3", 8, 9), ("A0-retired", 10, 11),
    ("E002-S4", 16, 17), ("E002-S5", 32, 33), ("D3", 35, 36),
    ("D4", 39, 40), ("D6", 42, 43), ("H6", 44, 45),
    ("D7", 46, 47), ("H7", 48, 49), ("D8", 50, 51),
    ("D9", 54, 55), ("H9", 56, 57), ("D10", 58, 59),
    ("H10", 60, 61), ("D11", 62, 63), ("H11", 64, 65),
    ("D12", 67, 68),
    ("A1", 33, 34), ("H3", 37, 38), ("H4", 41, 42),
    ("H8", 52, 53), ("A8", 66, 67), ("H12", 69, 70),
    ("A3", 70, 71), ("A4", 78, 79), ("A6", 84, 85),
    ("A7", 92, 93), ("A9", 108, 109), ("A10", 116, 117),
    ("A11", 124, 125), ("A12", 134, 135),
    ("G3-pre", 34, 35), ("G3-post", 36, 37),
    ("G4-pre", 38, 39), ("G4-mid", 40, 41),
    ("G6-mid", 43, 44), ("G7-pre", 45, 46),
    ("G7-mid", 47, 48), ("G8-pre", 49, 50),
    ("G8-mid", 51, 52), ("G9-pre", 53, 54),
    ("G9-mid", 55, 56), ("G10-pre", 57, 58),
    ("G10-mid", 59, 60), ("G11-pre", 61, 62),
    ("G11-mid", 63, 64), ("G12-pre", 65, 66),
    ("G12-mid", 68, 69),
)
FAMILIES = (
    (13, (71, 72, 73, 74, 144)),
    (14, (75, 76, 77, 79, 152)),
    (15, (80, 81, 82, 83, 162)),
    (16, (85, 86, 87, 88, 172)),
    (17, (89, 90, 91, 93, 180)),
    (18, (94, 95, 96, 97, 190)),
    (19, (98, 99, 100, 101, 198)),
)
MAX_STARTS = (128, 256, 512, 1024, 2048, 4096)
WIDTHS = (4096, 16384, 65536, 262144, 1048576)
VALIDATORS = ("plan_failure_count", "interval_exclusion_failure_count",
              "group_definition_failure_count", "word_convolution_failure_count",
              "remainder_bin_failure_count", "wheel_label_partition_failure_count",
              "frequency_conservation_failure_count", "signed_control_failure_count",
              "mode_duplicate_gate_failure_count", "serializer_failure_count")
PLAN = (("base_sieve_support", 0, 10199, "whole_prefix"),
        ("segmented_target", 103*M, 104*M, "direct_segmented"))
PARTITION = tuple((name, lo, hi, "discovery" if name == "D20" else
                   "guard" if name.startswith("G") else
                   "holdout" if name == "H20" else "adversarial")
                  for name, lo, hi in NEW)


def compose(g: str, h: str) -> str:
    return "".join(g[int(c)-1] for c in h)


MUL = tuple(tuple(INDEX[compose(g, h)] for h in STATES) for g in STATES)
BASE = tuple(int(g in (A, B)) for g in STATES)
UNIT = tuple(int(g == IDENTITY) for g in STATES)


def convolution(u: tuple[int, ...], v: tuple[int, ...], modulus: int | None) -> tuple[int, ...]:
    if len(u) != 6 or len(v) != 6:
        raise ValueError("six coefficients required")
    out = [0] * 6
    for i in range(6):
        for j in range(6):
            out[MUL[i][j]] += u[i] * v[j]
    if modulus is not None:
        if type(modulus) is not int or modulus < 1:
            raise ValueError("positive integer modulus required")
        out = [z % modulus for z in out]
    return tuple(out)


def word_power(n: int, modulus: int | None = None) -> tuple[int, ...]:
    if type(n) is not int or n < 0:
        raise ValueError("nonnegative integer exponent")
    accum = UNIT
    base = BASE
    while n:
        if n & 1:
            accum = convolution(accum, base, modulus)
        n >>= 1
        if n:
            base = convolution(base, base, modulus)
    return tuple(z % modulus for z in accum) if modulus else accum


def signature(x: int) -> int:
    if type(x) is not int or x < 1:
        raise ValueError("positive anchor")
    coeff = word_power(x, x)
    assert sum(coeff) % x == pow(2, x, x)
    aa, bb = coeff[INDEX[A]], coeff[INDEX[B]]
    if not (0 <= aa < x and 0 <= bb < x):
        raise AssertionError("noncanonical residue")
    u, v = (2*aa)//x, (2*bb)//x
    if u not in (0, 1) or v not in (0, 1):
        raise AssertionError("half-bin overflow")
    return 2*u+v


def old_roles():
    early = [(name, lo*M, hi*M) for name, lo, hi in EARLY]
    family = [(f"{prefix}{number}{suffix}", lo*M, (lo+1)*M)
              for number, starts in FAMILIES
              for prefix, suffix, lo in zip(("G", "D", "G", "H", "A"),
                                            ("-pre", "", "-mid", "", ""), starts)]
    calibration = [(f"E005-max-{s}", s*M, s*M+1048576) for s in MAX_STARTS]
    return early+family+calibration


def overlap(a, b):
    return a[1] < b[2] and b[1] < a[2]


def audit_intervals():
    old = old_roles()
    new = list(NEW)
    nested = [(f"E005-{s}-{w}", s*M, s*M+w) for s in MAX_STARTS for w in WIDTHS]
    if (len(EARLY), len(old), len(new), len(nested)) != (53, 94, 5, 30):
        raise ValueError("interval role inventory wrong")
    if len(set(v[0] for v in old+new)) != 99:
        raise ValueError("duplicate role name")
    if any(type(lo) is not int or lo >= hi for _, lo, hi in old+new+nested):
        raise ValueError("invalid interval endpoint")
    oo = sum(1 for i, a in enumerate(old) for b in old[i+1:] if overlap(a,b))
    no = sum(1 for a in new for b in old if overlap(a,b))
    nn = sum(1 for i,a in enumerate(new) for b in new[i+1:] if overlap(a,b))
    if (oo, no, nn) != (0, 0, 0):
        raise ValueError("overlapping old/new roles")
    if (len(old)*(len(old)-1)//2, len(old)*len(new), len(new)*(len(new)-1)//2) != (4371,470,10):
        raise ValueError("pairwise audit count mismatch")
    for ni in nested:
        if sum(1 for mx in old if mx[1] <= ni[1] and ni[2] <= mx[2] and mx[0].startswith("E005-max-")) != 1:
            raise ValueError("E005 nested containment failed")
    if sum(overlap(a,b) for a in new for b in nested) != 0 or len(new)*len(nested) != 150:
        raise ValueError("nested disjointness failed")
    if new != [("G20-pre",102*M,103*M),("D20",103*M,104*M),
               ("G20-mid",104*M,105*M),("H20",105*M,106*M),
               ("A20",206*M,207*M)] or new[-1][1] != 2*new[1][1]:
        raise ValueError("new interval mutation")
    if isqrt(104*M-1) != 10198 or not 10198**2 <= 104*M-1 < 10199**2:
        raise ValueError("isqrt drift")
    return True


def poison_validate():
    """Negative entire-plan firewall tests, including every old/nested named role."""
    poisons = [(PLAN[0], ("segmented_target", lo, hi, "direct_segmented"))
               for name, lo, hi in old_roles()+list(NEW)
               if name != "D20"]
    poisons += [(PLAN[0], ("segmented_target", s*M, s*M+w, "direct_segmented"))
                for s in MAX_STARTS for w in WIDTHS]
    poisons += [PLAN[::-1], PLAN[:1], PLAN+(PLAN[1],),
                (("base_sieve_support",0,104*M,"whole_prefix"),PLAN[1]),
                (("base_sieve_support",0,10198,"whole_prefix"),PLAN[1]),
                (("base_sieve_support",0,10200,"whole_prefix"),PLAN[1]),
                (PLAN[0],("segmented_target",103*M,104*M,"whole_prefix")),
                (PLAN[0],("segmented_target",103*M,104*M-1,"direct_segmented")),
                (PLAN[0],("segmented_target",103*M+1,104*M,"direct_segmented")),
                (PLAN[0],("per_anchor_primality_helper",103*M,104*M,"indirect"))]
    for candidate in poisons:
        try:
            validate_plan(candidate)
        except ValueError:
            continue
        raise AssertionError("poison plan admitted")
    for phase in ("H20","A20","G20-pre","G20-mid","D19"):
        try:
            validate_plan(PLAN,phase)
        except ValueError:
            continue
        raise AssertionError("off-phase poison admitted")
    return len(poisons)+5


def validate_plan(requested, phase="D20"):
    audit_intervals()
    if phase != "D20" or type(requested) not in (tuple, list) or len(requested) != 2:
        raise ValueError("off-phase or incomplete generation plan")
    if any(type(row) not in (tuple,list) or len(row) != 4 for row in requested):
        raise ValueError("malformed generator entry")
    if tuple(tuple(row) for row in requested) != PLAN:
        raise ValueError("non-allowlisted generator plan")
    return True


class GeneratorFirewall:
    def __init__(self, plan):
        validate_plan(plan)
        self.plan = plan
        self.index = 0

    def enter(self, purpose, start, stop, strategy):
        validate_plan(self.plan)
        if self.index >= len(PLAN) or (purpose,start,stop,strategy) != PLAN[self.index]:
            raise ValueError("forbidden generator entry or order")
        self.index += 1

    def complete(self):
        validate_plan(self.plan)
        if self.index != 2:
            raise ValueError("incomplete generator sequence")


def base_sieve(stop: int):
    flag = bytearray(b"\x01")*stop
    flag[:2] = b"\x00\x00"
    for p in range(2, isqrt(stop-1)+1):
        if flag[p]:
            flag[p*p:stop:p] = b"\x00" * ((stop-1-p*p)//p+1)
    return [i for i in range(2, stop) if flag[i]]


def segmented_target(start: int, stop: int, bases: list[int]):
    flag = bytearray(b"\x01")*(stop-start)
    for p in bases:
        first = max(p*p, ((start+p-1)//p)*p)
        if first < stop:
            flag[first-start:stop-start:p] = b"\x00" * ((stop-1-first)//p+1)
    return flag


def select_w1(pc, cc, pr, cr, pclass, cclass, support):
    """Fixed 4-state complete-domain mode, exact signed/mixed controls and one cap."""
    if any(len(rows) != 4 for rows in pr+cr) or len(pr) != 48 or len(cr) != 48:
        raise ValueError("invalid class table")
    if len(pc) != 4 or len(cc) != 4 or len(pclass) != 48 or len(cclass) != 48:
        raise ValueError("wrong complete state/class domain")
    np, nc = sum(pc), sum(cc)
    if sum(pclass) != np or sum(cclass) != nc:
        raise ValueError("population conservation")
    if any(sum(pr[i]) != pclass[i] or sum(cr[i]) != cclass[i] for i in range(48)):
        raise ValueError("class conservation")
    top = max(pc)
    winners = [j for j, v in enumerate(pc) if v == top]
    unique = len(winners) == 1
    target = winners[0] if unique else None
    competitor = max((v for j,v in enumerate(pc) if j != target), default=top) if unique else top
    population_ok = np >= 1000 and nc >= 1000
    classes_ok = all(pclass[i] >= 10 and cclass[i] >= 10 for i in range(48))
    occurrence_ok = unique and pc[target] >= 32
    mixed = sum(all((pr[i][target], pclass[i]-pr[i][target],
                     cr[i][target], cclass[i]-cr[i][target])) for i in range(48)) if unique else None
    positive = sum(pr[i][target]*cclass[i] - cr[i][target]*pclass[i] > 0 for i in range(48)) if unique else None
    signed = pc[target]*nc - cc[target]*np if unique else None
    if any(type(x) is not int for x in support):
        raise ValueError("supports must be exact integers")
    # Singleton cap and exact set equality, never hash/cardinality-only dedup.
    retained = []
    if unique and len(set(support)) != len(support):
        raise ValueError("duplicate prime anchor within support")
    eligible = bool(unique and population_ok and classes_ok and occurrence_ok and
                    mixed >= 36 and positive >= 30 and signed > 0)
    if eligible:
        candidate = set(support)
        if not any(candidate == s for s in retained) and len(retained) < 1:
            retained.append(candidate)
    eligible = eligible and len(retained) == 1
    row = dict(family="W1", prime_mode_count=top,
               highest_competing_count=competitor,
               strict_unique_prime_mode=unique, unique_mode_signature=target,
               target_composite_count=cc[target] if unique else None,
               population_floor_passed=population_ok,
               class_floor_passed=classes_ok,
               occurrence_floor_passed=occurrence_ok,
               mixed_class_count=mixed, mixed_class_floor_passed=bool(unique and mixed>=36),
               positive_class_count=positive, positive_class_floor_passed=bool(unique and positive>=30),
               aggregate_enrichment_numerator=signed,
               aggregate_enrichment_positive=bool(unique and signed>0),
               mechanically_eligible=eligible)
    promotions = ([dict(family="W1", target_signature=target,
                        target_prime_count=pc[target], target_composite_count=cc[target],
                        mixed_class_count=mixed, positive_class_count=positive,
                        aggregate_enrichment_numerator=signed)] if eligible else [])
    return row, promotions


def exact_equal_type(left, right):
    """Recursively forbid bool-as-int, list/tuple, and other weak equality."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal_type(left[k],right[k]) for k in left)
    if type(left) is list:
        return len(left)==len(right) and all(exact_equal_type(a,b) for a,b in zip(left,right))
    return left == right


def ensure_keys(o, keys):
    if type(o) is not dict or set(o) != set(keys):
        raise ValueError("unknown or missing JSON key")


def integer(x):
    if type(x) is not int:
        raise ValueError("strict integer required")


def boolean(x):
    if type(x) is not bool:
        raise ValueError("strict boolean required")


def validate_payload(d):
    ensure_keys(d, ("experiment","implementation_commit","band","partition", "parameters",
                    "generation_plan","anchor_summary","validation","families","promotions"))
    if d["experiment"] != "E020" or type(d["implementation_commit"]) is not str or len(d["implementation_commit"]) != 40 or any(c not in "0123456789abcdef" for c in d["implementation_commit"]):
        raise ValueError("invalid pinned implementation")
    ensure_keys(d["band"], ("name","range","interval_semantics"))
    if not exact_equal_type(d["band"], {"name":"D20","range":[103*M,104*M],"interval_semantics":"half-open"}):
        raise ValueError("wrong phase band")
    if type(d["partition"]) is not list or not exact_equal_type(d["partition"], [dict(name=n,range=[lo,hi],role=role) for n,lo,hi,role in PARTITION]):
        raise ValueError("wrong five-role partition")
    param = d["parameters"]
    expected = parameters()
    ensure_keys(param,expected)
    for k,v in expected.items():
        if not exact_equal_type(param[k],v):
            raise ValueError("wrong frozen parameter")
    allowed = [dict(purpose=p,start=s,stop=e,strategy=t) for p,s,e,t in PLAN]
    if type(d["generation_plan"]) is not list or not exact_equal_type(d["generation_plan"],allowed):
        raise ValueError("wrong generation plan")
    for row in d["generation_plan"]:
        ensure_keys(row,("purpose","start","stop","strategy"))
        integer(row["start"]); integer(row["stop"])
    summary = d["anchor_summary"]
    ensure_keys(summary,("wheel_anchor_count","prime_count","composite_count","prime_counts_by_R210","composite_counts_by_R210"))
    for k in ("wheel_anchor_count","prime_count","composite_count"):
        integer(summary[k])
        if summary[k] < 0: raise ValueError("negative population")
    for k in ("prime_counts_by_R210","composite_counts_by_R210"):
        if type(summary[k]) is not list or len(summary[k]) != 48:
            raise ValueError("wrong class shape")
        for n in summary[k]:
            integer(n)
            if n < 0: raise ValueError("negative class population")
    if (sum(summary["prime_counts_by_R210"]) != summary["prime_count"] or
        sum(summary["composite_counts_by_R210"]) != summary["composite_count"] or
        summary["wheel_anchor_count"] != summary["prime_count"]+summary["composite_count"]):
        raise ValueError("population sum mismatch")
    ensure_keys(d["validation"], VALIDATORS)
    for k in VALIDATORS:
        integer(d["validation"][k])
        if d["validation"][k] != 0: raise ValueError("nonzero validator")
    if type(d["families"]) is not list or len(d["families"]) != 1:
        raise ValueError("family cardinality")
    row = d["families"][0]
    ensure_keys(row,("family","prime_mode_count","highest_competing_count","strict_unique_prime_mode",
                     "unique_mode_signature","target_composite_count","population_floor_passed",
                     "class_floor_passed","occurrence_floor_passed","mixed_class_count",
                     "mixed_class_floor_passed","positive_class_count","positive_class_floor_passed",
                     "aggregate_enrichment_numerator","aggregate_enrichment_positive","mechanically_eligible"))
    if row["family"] != "W1": raise ValueError("family name")
    for k in ("prime_mode_count", "highest_competing_count"):
        integer(row[k])
        if row[k] < 0: raise ValueError("negative mode count")
    for k in ("strict_unique_prime_mode","population_floor_passed","class_floor_passed",
              "occurrence_floor_passed","mixed_class_floor_passed","positive_class_floor_passed",
              "aggregate_enrichment_positive","mechanically_eligible"):
        boolean(row[k])
    target_keys = ("unique_mode_signature","target_composite_count","mixed_class_count",
                   "positive_class_count","aggregate_enrichment_numerator")
    if row["strict_unique_prime_mode"]:
        for k in target_keys: integer(row[k])
        if row["unique_mode_signature"] not in range(4) or row["target_composite_count"] < 0 or not 0 <= row["mixed_class_count"] <= 48 or not 0 <= row["positive_class_count"] <= 48:
            raise ValueError("target out of bounds")
    elif any(row[k] is not None for k in target_keys) or any(row[k] for k in ("occurrence_floor_passed","mixed_class_floor_passed","positive_class_floor_passed","aggregate_enrichment_positive","mechanically_eligible")):
        raise ValueError("tie must null all target fields")
    if type(d["promotions"]) is not list or len(d["promotions"]) > 1:
        raise ValueError("promotion cap")
    if bool(d["promotions"]) != row["mechanically_eligible"]:
        raise ValueError("promotion eligibility mismatch")
    for prom in d["promotions"]:
        ensure_keys(prom,("family","target_signature","target_prime_count","target_composite_count",
                         "mixed_class_count","positive_class_count","aggregate_enrichment_numerator"))
        for k,v in prom.items():
            if k != "family": integer(v)
        if prom != {"family":"W1","target_signature":row["unique_mode_signature"],
                    "target_prime_count":row["prime_mode_count"],
                    "target_composite_count":row["target_composite_count"],
                    "mixed_class_count":row["mixed_class_count"],
                    "positive_class_count":row["positive_class_count"],
                    "aggregate_enrichment_numerator":row["aggregate_enrichment_numerator"]}:
            raise ValueError("promotion must equal mode")
    return True


def parameters():
    return dict(width=M,wheel=210,residues_R210=list(R210),group_states=list(STATES),
                composition="(g h)(i)=g(h(i))",identity=IDENTITY,generators=[A,B],
                word_length="anchor",endpoint_states=[A,B],convolution="noncommutative-group-ring",
                remainder_modulus="anchor",joint_half_bins=2,population_floor=1000,
                class_floor=10,occurrence_floor=32,mixed_class_floor=36,
                positive_class_floor=30,strict_global_enrichment=True)


def canonical(d):
    validate_payload(d)
    raw = (dumps(d,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+"\n").encode("ascii")
    if loads(raw) != d or raw != (dumps(loads(raw),sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+"\n").encode("ascii"):
        raise ValueError("noncanonical serializer")
    return raw


def self_check():
    audit_intervals(); validate_plan(PLAN)
    assert poison_validate() == 143
    assert STATES == tuple(sorted(STATES)) and len(INDEX) == 6
    assert compose(IDENTITY,A) == A == compose(A,IDENTITY)
    assert all(compose(g, h) in INDEX for g in STATES for h in STATES)
    assert all(compose(compose(g,h),k)==compose(g,compose(h,k)) for g in STATES for h in STATES for k in STATES)
    for n in range(5):
        brute = Counter()
        for letters in product((A,B),repeat=n):
            state = IDENTITY
            for letter in letters: state=compose(state,letter)
            brute[state]+=1
        direct = tuple(brute[g] for g in STATES)
        assert direct == word_power(n)
        assert sum(direct) == 2**n
        for m in (1,2,3,5,11):
            assert word_power(n,m) == tuple(v%m for v in direct)
        if n < 4:
            via_right = [0]*6
            for g in STATES:
                for h in (A,B): via_right[INDEX[compose(g,h)]]+=direct[INDEX[g]]
            assert tuple(via_right) == word_power(n+1)
    assert len(R210)==48 and R210==tuple(i for i in range(210) if gcd(i,210)==1)
    assert signature(1)==0 and all(signature(x) in range(4) for x in (2,3,4,5,6,7,8,11,29))
    return True


def execute_d20(implementation_commit, outpath):
    self_check()
    # Inspect all positive-plan, old/new/nested exclusion metadata before the LOW call.
    firewall = GeneratorFirewall(PLAN)
    firewall.enter(*PLAN[0])
    bases = base_sieve(PLAN[0][2])
    assert bases and bases[-1] <= 10198
    # The full common wheel population's representation is evaluated before labels.
    rindex = {r:i for i,r in enumerate(R210)}
    all_anchors = [(x,rindex[x%210],signature(x))
                   for x in range(103*M,104*M) if x%210 in rindex]
    if len(all_anchors) != sum(gcd(x,210)==1 for x in range(103*M,104*M)):
        raise ValueError("wheel population mismatch")
    # Re-audit complete plan and exclusions immediately before high entry.
    firewall.enter(*PLAN[1])
    prime_flags = segmented_target(PLAN[1][1],PLAN[1][2],bases)
    firewall.complete()
    pc,cc = [0]*4,[0]*4
    pr,cr = [[0]*4 for _ in range(48)],[[0]*4 for _ in range(48)]
    pclass,cclass = [0]*48,[0]*48
    supports = [[] for _ in range(4)]
    for x,ri,t in all_anchors:
        if prime_flags[x-103*M]:
            pc[t]+=1;pr[ri][t]+=1;pclass[ri]+=1;supports[t].append(x)
        else:
            cc[t]+=1;cr[ri][t]+=1;cclass[ri]+=1
    del all_anchors,prime_flags,bases
    np,nc = sum(pc),sum(cc)
    if np+nc != sum(1 for x in range(103*M,104*M) if gcd(x,210)==1):
        raise ValueError("wheel label loss")
    # The frozen W1 selector sees all four signatures and all 48 exact classes.
    top=max(pc); winning=[t for t in range(4) if pc[t]==top]
    chosen_support = supports[winning[0]] if len(winning)==1 else []
    row,promotions = select_w1(pc,cc,pr,cr,pclass,cclass,chosen_support)
    del supports,pr,cr,pc,cc,chosen_support
    payload = dict(experiment="E020",implementation_commit=implementation_commit,
                   band=dict(name="D20",range=[103*M,104*M],interval_semantics="half-open"),
                   partition=[dict(name=n,range=[lo,hi],role=role) for n,lo,hi,role in PARTITION],
                   parameters=parameters(),
                   generation_plan=[dict(purpose=p,start=s,stop=e,strategy=t) for p,s,e,t in PLAN],
                   anchor_summary=dict(wheel_anchor_count=np+nc,prime_count=np,composite_count=nc,
                                       prime_counts_by_R210=pclass,composite_counts_by_R210=cclass),
                   validation={key:0 for key in VALIDATORS},families=[row],promotions=promotions)
    raw=canonical(payload)
    Path(outpath).write_bytes(raw)
    # Validate entire file from disk without printing or inspecting contents here.
    if Path(outpath).read_bytes()!=raw: raise ValueError("artifact byte write mismatch")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--band",required=True,choices=("D20",))
    parser.add_argument("--code-commit",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    execute_d20(args.code_commit,args.output)


if __name__ == "__main__":
    main()

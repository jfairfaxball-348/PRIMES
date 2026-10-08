"""D1-53: exact frozen E018 D18-only tiling-remainder discovery evaluator.

Do not extend this module to H18/A18 or to a new tiling/signature family.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

W = 1_000_000
Q = 210
R210 = (1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
        61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169,
        173, 179, 181, 187, 191, 193, 197, 199, 209)
M = ((1, 1, 1), (1, 0, 0), (0, 1, 0))
SEED = (2, 1, 1)
ROLE_DATA = (("G18-pre", 94), ("D18", 95), ("G18-mid", 96),
             ("H18", 97), ("A18", 190))
ROLES = tuple((name, start * W, (start + 1) * W) for name, start in ROLE_DATA)
EARLY = (
    ("D0",0),("H0",1),("S1",2),("S2",4),("S3",8),("A0-retired",10),
    ("S4",16),("S5",32),("D3",35),("D4",39),("D6",42),("H6",44),
    ("D7",46),("H7",48),("D8",50),("D9",54),("H9",56),("D10",58),
    ("H10",60),("D11",62),("H11",64),("D12",67),
    ("A1",33),("H3",37),("H4",41),("H8",52),("A8",66),("H12",69),
    ("A3",70),("A4",78),("A6",84),("A7",92),("A9",108),("A10",116),
    ("A11",124),("A12",134),
    ("G3-pre",34),("G3-post",36),("G4-pre",38),("G4-mid",40),
    ("G6-mid",43),("G7-pre",45),("G7-mid",47),("G8-pre",49),
    ("G8-mid",51),("G9-pre",53),("G9-mid",55),("G10-pre",57),
    ("G10-mid",59),("G11-pre",61),("G11-mid",63),("G12-pre",65),
    ("G12-mid",68),
)
LATE = (
    ("G13-pre",71),("D13",72),("G13-mid",73),("H13",74),("A13",144),
    ("G14-pre",75),("D14",76),("G14-mid",77),("H14",79),("A14",152),
    ("G15-pre",80),("D15",81),("G15-mid",82),("H15",83),("A15",162),
    ("G16-pre",85),("D16",86),("G16-mid",87),("H16",88),("A16",172),
    ("G17-pre",89),("D17",90),("G17-mid",91),("H17",93),("A17",180),
)
CAL_STARTS = (128_000_000,256_000_000,512_000_000,1_024_000_000,
              2_048_000_000,4_096_000_000)
CAL_WIDTHS = (4096, 16384, 65536, 262144, 1048576)
HISTORIC = (tuple((name, n*W, (n+1)*W) for name, n in EARLY+LATE)
            + tuple((f"E005-max-{i+1}", s, s+CAL_WIDTHS[-1])
                    for i, s in enumerate(CAL_STARTS)))
NESTED = tuple((f"E005-{i+1}-{w}", s, s+w)
               for i, s in enumerate(CAL_STARTS) for w in CAL_WIDTHS)
D18_PLAN = (
    {"purpose": "base_sieve_support", "start": 0, "stop": 9798,
     "strategy": "whole_prefix"},
    {"purpose": "segmented_target", "start": 95_000_000, "stop": 96_000_000,
     "strategy": "direct_segmented"},
)
VALIDATORS = (
    "plan_failure_count", "domain_partition_failure_count",
    "tiling_recurrence_failure_count", "transfer_matrix_failure_count",
    "residue_bin_failure_count", "support_identity_failure_count",
    "class_label_failure_count", "frequency_mode_failure_count",
    "gate_duplicate_failure_count", "serializer_failure_count",
)
FAMILY_KEYS = frozenset((
    "family", "prime_mode_count", "highest_competing_count",
    "strict_unique_prime_mode", "unique_mode_signature", "target_composite_count",
    "population_floor_passed", "class_floor_passed", "occurrence_floor_passed",
    "mixed_class_count", "mixed_class_floor_passed", "positive_class_count",
    "positive_class_floor_passed", "aggregate_enrichment_numerator",
    "aggregate_enrichment_positive", "mechanically_eligible",
))
PROMO_KEYS = frozenset(("family", "target_signature", "target_prime_count",
                        "target_composite_count", "mixed_class_count",
                        "positive_class_count", "aggregate_enrichment_numerator"))
PARAMETERS = {
    "width": W, "wheel": Q, "residues_R210": list(R210),
    "tile_lengths": [1, 2, 3], "tiling_seed": list(SEED),
    "transfer_matrix": [list(row) for row in M],
    "remainder_modulus": "anchor", "residue_bin_counts": [4, 8],
    "population_floor": 1000, "class_floor": 10, "occurrence_floor": 32,
    "mixed_class_floor": 36, "positive_class_floor": 30,
    "strict_global_enrichment": True,
}


def _overlap(a, b):
    return a[1] < b[2] and b[1] < a[2]


def interval_audit():
    """Named exclusion metadata only: no prime or high-anchor access."""
    assert len(EARLY) == 53 and len(LATE) == 25
    assert len(HISTORIC) == 84 and len(ROLES) == 5 and len(NESTED) == 30
    assert len({name for name, *_ in HISTORIC+ROLES+NESTED}) == 119
    assert len({(a,b) for _,a,b in HISTORIC+ROLES}) == 89
    assert all(a<b for _,a,b in HISTORIC+ROLES+NESTED)
    old_pairs = list(combinations(HISTORIC, 2))
    new_pairs = [(a,b) for a in ROLES for b in HISTORIC] + list(combinations(ROLES,2))
    assert len(old_pairs) == 3486 and len(new_pairs) == 430
    assert not any(_overlap(a,b) for a,b in old_pairs+new_pairs)
    assert all(any(a<=s and e<=b for _,a,b in HISTORIC if a==s)
               for _,s,e in NESTED)
    assert len([(a,b) for a in ROLES for b in NESTED]) == 150
    assert not any(_overlap(a,b) for a in ROLES for b in NESTED)
    assert all(l%W==0 and u-l==W for _,l,u in ROLES)
    assert ROLES[4][1] == 2*ROLES[1][1]
    root = isqrt(95_999_999)
    assert root == 9797 and root*root <= 95_999_999 < (root+1)**2
    return (len(old_pairs), len(new_pairs), len(NESTED), len(ROLES)*len(NESTED))


def validate_plan(phase, plan):
    """Validate the ENTIRE exact typed positive plan, before any generator call."""
    if phase != "D18" or type(plan) not in (list,tuple) or len(plan) != 2:
        raise ValueError("D18-only complete positive generation plan required")
    for actual, expected in zip(plan, D18_PLAN):
        if type(actual) is not dict or actual.keys() != expected.keys():
            raise ValueError("bad generation entry key set")
        if any(type(actual[k]) is not type(expected[k]) or actual[k] != expected[k]
               for k in expected):
            raise ValueError("off-allowlist generation entry")
    a,b = plan
    s = isqrt(b["stop"]-1)
    if s != 9797 or s*s > b["stop"]-1 or (s+1)**2 <= b["stop"]-1:
        raise ValueError("wrong square root")
    if a["stop"] != s+1 or not (a["stop"] < 100_000):
        raise ValueError("bad base support")
    new_high = ("D18", b["start"], b["stop"])
    forbidden = HISTORIC+NESTED+tuple(x for x in ROLES if x[0] != "D18")
    if any(_overlap(new_high, x) for x in forbidden):
        raise ValueError("protected-range intersection")
    return True


def _base_sieve_support(stop):
    """Only [0,9798) may be sieved via whole-prefix strategy."""
    if stop != 9798:
        raise ValueError("non-target base support")
    sieve = bytearray(b"\x01")*stop
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(stop-1)+1):
        if sieve[p]:
            sieve[p*p:stop:p] = b"\x00"*(((stop-1-p*p)//p)+1)
    return [p for p,flag in enumerate(sieve) if flag]


def _segmented_target(start, stop, base):
    """Directly segment ONLY D18; never visit intervening or excluded integers."""
    if (start,stop) != (95_000_000,96_000_000):
        raise ValueError("off-target segmented generation")
    flags = bytearray(b"\x01")*(stop-start)
    for p in base:
        first = max(p*p, ((start+p-1)//p)*p)
        if first < stop:
            flags[first-start:stop-start:p] = b"\x00"*((stop-1-first)//p+1)
    return {start+i for i,flag in enumerate(flags) if flag}


def execute_plan(phase, plan, base_generator=_base_sieve_support,
                 segment_generator=_segmented_target):
    """No base or segment generator is reachable with an invalid WHOLE plan."""
    interval_audit()
    validate_plan(phase, plan)
    validate_plan(phase, plan)  # at the first boundary, before call 1
    base = base_generator(plan[0]["stop"])
    validate_plan(phase, plan)  # at the second boundary, before call 2
    primes = segment_generator(plan[1]["start"], plan[1]["stop"], base)
    return primes


def matrix_product(a,b,mod):
    """Pure, exact 3x3 modular multiplication; no floating/machine word limit."""
    return tuple(tuple((a[i][0]*b[0][j]+a[i][1]*b[1][j]
                         +a[i][2]*b[2][j]) % mod for j in range(3))
                 for i in range(3))


def tiling_remainder(n):
    if type(n) is not int or n < 1:
        raise ValueError("positive integral row length/modulus required")
    if n == 1:
        return 0
    power = tuple(tuple(v % n for v in row) for row in M)
    result = ((1,0,0),(0,1,0),(0,0,1))
    exponent = n
    while exponent:
        if exponent & 1:
            result = matrix_product(result, power, n)
        exponent >>= 1
        if exponent:
            power = matrix_product(power, power, n)
    return sum(result[2][i]*SEED[i] for i in range(3)) % n


def binned(n, remainder):
    if (type(n) is not int or n<=1 or type(remainder) is not int
            or not 0<=remainder<n):
        raise ValueError("noncanonical tiling remainder")
    a,b = (4*remainder)//n, (8*remainder)//n
    if not (0<=a<=3 and 0<=b<=7 and a==b//2):
        raise AssertionError("residue bins not a coarsening")
    return a,b


def strict_mode(freq):
    """Counts for the ENTIRE fixed signature domain, including zeros."""
    if not freq or any(type(x) is not int or x<0 for x in freq):
        raise ValueError("invalid complete frequencies")
    maximum = max(freq)
    winners = [i for i,x in enumerate(freq) if x==maximum]
    if len(winners) != 1:
        return (maximum, maximum, None)
    i = winners[0]
    return (maximum, max(freq[j] for j in range(len(freq)) if j!=i), i)


def signed_enrichment(target_prime, total_composite, target_composite, total_prime):
    values=(target_prime,total_composite,target_composite,total_prime)
    if any(type(v) is not int or v<0 for v in values):
        raise ValueError("signed enrichment requires nonnegative integer counts")
    if target_prime>total_prime or target_composite>total_composite:
        raise ValueError("target exceeds its label population")
    return target_prime*total_composite-target_composite*total_prime


def fully_mixed(target_prime, total_prime, target_composite, total_composite):
    values=(target_prime,total_prime,target_composite,total_composite)
    if any(type(v) is not int or v<0 for v in values):
        raise ValueError("invalid class counts")
    if target_prime>total_prime or target_composite>total_composite:
        raise ValueError("invalid target conservation")
    return (0<target_prime<total_prime and 0<target_composite<total_composite)


def select_supports(rows):
    """L1-first exact integer-set suppression, no replacement, hard cap 2."""
    if type(rows) not in (list,tuple) or len(rows)>2:
        raise ValueError("promotion cap")
    out=[]
    for index,(family, signature, anchors) in enumerate(rows):
        if (family not in ("L1","L2") or type(family) is not str
                or type(signature) is not int or (family=="L1" and not 0<=signature<4)
                or (family=="L2" and not 0<=signature<8)):
            raise ValueError("invalid family/target")
        if index and rows[index-1][0]>=family:
            raise ValueError("noncanonical family order")
        if type(anchors) is not set or any(type(x) is not int for x in anchors):
            raise ValueError("not an exact prime-anchor ID set")
        if not any(anchors==item[2] for item in out):
            out.append((family,signature,anchors))
    return out


def _typed(v,typ):
    return type(v) is typ


def _integer_array(v, count, nonnegative=True):
    return (type(v) is list and len(v)==count and
            all(type(x) is int and (x>=0 if nonnegative else True) for x in v))


def _exact_map(obj, keys):
    if type(obj) is not dict or set(obj)!=set(keys):
        raise ValueError("forbidden, extra or missing serializer key")


def validate_payload(p):
    """Strict frozen per-level key AND type allowlists; fail closed on any data."""
    _exact_map(p,("experiment","implementation_commit","band","partition",
                  "parameters","generation_plan","anchor_summary","validation",
                  "families","promotions"))
    if p["experiment"] != "E018" or not _typed(p["experiment"],str):
        raise ValueError("experiment schema mismatch")
    h = p["implementation_commit"]
    if type(h) is not str or len(h)!=40 or any(c not in '0123456789abcdef' for c in h):
        raise ValueError("invalid pinned commit")
    _exact_map(p["band"],("name","range","interval_semantics"))
    if (p["band"]["name"]!="D18" or p["band"]["interval_semantics"]!="half-open"
            or p["band"]["range"] != [95_000_000,96_000_000]
            or not _integer_array(p["band"]["range"],2)):
        raise ValueError("band schema mismatch")
    if type(p["partition"]) is not list or len(p["partition"])!=5:
        raise ValueError("partition shape mismatch")
    roles=("non-target guard","discovery","non-target guard","one-shot holdout",
           "independently locked adversarial reserve")
    for got,(name,l,u),role in zip(p["partition"],ROLES,roles):
        _exact_map(got,("name","range","role"))
        if (got["name"]!=name or got["range"]!=[l,u] or
                not _integer_array(got["range"],2) or got["role"]!=role):
            raise ValueError("partition element invalid")
    _exact_map(p["parameters"],PARAMETERS)
    if p["parameters"] != PARAMETERS:
        raise ValueError("parameters changed")
    for key,val in PARAMETERS.items():
        if type(p["parameters"][key]) is not type(val):
            raise ValueError("wrong parameter primitive type")
    if (not _integer_array(p["parameters"]["residues_R210"],48)
            or not _integer_array(p["parameters"]["tile_lengths"],3)
            or not _integer_array(p["parameters"]["tiling_seed"],3)
            or not _integer_array(p["parameters"]["residue_bin_counts"],2)
            or any(not _integer_array(row,3) for row in p["parameters"]["transfer_matrix"])):
        raise ValueError("wrong parameter integer nested types")
    validate_plan("D18",p["generation_plan"])
    _exact_map(p["anchor_summary"],("wheel_anchor_count","prime_count","composite_count",
                                    "prime_counts_by_R210","composite_counts_by_R210"))
    a=p["anchor_summary"]
    for k in ("wheel_anchor_count","prime_count","composite_count"):
        if type(a[k]) is not int or a[k]<0:
            raise ValueError("invalid anchor count")
    if not _integer_array(a["prime_counts_by_R210"],48) or not _integer_array(a["composite_counts_by_R210"],48):
        raise ValueError("invalid class counts")
    if (sum(a["prime_counts_by_R210"])!=a["prime_count"] or
        sum(a["composite_counts_by_R210"])!=a["composite_count"] or
        a["prime_count"]+a["composite_count"]!=a["wheel_anchor_count"]):
        raise ValueError("unconserved labels")
    _exact_map(p["validation"],VALIDATORS)
    if any(type(v) is not int or v!=0 for v in p["validation"].values()):
        raise ValueError("nonzero or ill-typed validation failure")
    if type(p["families"]) is not list or len(p["families"])!=2:
        raise ValueError("family list mismatch")
    boolean_keys=("strict_unique_prime_mode","population_floor_passed","class_floor_passed",
                  "occurrence_floor_passed","mixed_class_floor_passed",
                  "positive_class_floor_passed","aggregate_enrichment_positive",
                  "mechanically_eligible")
    for f,(name,domain) in zip(p["families"],(("L1",4),("L2",8))):
        _exact_map(f,FAMILY_KEYS)
        if f["family"]!=name or type(f["family"]) is not str:
            raise ValueError("wrong family order")
        if any(type(f[k]) is not bool for k in boolean_keys):
            raise ValueError("ill-typed family boolean")
        for k in ("prime_mode_count","highest_competing_count"):
            if type(f[k]) is not int or f[k]<0:
                raise ValueError("ill-typed mode frequency")
        nullable=("unique_mode_signature","target_composite_count","mixed_class_count",
                  "positive_class_count","aggregate_enrichment_numerator")
        if not f["strict_unique_prime_mode"]:
            if any(f[k] is not None for k in nullable) or f["mechanically_eligible"]:
                raise ValueError("tie must fail without fallback")
        else:
            if type(f["unique_mode_signature"]) is not int or not 0<=f["unique_mode_signature"]<domain:
                raise ValueError("mode outside domain")
            for k in nullable[1:4]:
                if type(f[k]) is not int or f[k]<0:
                    raise ValueError("target count invalid")
            if type(f["aggregate_enrichment_numerator"]) is not int:
                raise ValueError("signed enrichment invalid")
            if f["mixed_class_count"]>48 or f["positive_class_count"]>48:
                raise ValueError("class count outside domain")
    if type(p["promotions"]) is not list or len(p["promotions"])>2:
        raise ValueError("too many promotions")
    past=-1
    for promo in p["promotions"]:
        _exact_map(promo,PROMO_KEYS)
        if promo["family"] not in ("L1","L2") or type(promo["family"]) is not str:
            raise ValueError("unknown promoted family")
        ind=("L1","L2").index(promo["family"])
        if ind<=past or not p["families"][ind]["mechanically_eligible"]:
            raise ValueError("out-of-order or unqualified promotion")
        past=ind
        if any(type(v) is not int for k,v in promo.items() if k!="family"):
            raise ValueError("noninteger promotion payload")
        if (promo["target_signature"]!=p["families"][ind]["unique_mode_signature"] or
            promo["target_prime_count"]!=p["families"][ind]["prime_mode_count"] or
            promo["target_composite_count"]!=p["families"][ind]["target_composite_count"] or
            promo["mixed_class_count"]!=p["families"][ind]["mixed_class_count"] or
            promo["positive_class_count"]!=p["families"][ind]["positive_class_count"] or
            promo["aggregate_enrichment_numerator"]!=p["families"][ind]["aggregate_enrichment_numerator"]):
            raise ValueError("promotion contradicts frozen family")
    if {f["family"] for f in p["families"] if f["mechanically_eligible"]} != {v["family"] for v in p["promotions"]}:
        raise ValueError("family/promotion correspondence")
    return True


def canonical_bytes(payload):
    validate_payload(payload)
    b=(json.dumps(payload, sort_keys=True,indent=2,ensure_ascii=True)+"\n").encode("utf-8")
    if json.loads(b)!=payload or b.count(b"\n")<2 or not b.endswith(b"\n") or b.endswith(b"\n\n"):
        raise ValueError("canonical byte failure")
    return b


def _reference_checks():
    """Small INVENTED n only: independent tiling enumeration and matrix identity."""
    def count_enum(n):
        if n==0:
            return 1
        return sum(count_enum(n-k) for k in (1,2,3) if k<=n)
    t=[1,1,2]
    for n in range(3,18):
        t.append(t[-1]+t[-2]+t[-3])
    for n in range(9):
        if count_enum(n)!=t[n]:
            raise AssertionError("synthetic tiling recurrence")
    for n in range(1,18):
        # Independently apply the defining matrix exactly n times (no exponentiation).
        v=list(SEED)
        for _ in range(n):
            v=[v[0]+v[1]+v[2], v[0], v[1]]
        if v != [t[n+2] if n+2<len(t) else _tiling_direct(n+2),
                 t[n+1] if n+1<len(t) else _tiling_direct(n+1),t[n]]:
            raise AssertionError("matrix identity disagreement")
        if tiling_remainder(n)!=t[n]%n:
            raise AssertionError("modular matrix power mismatch")


def _tiling_direct(n):
    a,b,c=1,0,0
    for _ in range(n):
        a,b,c=a+b+c,a,b
    return a


def evaluate(implementation_commit, primes):
    """Aggregate-only evaluation on full label-blind X_D18, no new prime query."""
    _reference_checks()
    if type(primes) is not set or any(type(x) is not int or not 95_000_000<=x<96_000_000 for x in primes):
        raise ValueError("invalid single segmented label source")
    residue_id={r:i for i,r in enumerate(R210)}
    if len(residue_id)!=48 or tuple(x for x in range(Q) if gcd(x,Q)==1)!=R210:
        raise AssertionError("wheel class identity")
    pop=[[0]*48 for _ in range(2)]
    freqs=[[[0]*d for _ in range(2)] for d in (4,8)]
    cls=[[[[0]*d for _ in range(48)] for _ in range(2)] for d in (4,8)]
    prime_rows=[]
    all_count=0
    for x in range(95_000_000,96_000_000):
        rid=residue_id.get(x%Q)
        if rid is None:
            continue
        label=int(x in primes)
        remainder=tiling_remainder(x)
        b4,b8=binned(x,remainder)
        pop[label][rid]+=1
        all_count+=1
        for j,b in enumerate((b4,b8)):
            freqs[j][label][b]+=1
            cls[j][label][rid][b]+=1
        if label:
            prime_rows.append((x,b4,b8))
    if all_count!=sum(map(sum,pop)) or any(sum(freqs[j][i])!=sum(pop[i]) for j in (0,1) for i in (0,1)):
        raise AssertionError("population/support conservation")
    if any(sum(cls[j][label][r])!=pop[label][r] for j in (0,1) for label in (0,1) for r in range(48)):
        raise AssertionError("class conservation")
    NP,NC=sum(pop[1]),sum(pop[0])
    if len(prime_rows)!=NP or NP+NC!=all_count or all_count!=sum(1 for i in range(95_000_000,96_000_000) if (i%Q) in residue_id):
        raise AssertionError("wheel conservation")
    global_floor=NP>=1000 and NC>=1000
    class_floor=all(pop[0][r]>=10 and pop[1][r]>=10 for r in range(48))
    families=[]
    candidate_sets=[]
    for j,(family,domain) in enumerate((("L1",4),("L2",8))):
        max_count,highest_other,target=strict_mode(freqs[j][1])
        unique=target is not None
        occurrence=max_count>=32
        if unique:
            cp=freqs[j][0][target]
            mixed=0
            positive=0
            for r in range(48):
                tp=cls[j][1][r][target]
                tc=cls[j][0][r][target]
                pr=pop[1][r]
                cr=pop[0][r]
                mixed+=int(fully_mixed(tp,pr,tc,cr))
                positive+=int(signed_enrichment(tp,cr,tc,pr)>0)
            enrichment=signed_enrichment(max_count,NC,cp,NP)
            support={x for x,b4,b8 in prime_rows if (b4 if j==0 else b8)==target}
            if len(support)!=max_count:
                raise AssertionError("exact prime support mismatch")
            good=(global_floor and class_floor and occurrence and mixed>=36
                  and enrichment>0 and positive>=30)
            if good:
                candidate_sets.append((family,target,support))
        else:
            cp=mixed=positive=enrichment=None
            good=False
        row={
            "family":family,
            "prime_mode_count":max_count,
            "highest_competing_count":highest_other,
            "strict_unique_prime_mode":unique,
            "unique_mode_signature":target,
            "target_composite_count":cp,
            "population_floor_passed":global_floor,
            "class_floor_passed":class_floor,
            "occurrence_floor_passed":bool(occurrence and unique),
            "mixed_class_count":mixed,
            "mixed_class_floor_passed":bool(unique and mixed>=36),
            "positive_class_count":positive,
            "positive_class_floor_passed":bool(unique and positive>=30),
            "aggregate_enrichment_numerator":enrichment,
            "aggregate_enrichment_positive":bool(unique and enrichment>0),
            "mechanically_eligible":False,
        }
        families.append(row)
    retained=select_supports(candidate_sets)
    retained_families={x[0] for x in retained}
    promotions=[]
    for fam,target,_support in retained:
        ind=("L1","L2").index(fam)
        f=families[ind]
        f["mechanically_eligible"]=True
        promotions.append({
            "family":fam,"target_signature":target,
            "target_prime_count":f["prime_mode_count"],
            "target_composite_count":f["target_composite_count"],
            "mixed_class_count":f["mixed_class_count"],
            "positive_class_count":f["positive_class_count"],
            "aggregate_enrichment_numerator":f["aggregate_enrichment_numerator"],
        })
    if len(retained)>2 or len(retained_families)!=len(retained):
        raise AssertionError("duplicate/cap failure")
    role_names=("non-target guard","discovery","non-target guard","one-shot holdout",
                "independently locked adversarial reserve")
    payload={
        "experiment":"E018", "implementation_commit":implementation_commit,
        "band":{"name":"D18","range":[95_000_000,96_000_000],
                "interval_semantics":"half-open"},
        "partition":[{"name":name,"range":[l,u],"role":role}
                     for (name,l,u),role in zip(ROLES,role_names)],
        "parameters":PARAMETERS,
        "generation_plan":[dict(a) for a in D18_PLAN],
        "anchor_summary":{
            "wheel_anchor_count":all_count,"prime_count":NP,"composite_count":NC,
            "prime_counts_by_R210":pop[1],"composite_counts_by_R210":pop[0],
        },
        "validation":{key:0 for key in VALIDATORS},
        "families":families,
        "promotions":promotions,
    }
    canonical_bytes(payload)
    return payload


def main(argv=None):
    parser=argparse.ArgumentParser(description="Frozen E018 D18-only discovery")
    parser.add_argument("--phase",required=True,choices=("D18",))
    parser.add_argument("--implementation-commit",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    if args.output!="research/evidence/E018_D18_discovery.json":
        parser.error("only the complete precommitted D18 output path is accepted")
    if type(args.implementation_commit) is not str or len(args.implementation_commit)!=40:
        parser.error("expected pinned 40-character source/test commit")
    # Plan audit precedes either generator. All signature computation follows generation.
    interval_audit()
    plan=[dict(a) for a in D18_PLAN]
    primes=execute_plan(args.phase,plan)
    payload=evaluate(args.implementation_commit,primes)
    raw=canonical_bytes(payload)
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(raw)


if __name__=="__main__":
    main()

"""Frozen E015 D15 evaluator; no prime generation during import or unit tests."""

import argparse
import itertools
import json
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

R30 = (1, 7, 11, 13, 17, 19, 23, 29)
OFFSETS = tuple(range(-4, 5))
ROLES = (
    ("G15-pre", 80_000_000, 81_000_000, "guard"),
    ("D15", 81_000_000, 82_000_000, "discovery"),
    ("G15-mid", 82_000_000, 83_000_000, "guard"),
    ("H15", 83_000_000, 84_000_000, "holdout"),
    ("A15", 162_000_000, 163_000_000, "adversarial"),
)
PLANS = {
    "D15": (("base_sieve_support", 0, 9056, "whole_prefix"), ("segmented_target", 81_000_000, 82_000_000, "segmented")),
    "H15": (("base_sieve_support", 0, 9166, "whole_prefix"), ("segmented_target", 83_000_000, 84_000_000, "segmented")),
    "A15": (("base_sieve_support", 0, 12768, "whole_prefix"), ("segmented_target", 162_000_000, 163_000_000, "segmented")),
}
# The first 53 entries are exactly E013's 23 consumed/contaminated,
# 14 protected and 16 guard roles. No prime-derived inputs are used.
HISTORICAL_MILLIONS = (
    ("D0",0),("H0",1),("S1",2),("S2",4),("S3",8),("A0-contaminated",10),
    ("S4",16),("S5",32),("D3",35),("D4",39),("D6",42),("H6",44),
    ("D7",46),("H7",48),("D8",50),("D9",54),("H9",56),("D10",58),
    ("H10",60),("D11",62),("H11",64),("D12",67),
    ("A1",33),("H3",37),("H4",41),("H8",52),("A8",66),("H12",69),
    ("A3",70),("A4",78),("A6",84),("A7",92),("A9",108),
    ("A10",116),("A11",124),("A12",134),
    ("G3-pre",34),("G3-post",36),("G4-pre",38),("G4-mid",40),
    ("G6-mid",43),("G7-pre",45),("G7-mid",47),("G8-pre",49),
    ("G8-mid",51),("G9-pre",53),("G9-mid",55),("G10-pre",57),
    ("G10-mid",59),("G11-pre",61),("G11-mid",63),("G12-pre",65),
    ("G12-mid",68),
    ("G13-pre",71),("D13",72),("G13-mid",73),("H13",74),("A13",144),
    ("G14-pre",75),("D14",76),("G14-mid",77),("H14",79),("A14",152),
)
CALIBRATION_STARTS = (128_000_000,256_000_000,512_000_000,1_024_000_000,2_048_000_000,4_096_000_000)
VALIDATION_KEYS = (
    "plan_failure_count", "shell_or_division_failure_count", "zero_condition_failure_count",
    "quartile_boundary_failure_count", "histogram_identity_failure_count", "signature_domain_failure_count",
    "anchor_or_label_failure_count", "R30_population_failure_count", "frequency_or_mode_failure_count",
    "serializer_or_duplicate_failure_count",
)
TOP_KEYS = {"experiment","implementation_commit","band","partition","parameters","generation_plan","anchor_summary","validation","families","promotions"}
FAMILY_KEYS = {"family","prime_mode_count","highest_competing_count","strict_unique_prime_mode", "unique_mode_signature","target_composite_count","population_floor_passed", "class_floor_passed","occurrence_floor_passed","mixed_class_count","mixed_class_floor_passed","aggregate_enrichment_numerator","aggregate_enrichment_positive","mechanically_eligible"}


def historical_intervals():
    if len(HISTORICAL_MILLIONS) != 63 or len({name for name,_ in HISTORICAL_MILLIONS}) != 63:
        raise ValueError("historical role inventory mismatch")
    return [(name, m*1_000_000, (m+1)*1_000_000) for name,m in HISTORICAL_MILLIONS] + [
        (f"E005-{i}", start, start+1_048_576) for i,start in enumerate(CALIBRATION_STARTS)
    ]


def audit_partition():
    hist = historical_intervals()
    if len(hist) != 69:
        raise ValueError("69 exclusions required")
    pairs = [(a,b) for a in ROLES for b in hist] + [
        (ROLES[i], ROLES[j]) for i in range(5) for j in range(i+1,5)
    ]
    if len(pairs) != 355 or any(a[1]<b[2] and b[1]<a[2] for a,b in pairs):
        raise ValueError("355 pair audit failed")
    for name,start,stop,_ in ROLES:
        if stop-start != 1_000_000 or start >= stop:
            raise ValueError(name)
    return len(pairs)


def expected_plan(phase):
    if phase not in PLANS:
        raise ValueError("unauthorized phase")
    return [dict(zip(("purpose","start","stop","strategy"), entry)) for entry in PLANS[phase]]


def validate_plan(phase, plan, authorized="D15"):
    if phase != authorized or phase not in PLANS or type(plan) is not list or plan != expected_plan(phase):
        raise ValueError("plan denied before prime generator")
    for call in plan:
        if type(call) is not dict or set(call) != {"purpose","start","stop","strategy"}:
            raise ValueError("invalid generator call")
        if type(call["start"]) is not int or type(call["stop"]) is not int:
            raise ValueError("noninteger bounds")
    if isqrt(plan[1]["stop"]-1)+1 != plan[0]["stop"]:
        raise ValueError("base-support mismatch")
    return True


def generator_entry(phase, plan, index, generate, authorized="D15"):
    validate_plan(phase, plan, authorized)
    if index not in (0,1) or plan[index] != expected_plan(phase)[index]:
        raise ValueError("entry denied")
    return generate(plan[index])


def guarded_primes(phase, plan, authorized="D15"):
    validate_plan(phase, plan, authorized)
    base = generator_entry(phase, plan, 0, _generate, authorized)
    return generator_entry(phase, plan, 1, lambda entry: _generate(entry, base), authorized)


def _generate(entry, base=None):
    # Only guarded_primes calls this private generator, after full-plan checks.
    start,stop = entry["start"],entry["stop"]
    if entry["purpose"] == "base_sieve_support" and entry["strategy"] == "whole_prefix" and start == 0 and stop in (9056,9166,12768):
        mask = bytearray(b"\x01")*stop
        mask[:2] = b"\x00\x00"
        for p in range(2,isqrt(stop-1)+1):
            if mask[p]:
                mask[p*p:stop:p] = b"\x00"*(((stop-1-p*p)//p)+1)
        return [i for i in range(stop) if mask[i]]
    if entry["purpose"] == "segmented_target" and entry["strategy"] == "segmented" and (start,stop) in ((81_000_000,82_000_000),(83_000_000,84_000_000),(162_000_000,163_000_000)) and base is not None:
        mask = bytearray(b"\x01")*(stop-start)
        for p in base:
            first = max(p*p, ((start+p-1)//p)*p)
            if first < stop:
                mask[first-start:stop-start:p] = b"\x00"*(((stop-1-first)//p)+1)
        return {start+i for i,v in enumerate(mask) if v}
    raise ValueError("generator entry outside allowlist")


def quartile(remainder,denominator):
    if type(remainder) is not int or type(denominator) is not int or not (0<=remainder<denominator):
        raise ValueError("division bounds")
    result=(4*remainder)//denominator
    if result not in range(4) or not (result*denominator<=4*remainder<(result+1)*denominator):
        raise ValueError("quartile boundaries")
    return result


def shape(x):
    s=isqrt(x)
    if not (s*s<=x<(s+1)*(s+1)):
        raise ValueError("isqrt")
    bins=[]
    for offset in OFFSETS:
        d=s+offset
        if not (1<d<x):
            raise ValueError("shell denominator")
        q,r=divmod(x,d)
        if x != q*d+r or not (0<=r<d):
            raise ValueError("division conservation")
        if r==0:
            return None
        bins.append(quartile(r,d))
    c=tuple(bins.count(k) for k in range(4))
    if len(bins)!=9 or sum(c)!=9 or any(not 0<=v<=9 for v in c):
        raise ValueError("histogram")
    signatures=(max(c),tuple(sorted(c,reverse=True)),c)
    if signatures[0]!=signatures[1][0] or sorted(signatures[2],reverse=True)!=list(signatures[1]):
        raise ValueError("coarsening")
    return signatures


def domains():
    r3=tuple(t for t in itertools.product(range(10),repeat=4) if sum(t)==9)
    r2=tuple(t for t in r3 if list(t)==sorted(t,reverse=True))
    return (tuple(range(3,10)),r2,r3)


def strict_mode(counts, domain):
    ranking=sorted(domain,key=lambda t:(-counts.get(t,0),t))
    highest=counts.get(ranking[0],0)
    competitor=counts.get(ranking[1],0)
    return (ranking[0] if highest>competitor else None,highest,competitor)


def mixed_classes(prime_by,composite_by,np_by,nc_by,target):
    return sum(all((prime_by[i].get(target,0),np_by[i]-prime_by[i].get(target,0),
                    composite_by[i].get(target,0),nc_by[i]-composite_by[i].get(target,0)))
               for i in range(8))


def exact_enrichment(np,nc,npt,nct):
    return npt*nc-nct*np


def select_duplicates(eligible_supports):
    kept=[]
    for family,support in eligible_supports:
        if not any(support==prior for _,prior in kept):
            kept.append((family,support))
    if len(kept)>3:
        raise ValueError("promotion overflow")
    return [family for family,_ in kept]


def serialize(payload):
    validate_schema(payload)
    return (json.dumps(payload,sort_keys=True,indent=2,ensure_ascii=True)+"\n").encode("utf-8")


def validate_schema(p):
    def keys(obj, wanted):
        if type(obj) is not dict or set(obj)!=set(wanted):
            raise ValueError("narrow schema fields")
    keys(p,TOP_KEYS)
    if p["experiment"]!="E015" or type(p["implementation_commit"]) is not str or len(p["implementation_commit"])!=40:
        raise ValueError("identity")
    keys(p["band"],("name","range","interval_semantics"))
    if p["band"]!={"name":"D15","range":[81_000_000,82_000_000],"interval_semantics":"half-open"}:
        raise ValueError("band")
    if p["partition"] != [dict(name=n,range=[a,b],role=role) for n,a,b,role in ROLES]:
        raise ValueError("partition")
    keys(p["parameters"],("width","wheel","residues_R30","denominator_offsets","quartile_edges_num","quartile_denominator","zero_remainder_excluded","population_floor","class_floor","occurrence_floor","mixed_class_floor"))
    if p["parameters"] != dict(width=1_000_000,wheel=30,residues_R30=list(R30),denominator_offsets=list(OFFSETS),quartile_edges_num=[0,1,2,3,4],quartile_denominator=4,zero_remainder_excluded=True,population_floor=1000,class_floor=100,occurrence_floor=32,mixed_class_floor=6):
        raise ValueError("parameters")
    validate_plan("D15",p["generation_plan"])
    keys(p["anchor_summary"],("wheel_anchor_count","conditioned_anchor_count","excluded_zero_remainder_count","prime_count","composite_count","prime_counts_by_R30","composite_counts_by_R30"))
    a=p["anchor_summary"]
    for v in (a["prime_counts_by_R30"],a["composite_counts_by_R30"]):
        if type(v) is not list or len(v)!=8 or any(type(n) is not int or n<0 for n in v):
            raise ValueError("R30 counts")
    for k in ("wheel_anchor_count","conditioned_anchor_count","excluded_zero_remainder_count","prime_count","composite_count"):
        if type(a[k]) is not int or a[k]<0:
            raise ValueError("counts")
    if a["prime_count"]+a["composite_count"]!=a["conditioned_anchor_count"] or a["wheel_anchor_count"]!=a["conditioned_anchor_count"]+a["excluded_zero_remainder_count"] or sum(a["prime_counts_by_R30"])!=a["prime_count"] or sum(a["composite_counts_by_R30"])!=a["composite_count"]:
        raise ValueError("population conservation")
    keys(p["validation"],VALIDATION_KEYS)
    if any(type(x) is not int or x!=0 for x in p["validation"].values()):
        raise ValueError("nonzero validation counter")
    if type(p["families"]) is not list or len(p["families"])!=3 or [f.get("family") for f in p["families"]]!=["R1","R2","R3"]:
        raise ValueError("families")
    for i,f in enumerate(p["families"]):
        keys(f,FAMILY_KEYS)
        for k in ("prime_mode_count","highest_competing_count"):
            if type(f[k]) is not int or f[k]<0:
                raise ValueError("mode counts")
        for k in ("strict_unique_prime_mode","population_floor_passed","class_floor_passed","occurrence_floor_passed","mixed_class_floor_passed","aggregate_enrichment_positive","mechanically_eligible"):
            if type(f[k]) is not bool:
                raise ValueError("mode flag")
        target=f["unique_mode_signature"]
        if target is None:
            if f["strict_unique_prime_mode"] or any(f[k] is not None for k in ("target_composite_count","mixed_class_count","aggregate_enrichment_numerator")):
                raise ValueError("tie handling")
        else:
            target=tuple(target) if type(target) is list else target
            if target not in domains()[i] or not f["strict_unique_prime_mode"]:
                raise ValueError("signature")
            for k in ("target_composite_count","mixed_class_count","aggregate_enrichment_numerator"):
                if type(f[k]) is not int:
                    raise ValueError("target counts")
    if type(p["promotions"]) is not list or len(p["promotions"])>3:
        raise ValueError("promotions")
    if [item["family"] for item in p["promotions"]] != [f["family"] for f in p["families"] if f["mechanically_eligible"]]:
        raise ValueError("promotion family agreement")
    for item in p["promotions"]:
        keys(item,("family","target_signature","target_prime_count","target_composite_count","mixed_class_count","aggregate_enrichment_numerator"))
        f=next(f for f in p["families"] if f["family"]==item["family"])
        if item["target_signature"]!=f["unique_mode_signature"] or item["target_prime_count"]!=f["prime_mode_count"] or item["target_composite_count"]!=f["target_composite_count"] or item["mixed_class_count"]!=f["mixed_class_count"] or item["aggregate_enrichment_numerator"]!=f["aggregate_enrichment_numerator"]:
            raise ValueError("promotion count mismatch")


def evaluate(implementation_commit, prime_set, plan):
    validate_plan("D15",plan)
    audit_partition()
    low,high=PLANS["D15"][1][1:3]
    if any(type(p) is not int or p<low or p>=high or gcd(p,30)!=1 for p in prime_set):
        raise ValueError("unexpected prime support")
    domains_all=domains()
    prime=[Counter() for _ in range(3)]
    composite=[Counter() for _ in range(3)]
    prime_by=[[Counter() for _ in range(8)] for _ in range(3)]
    comp_by=[[Counter() for _ in range(8)] for _ in range(3)]
    support=[{} for _ in range(3)]
    np_by=[0]*8; nc_by=[0]*8
    wheel=excluded=0
    for x in range(low,high):
        residue=x%30
        if residue not in R30:
            continue
        wheel+=1
        t=shape(x)
        if t is None:
            excluded+=1
            continue
        cls=R30.index(residue)
        isprime=x in prime_set
        if isprime: np_by[cls]+=1
        else: nc_by[cls]+=1
        for i,sig in enumerate(t):
            if sig not in domains_all[i]:
                raise ValueError("signature domain")
            counts=prime if isprime else composite
            by=prime_by if isprime else comp_by
            counts[i][sig]+=1
            by[i][cls][sig]+=1
            if isprime: support[i].setdefault(sig,set()).add(x)
    np=sum(np_by);nc=sum(nc_by)
    if np+nc!=wheel-excluded or any(sum(prime[i].values())!=np or sum(composite[i].values())!=nc for i in range(3)):
        raise ValueError("frequency conservation")
    pop_ok=np>=1000 and nc>=1000
    cls_ok=all(p>=100 and c>=100 for p,c in zip(np_by,nc_by))
    families=[]; eligible=[]
    for i,name in enumerate(("R1","R2","R3")):
        target,highest,rival=strict_mode(prime[i],domains_all[i])
        unique=target is not None
        nct=composite[i][target] if unique else None
        mix=mixed_classes(prime_by[i],comp_by[i],np_by,nc_by,target) if unique else None
        enrich=exact_enrichment(np,nc,highest,nct) if unique else None
        count_ok=unique and highest>=32
        mixed_ok=unique and mix>=6
        pos=unique and enrich>0
        before_duplicate=bool(unique and pop_ok and cls_ok and count_ok and mixed_ok and pos)
        if before_duplicate:
            eligible.append((name,support[i][target]))
        families.append(dict(family=name,prime_mode_count=highest,highest_competing_count=rival,strict_unique_prime_mode=unique,unique_mode_signature=(list(target) if i else target) if unique else None,target_composite_count=nct,population_floor_passed=pop_ok,class_floor_passed=cls_ok,occurrence_floor_passed=bool(count_ok),mixed_class_count=mix,mixed_class_floor_passed=bool(mixed_ok),aggregate_enrichment_numerator=enrich,aggregate_enrichment_positive=bool(pos),mechanically_eligible=False))
    retained=select_duplicates(eligible)
    promotions=[]
    for f in families:
        if f["family"] in retained:
            f["mechanically_eligible"]=True
            promotions.append(dict(family=f["family"],target_signature=f["unique_mode_signature"],target_prime_count=f["prime_mode_count"],target_composite_count=f["target_composite_count"],mixed_class_count=f["mixed_class_count"],aggregate_enrichment_numerator=f["aggregate_enrichment_numerator"]))
    payload=dict(experiment="E015",implementation_commit=implementation_commit,band=dict(name="D15",range=[low,high],interval_semantics="half-open"),partition=[dict(name=n,range=[a,b],role=role) for n,a,b,role in ROLES],parameters=dict(width=1_000_000,wheel=30,residues_R30=list(R30),denominator_offsets=list(OFFSETS),quartile_edges_num=[0,1,2,3,4],quartile_denominator=4,zero_remainder_excluded=True,population_floor=1000,class_floor=100,occurrence_floor=32,mixed_class_floor=6),generation_plan=plan,anchor_summary=dict(wheel_anchor_count=wheel,conditioned_anchor_count=wheel-excluded,excluded_zero_remainder_count=excluded,prime_count=np,composite_count=nc,prime_counts_by_R30=np_by,composite_counts_by_R30=nc_by),validation=dict.fromkeys(VALIDATION_KEYS,0),families=families,promotions=promotions)
    serialize(payload)
    return payload


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--phase",required=True,choices=("D15",))
    parser.add_argument("--implementation-commit",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    if args.phase!="D15" or len(args.implementation_commit)!=40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        raise ValueError("nonfrozen identity")
    plan=expected_plan("D15")
    audit_partition()
    validate_plan(args.phase,plan)
    primes=guarded_primes(args.phase,plan)
    payload=evaluate(args.implementation_commit,primes,plan)
    Path(args.output).write_bytes(serialize(payload))


if __name__=="__main__":
    main()

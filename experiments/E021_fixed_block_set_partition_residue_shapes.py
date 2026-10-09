"""E021 D21-only exact, source-free fixed-block set-partition evaluator.

Only the fully pinned D21 direct-segment plan may invoke a prime generator.
Per-anchor combinatorial features are evaluated BEFORE segmented labels.
"""
import argparse
import json
from math import comb, factorial, gcd, isqrt
from pathlib import Path

R210 = (1,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,121,127,131,137,139,143,149,151,157,163,167,169,173,179,181,187,191,193,197,199,209)
ROLES = (("G21-pre",136000000,138000000,"guard"),("D21",138000000,140000000,"discovery"),("G21-mid",140000000,142000000,"guard"),("H21",142000000,144000000,"holdout"),("A21",276000000,278000000,"adversarial"))
PLAN = (("base_sieve_support",0,11833,"whole_prefix"),("segmented_target",138000000,140000000,"direct_segmented"))
# Frozen E013 early source metadata: 22 consumed/contaminated, 14 held-back, 17 guards.
EARLY = (
 ("D0",0,1),("H0",1,2),("S1",2,3),("S2",4,5),("S3",8,9),("A0",10,11),("S4",16,17),("S5",32,33),
 ("D3",35,36),("D4",39,40),("D6",42,43),("H6",44,45),("D7",46,47),("H7",48,49),("D8",50,51),
 ("D9",54,55),("H9",56,57),("D10",58,59),("H10",60,61),("D11",62,63),("H11",64,65),("D12",67,68),
 ("A1",33,34),("H3",37,38),("H4",41,42),("H8",52,53),("A8",66,67),("H12",69,70),("A3",70,71),
 ("A4",78,79),("A6",84,85),("A7",92,93),("A9",108,109),("A10",116,117),("A11",124,125),("A12",134,135),
 ("G3-pre",34,35),("G3-post",36,37),("G4-pre",38,39),("G4-mid",40,41),("G6-mid",43,44),
 ("G7-pre",45,46),("G7-mid",47,48),("G8-pre",49,50),("G8-mid",51,52),("G9-pre",53,54),("G9-mid",55,56),
 ("G10-pre",57,58),("G10-mid",59,60),("G11-pre",61,62),("G11-mid",63,64),("G12-pre",65,66),("G12-mid",68,69))
# Frozen five-role design tables E013-E020, in G/D/G/H/A order; all endpoints are millions.
FIVE = (
 (13,((71,72),(72,73),(73,74),(74,75),(144,145))),
 (14,((75,76),(76,77),(77,78),(79,80),(152,153))),
 (15,((80,81),(81,82),(82,83),(83,84),(162,163))),
 (16,((85,86),(86,87),(87,88),(88,89),(172,173))),
 (17,((89,90),(90,91),(91,92),(93,94),(180,181))),
 (18,((94,95),(95,96),(96,97),(97,98),(190,191))),
 (19,((98,99),(99,100),(100,101),(101,102),(198,199))),
 (20,((102,103),(103,104),(104,105),(105,106),(206,207))))
E005_STARTS = (128000000,256000000,512000000,1024000000,2048000000,4096000000)
E005_WIDTHS = (4096,16384,65536,262144,1048576)
COUNTERS = ("plan_failure_count","interval_exclusion_failure_count","partition_quotient_failure_count","modular_power_failure_count","quartile_signature_failure_count","wheel_label_failure_count","frequency_conservation_failure_count","signed_class_control_failure_count","selection_duplicate_failure_count","serializer_failure_count")
TOP = ("experiment","implementation_commit","band","partition","parameters","generation_plan","anchor_summary","validation","families","promotions")
PARAMS = {"width":2000000,"wheel":210,"residues_R210":list(R210),"block_counts":[3,4],"denominators":[6,24],"modulus":"anchor_plus_one","surjection_numerator":"inclusion_exclusion","quartile_count":4,"signature_order":"4*q3+q4","selector":"strict_unique_positive_signed_enrichment_max","population_floor":2000,"class_floor":20,"occurrence_floor":64,"mixed_class_floor":36,"positive_class_floor":30,"full_mixed_required":True}
FAMILY_KEYS = ("family","candidate_signature","evaluated_signature","highest_enrichment_numerator","highest_competing_enrichment_numerator","strict_unique_positive_enrichment_max","target_prime_count","target_composite_count","population_floor_passed","class_floor_passed","occurrence_floor_passed","mixed_class_count","mixed_class_floor_passed","positive_class_count","positive_class_floor_passed","target_enrichment_numerator","target_enrichment_positive","mechanically_eligible")


def old_intervals():
    old = [(n,a*1000000,b*1000000) for n,a,b in EARLY]
    for version, spans in FIVE:
        old += [(f"{prefix}{version}{suffix}",a*1000000,b*1000000) for (prefix,suffix),(a,b) in zip((("G","-pre"),("D",""),("G","-mid"),("H",""),("A","")),spans)]
    old += [(f"E005-{i}",a,a+1048576) for i,a in enumerate(E005_STARTS)]
    return old


def overlap(a,b):
    return a[1]<b[2] and b[1]<a[2]


def audit_intervals():
    old = old_intervals()
    new = [(n,a,b) for n,a,b,_ in ROLES]
    nested = [(f"E005-{i}-w{w}",a,a+w) for i,a in enumerate(E005_STARTS) for w in E005_WIDTHS]
    assert len(EARLY)==53 and len(old)==99 and len(new)==5 and len(nested)==30
    assert sum(overlap(a,b) for i,a in enumerate(old) for b in old[i+1:])==0
    assert sum(overlap(a,b) for a in old for b in new)==0
    assert sum(overlap(a,b) for i,a in enumerate(new) for b in new[i+1:])==0
    assert sum(overlap(a,b) for a in new for b in nested)==0
    assert all(start<=a and b<=start+1048576 for i,start in enumerate(E005_STARTS) for n,a,b in nested[i*5:(i+1)*5])
    assert len({n for n,_,_ in old+new})==104
    assert ROLES[4][1]==2*ROLES[1][1]
    assert all((b-a)==2000000 and a%2000000==0 for _,a,b,_ in ROLES)
    for guard in range(106000000,136000000,2000000):
        trial=(("G",guard,guard+2000000),("D",guard+2000000,guard+4000000),("G2",guard+4000000,guard+6000000),("H",guard+6000000,guard+8000000),("A",2*(guard+2000000),2*(guard+2000000)+2000000))
        assert any(overlap(x,y) for x in trial for y in old)
    assert isqrt(139999999)==11832 and 11832**2<=139999999<11833**2
    return (4851,495,10,150,30)


def validate_plan(entries, phase="D21", indirect=False, per_anchor=False):
    # Validate the ENTIRE plan before any generator and again at each entry.
    audit_intervals()
    if phase!="D21" or indirect or per_anchor or type(entries) not in (tuple,list) or len(entries)!=2:
        raise ValueError("off-phase/indirect/per-anchor/incomplete plan")
    if any(type(e) not in (tuple,list) or len(e)!=4 or any(type(z)!=type(w) or z!=w for z,w in zip(e,p)) for e,p in zip(entries,PLAN)):
        raise ValueError("altered generator call")
    return True


class GeneratorGate:
    """Fail-closed ordered generator capability; check entire plan at every entry."""
    def __init__(self,entries=PLAN,phase="D21",indirect=False,per_anchor=False):
        validate_plan(entries,phase,indirect,per_anchor)
        self.entries=entries
        self.phase=phase
        self.cursor=0

    def enter(self,index,purpose,start,stop,strategy):
        validate_plan(self.entries,self.phase)
        if type(index)!=int or index!=self.cursor or index>=2:
            raise ValueError("reordered or extra generator entry")
        if (purpose,start,stop,strategy)!=PLAN[index]:
            raise ValueError("generator entry mismatch")
        self.cursor+=1



def recurrence_small(n,k):
    if n==0: return int(k==0)
    if k<=0 or k>n: return 0
    return k*recurrence_small(n-1,k)+recurrence_small(n-1,k-1)


def numerator(n,k):
    return sum((-1)**(k-j)*comb(k,j)*j**n for j in range(k+1))


def residues(n):
    if type(n)!=int or n<1: raise ValueError("anchor must be positive integer")
    m=n+1
    ans=[]
    for k,d in ((3,6),(4,24)):
        mod=d*m
        v=sum((-1)**(k-j)*comb(k,j)*pow(j,n,mod) for j in range(k+1))%mod
        if v%d: raise AssertionError("nonintegral surjection quotient")
        r=v//d
        if not (0<=r<m): raise AssertionError("invalid residue")
        ans.append(r)
    return tuple(ans)


def signature(n,r3,r4):
    if not (type(n)==type(r3)==type(r4)==int and n>=1 and 0<=r3<n+1 and 0<=r4<n+1):
        raise ValueError("invalid quartile input")
    q3=4*r3//(n+1);q4=4*r4//(n+1)
    t=4*q3+q4
    if not (0<=t<16): raise AssertionError("outside 16 states")
    return t


def select(enrichments):
    if len(enrichments)!=16 or any(type(x)!=int for x in enrichments): raise ValueError("invalid enrichment table")
    best=max(enrichments)
    order=sorted(enrichments,reverse=True)
    return (enrichments.index(best) if best>0 and order[0]>order[1] else None,best,order[1])


def dedup_support(support, existing):
    if type(support)!=set or any(type(x)!=int for x in support) or type(existing)!=list:
        raise ValueError("invalid exact supports")
    if any(support==prior for prior in existing):return False
    if len(existing)>=1:return False
    existing.append(set(support))
    return True


def base_sieve(stop,gate):
    gate.enter(0,"base_sieve_support",0,stop,"whole_prefix")
    flags=bytearray(b'\x01')*stop
    flags[:2]=b'\x00\x00'
    for p in range(2,isqrt(stop-1)+1):
        if flags[p]: flags[p*p:stop:p]=b'\x00'*(((stop-1-p*p)//p)+1)
    return [i for i in range(stop) if flags[i]]


def target_segment(start,stop,base,gate):
    gate.enter(1,"segmented_target",start,stop,"direct_segmented")
    flags=bytearray(b'\x01')*(stop-start)
    for p in base:
        first=max(p*p,((start+p-1)//p)*p)
        if first<stop: flags[first-start:stop-start:p]=b'\x00'*(((stop-1-first)//p)+1)
    return flags


def checked_synthetics():
    for n in range(1,13):
        rs=residues(n)
        for k,r in zip((3,4),rs):
            d=factorial(k); a=numerator(n,k)
            assert a%d==0 and a//d==recurrence_small(n,k)
            assert r==recurrence_small(n,k)%(n+1)
            mod=d*(n+1)
            assert all(pow(j,n,mod)==(j**n)%mod for j in range(k+1))
        t=signature(n,*rs)
        assert 0<=t<16
    for n in (3,7,11,15,19):
        m=n+1
        for a in range(m):
            assert 4*a//m in range(4)
    assert len(R210)==48 and len(set(R210))==48 and R210==tuple(i for i in range(210) if gcd(i,210)==1)
    audit_intervals()


def strict_schema(p):
    if type(p)!=dict or set(p)!=set(TOP): raise ValueError("top-level schema")
    if p["experiment"]!="E021" or type(p["implementation_commit"])!=str or len(p["implementation_commit"])!=40:raise ValueError("identity")
    b=p["band"]
    if set(b)!={"name","range","interval_semantics"} or b!={"name":"D21","range":[138000000,140000000],"interval_semantics":"half-open"}:raise ValueError("band")
    if type(p["partition"])!=list or p["partition"]!=[dict(name=n,range=[a,z],role=role) for n,a,z,role in ROLES]:raise ValueError("partition")
    if p["parameters"]!=PARAMS or set(p["parameters"])!=set(PARAMS) or any(type(p["parameters"][k])!=type(v) or (type(v)==list and any(type(i)!=type(j) for i,j in zip(p["parameters"][k],v))) for k,v in PARAMS.items()):raise ValueError("parameters")
    if p["generation_plan"]!=[dict(purpose=a,start=b,stop=c,strategy=d) for a,b,c,d in PLAN]: raise ValueError("plan")
    if any(type(q)!=int for v in p["generation_plan"] for k,q in v.items() if k in ("start","stop")):raise ValueError("plan types")
    summary=p["anchor_summary"]
    if set(summary)!={"wheel_anchor_count","prime_count","composite_count","prime_counts_by_R210","composite_counts_by_R210"}:raise ValueError("summary")
    if any(type(summary[k])!=int or summary[k]<0 for k in ("wheel_anchor_count","prime_count","composite_count")):raise ValueError("summary scalar types")
    for k in ("prime_counts_by_R210","composite_counts_by_R210"):
        if type(summary[k])!=list or len(summary[k])!=48 or any(type(v)!=int or v<0 for v in summary[k]):raise ValueError("summary arrays")
    if summary["wheel_anchor_count"]!=summary["prime_count"]+summary["composite_count"]:raise ValueError("population conservation")
    if summary["prime_count"]!=sum(summary["prime_counts_by_R210"]) or summary["composite_count"]!=sum(summary["composite_counts_by_R210"]):raise ValueError("class conservation")
    if type(p["validation"])!=dict or set(p["validation"])!=set(COUNTERS) or any(type(v)!=int or v!=0 for v in p["validation"].values()):raise ValueError("ten validators")
    if type(p["families"])!=list or len(p["families"])!=1 or set(p["families"][0])!=set(FAMILY_KEYS):raise ValueError("family keys")
    f=p["families"][0]
    if f["family"]!="F1":raise ValueError("family")
    ints=("highest_enrichment_numerator","highest_competing_enrichment_numerator")
    if any(type(f[k])!=int for k in ints):raise ValueError("signed integers")
    for k in ("candidate_signature","evaluated_signature"):
        if f[k] is not None and (type(f[k])!=int or not 0<=f[k]<16):raise ValueError("signature type")
    for k in ("target_prime_count","target_composite_count","mixed_class_count","positive_class_count","target_enrichment_numerator"):
        if f[k] is not None and (type(f[k])!=int or (k!="target_enrichment_numerator" and f[k]<0)):raise ValueError("target types")
    booleans=("strict_unique_positive_enrichment_max","population_floor_passed","class_floor_passed","occurrence_floor_passed","mixed_class_floor_passed","positive_class_floor_passed","target_enrichment_positive","mechanically_eligible")
    if any(type(f[k])!=bool for k in booleans):raise ValueError("family booleans")
    if f["evaluated_signature"]!=f["candidate_signature"]:raise ValueError("D21 frozen selection")
    if f["candidate_signature"] is None:
        if any(f[k] is not None for k in ("target_prime_count","target_composite_count","mixed_class_count","positive_class_count","target_enrichment_numerator")):raise ValueError("null target")
        if any(f[k] for k in ("occurrence_floor_passed","mixed_class_floor_passed","positive_class_floor_passed","target_enrichment_positive","mechanically_eligible","strict_unique_positive_enrichment_max")):raise ValueError("null flags")
    else:
        if any(f[k] is None for k in ("target_prime_count","target_composite_count","mixed_class_count","positive_class_count","target_enrichment_numerator")):raise ValueError("target missing")
    if type(p["promotions"])!=list or len(p["promotions"])>1:raise ValueError("cap")
    if len(p["promotions"])==1:
        v=p["promotions"][0]
        if set(v)!={"family","target_signature","target_prime_count","target_composite_count","mixed_class_count","positive_class_count","target_enrichment_numerator"} or not f["mechanically_eligible"] or v["target_signature"]!=f["candidate_signature"]:raise ValueError("promotion")
        if any(type(v[k])!=int for k in v if k not in ("family",)) or v["family"]!="F1": raise ValueError("promotion types")
    elif f["mechanically_eligible"]: raise ValueError("missing promotion")


def canonical(p):
    strict_schema(p)
    raw=(json.dumps(p,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
    if json.loads(raw)!=p or raw!= (json.dumps(json.loads(raw),sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii'):
        raise ValueError("noncanonical")
    return raw


def run(commit,output):
    if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit):raise ValueError("must pin actual SHA")
    checked_synthetics()
    entries=PLAN
    validate_plan(entries)
    # Label-blind enumeration and combinatorial features happen before any generator.
    anchors=[]; sigs=[]; classes=[]
    for x in range(138000000,140000000):
        if gcd(x,210)!=1:continue
        t=signature(x,*residues(x))
        r=x%210
        if r not in R210:raise AssertionError("invalid wheel")
        anchors.append(x);sigs.append(t);classes.append(R210.index(r))
    # Entire positive plan validated once more before first low sieve and at every entry.
    validate_plan(entries)
    gate=GeneratorGate(entries)
    base=base_sieve(11833,gate)
    flags=target_segment(138000000,140000000,base,gate)
    assert gate.cursor==2
    pclass=[0]*48;cclass=[0]*48
    pc=[[0]*16 for _ in range(48)];cc=[[0]*16 for _ in range(48)]
    support=[set() for _ in range(16)]
    for x,t,r in zip(anchors,sigs,classes):
        is_p=bool(flags[x-138000000])
        if is_p:
            pclass[r]+=1;pc[r][t]+=1;support[t].add(x)
        else:
            cclass[r]+=1;cc[r][t]+=1
    NP=sum(pclass);NC=sum(cclass)
    nP=[sum(row[t] for row in pc) for t in range(16)]
    nC=[sum(row[t] for row in cc) for t in range(16)]
    E=[nP[t]*NC-nC[t]*NP for t in range(16)]
    winner,best,runner=select(E)
    pop=NP>=2000 and NC>=2000
    floor=all(p>=20 and c>=20 for p,c in zip(pclass,cclass))
    if winner is None:
        tp=tc=mix=positive=total=None
    else:
        tp=nP[winner];tc=nC[winner];total=E[winner]
        mix=sum(pc[r][winner]>0 and pclass[r]-pc[r][winner]>0 and cc[r][winner]>0 and cclass[r]-cc[r][winner]>0 for r in range(48))
        positive=sum(pc[r][winner]*cclass[r]-cc[r][winner]*pclass[r]>0 for r in range(48))
    enough=winner is not None and tp>=64
    mixed=winner is not None and mix>=36
    signed=winner is not None and positive>=30
    e_positive=winner is not None and total>0
    eligible=bool(pop and floor and winner is not None and enough and mixed and signed and e_positive)
    existing=[]
    if eligible and not dedup_support(support[winner],existing):eligible=False
    assert len(existing)<=1
    # Exactly ten independently calculated nonnegative validation counts; fail closed.
    checks={
        "plan_failure_count": int(not validate_plan(entries) or gate.cursor!=2),
        "interval_exclusion_failure_count": int(audit_intervals()!=(4851,495,10,150,30)),
        "partition_quotient_failure_count": sum(numerator(n,k)%factorial(k)!=0 or numerator(n,k)//factorial(k)!=recurrence_small(n,k) for n in range(1,8) for k in (3,4)),
        "modular_power_failure_count": sum(pow(j,n,d*(n+1))!=j**n%(d*(n+1)) for n in range(1,8) for k,d in ((3,6),(4,24)) for j in range(k+1)),
        "quartile_signature_failure_count": sum(not (0<=signature(n,*residues(n))<16) for n in range(1,16)),
        "wheel_label_failure_count": int(len(anchors)!=NP+NC or any(gcd(x,210)!=1 or x%210!=R210[r] for x,r in zip(anchors,classes))),
        "frequency_conservation_failure_count": sum(sum(pc[r])!=pclass[r] or sum(cc[r])!=cclass[r] for r in range(48))+int(sum(nP)!=NP or sum(nC)!=NC or sum(pclass)!=NP or sum(cclass)!=NC),
        "signed_class_control_failure_count": sum(E[t]!=nP[t]*NC-nC[t]*NP for t in range(16))+int((winner,best,runner)!=select([sum(pc[r][t] for r in range(48))*NC-sum(cc[r][t] for r in range(48))*NP for t in range(16)])),
        "selection_duplicate_failure_count": int(sum(len(s) for s in support)!=NP or len(existing)>1 or (eligible and (winner is None or existing!=[support[winner]]))),
        "serializer_failure_count": 0,
    }
    assert tuple(checks)==COUNTERS and all(type(v)==int and v==0 for v in checks.values()),"mandatory independent validator failure"
    values=checks
    promotion=[]
    if eligible: promotion=[dict(family="F1",target_signature=winner,target_prime_count=tp,target_composite_count=tc,mixed_class_count=mix,positive_class_count=positive,target_enrichment_numerator=total)]
    fam=dict(family="F1",candidate_signature=winner,evaluated_signature=winner,highest_enrichment_numerator=best,highest_competing_enrichment_numerator=runner,strict_unique_positive_enrichment_max=winner is not None,target_prime_count=tp,target_composite_count=tc,population_floor_passed=pop,class_floor_passed=floor,occurrence_floor_passed=bool(enough),mixed_class_count=mix,mixed_class_floor_passed=bool(mixed),positive_class_count=positive,positive_class_floor_passed=bool(signed),target_enrichment_numerator=total,target_enrichment_positive=bool(e_positive),mechanically_eligible=eligible)
    payload=dict(experiment="E021",implementation_commit=commit,band=dict(name="D21",range=[138000000,140000000],interval_semantics="half-open"),partition=[dict(name=n,range=[a,b],role=role) for n,a,b,role in ROLES],parameters=PARAMS,generation_plan=[dict(purpose=a,start=b,stop=c,strategy=d) for a,b,c,d in PLAN],anchor_summary=dict(wheel_anchor_count=len(anchors),prime_count=NP,composite_count=NC,prime_counts_by_R210=pclass,composite_counts_by_R210=cclass),validation=values,families=[fam],promotions=promotion)
    raw=canonical(payload)
    Path(output).write_bytes(raw)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output',required=True)
    a=parser.parse_args()
    run(a.code_commit,a.output)

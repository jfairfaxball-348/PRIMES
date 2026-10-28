#!/usr/bin/env python3
"""RS-S041 plots. Read-only reproduction of committed data, no fitting or new tests.

Usage from repository root: python paper/figures/make_all.py
Uses only reciprocity_spectra/results/*.json. Figures are explanatory or
descriptive; plot labels distinguish these from experimental evidence.
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "reciprocity_spectra" / "results"
OUT = Path(__file__).resolve().parent / "generated"
OUT.mkdir(exist_ok=True)
FILES = {
    "s015": "rs_s015_class_tests_2026-10-26.json",
    "s016": "rs_s016_x_dependence_2026-10-26.json",
    "s017": "rs_s017_fresh_classes_2026-10-26.json",
    "s019": "rs_s019_moduli_2026-10-26.json",
    "s020": "rs_s020_rho_partition_2026-10-26.json",
    "s021": "rs_s021_large_x_2026-10-26.json",
    "s022": "rs_s022_cand002_audit_2026-10-26.json",
}
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
SHAPES = ["o", "s", "^", "D", "v", "P"]

def load(k):
    with (DATA / FILES[k]).open(encoding="utf-8") as f:
        return json.load(f)

def make(name, fn):
    plt.rcParams.update({
        "figure.figsize": (6.4, 3.55), "figure.dpi": 120,
        "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 11,
        "legend.fontsize": 8, "savefig.bbox": "tight",
        "axes.spines.top": False, "axes.spines.right": False,
    })
    fig, ax = plt.subplots()
    fn(fig, ax)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / (name + "." + ext), dpi=180)
    plt.close(fig)

def style(ax, xlabel, ylabel, title):
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid(True, alpha=.22)

def overview(fig, ax):
    ax.axis("off")
    nodes = [(0.01,.56,r"$R_X=(\frac{\rho}{\sigma})_6$"),
             (.34,.56,r"$w_\kappa=\bar g\,\chi(\kappa)$"),
             (.68,.56,r"$s_\kappa=\frac{r_\kappa^2-1}{r_1^2-1}N_6^{1/6}$"),
             (.34,.14,r"$t=N_6(\kappa)/X$"),
             (.68,.14,r"crossover $F(t)$ (CONJECTURE)")]
    for x,y,label in nodes:
        ax.text(x,y,label,transform=ax.transAxes,fontsize=13,
                bbox=dict(boxstyle="round,pad=.45",facecolor="#f2f5f8",edgecolor="#6a7b8f"))
    for x1,y1,x2,y2 in [(.23,.60,.32,.60),(.57,.60,.66,.60),(.51,.47,.51,.25),(.57,.19,.66,.19)]:
        ax.annotate("",xy=(x2,y2),xytext=(x1,y1),xycoords="axes fraction",
                    arrowprops=dict(arrowstyle="->",lw=1.5,color="#0072B2"))
    ax.set_title("From an arithmetic residue matrix to a measured crossover",loc="left")

def lattice(fig, ax):
    j = load("s019")
    pts = list({(c["kappa"][0][0][0],c["kappa"][0][0][1])
                for c in j["runs"][0]["prime"]["classes"]})
    xx,yy = zip(*sorted(pts), strict=False)
    ax.scatter(xx,yy,color=PALETTE[0],s=30)
    ax.axhline(0,color="grey",lw=.5)
    ax.axvline(0,color="grey",lw=.5)
    style(ax,r"$a$ in $a+b\omega$",r"$b$ in $a+b\omega$","Sample primary prime representatives")
    ax.text(.02,.03,"Finite illustrative set from RS-S019 classes",transform=ax.transAxes,fontsize=7)

def baseline(fig, ax):
    a,b=load("s016"),load("s021")
    X=[int(k) for k in a["analysis"]["r_u1"].keys()]
    y=[a["analysis"]["r_u1"][str(x)] for x in X]
    for k,v in b["score"]["r_u1"].items():
        X.append(int(k))
        y.append(v)
    pairs=sorted(zip(X,y, strict=False))
    ax.plot([x/1e6 for x,_ in pairs],[v for _,v in pairs],marker="o",color=PALETTE[0])
    style(ax,r"Cutoff $X$ ($10^6$)",r"Baseline $r_1$","Observed baseline strength")

def collapse(fig, ax):
    a,b,c=load("s016"),load("s021"),load("s015")
    for run in a["runs"]+c["runs"][:1]+b["runs"]:
        X=run["X"]
        vals=[]
        if X<=1e6:
            r1=next((r["analysis"]["r_u1"][str(X)] for r in [a] if str(X) in r["analysis"]["r_u1"]),None)
        else:
            r1=b["score"]["r_u1"][str(X)]
        if r1 is None:
            continue
        for item in run["classes"]:
            k=item.get("k")
            if k is None:
                k=item.get("exponents",[None])[0]
            if k not in (1,2,3,4):
                continue
            n=item.get("N6")
            if not n:
                continue
            s=item.get("s")
            if s is None:
                s=((item["r"]**2-1)/(r1**2-1))*n**(1/6)
            vals.append((math.log10(n/X),s))
        if vals:
            ii={160000:0,320000:1,640000:2,1000000:3,2000000:4,4000000:5}[X]
            ax.scatter(*zip(*vals, strict=False), s=9,marker=SHAPES[ii],alpha=.27,
                       color=PALETTE[ii],label=f"$X={X/1e6:g}\\times10^6$")
    bins=a["analysis"]["collapse_bins_t_eq_N6_over_X"]["k234"]
    ax.plot([p["log10_t_lo"]+.25 for p in bins],[p["mean_s"] for p in bins],
            color="black",lw=2.3,label="Frozen discovery bin means")
    style(ax,r"$\log_{10}(t)$, $t=N_6/X$",r"$s_\kappa$","Exponent classes 1–4: shift-aspect profile")
    ax.legend(ncol=2,fontsize=6,loc="lower left")

def residuals(fig, ax):
    j=load("s021")
    p=j["score"]["A"]["bins"]
    xx=[a["log10_t_lo"]+.25 for a in p]
    yy=[a["diff"] for a in p]
    ax.axhspan(-.12,.12,color=PALETTE[2],alpha=.13,label="Registered ±0.12")
    ax.axhline(0,color="black",lw=.7)
    ax.scatter(xx,yy,c=PALETTE[0],s=[10+2*v["n"] for v in p])
    style(ax,r"Half-decade bin centre in $\log_{10}t$",r"Observed mean $s$ minus frozen $F$",
          "RS-S021 fresh-scale holdout residuals")
    ax.legend(loc="upper left")

def pi5(fig, ax):
    j=load("s021")
    for idx,run in enumerate(j["runs"]):
        pts=sorted((c["N"],c["s"]) for c in run["classes"] if c["k"]==5)
        ax.scatter([v[0] for v in pts],[v[1] for v in pts],s=22,
                   marker=SHAPES[idx],color=PALETTE[idx],
                   label=f"$X={run['X']/1e6:g}\\times10^6$")
    ax.axhline(-1,color="black",ls="--",lw=1,label="Conjectured large-$t$ limit")
    style(ax,r"Prime norm $N(\pi)$",r"$s_{\pi^5}$","Observed exponent-five deficit")
    ax.legend()

def moduli(fig, ax):
    j=load("s019")["runs"][0]
    for idx,key in enumerate(["prime","unrestricted"]):
        vals=[(math.log10(c["t"]),c["s"]) for c in j[key]["classes"] if c["k"]!=5 and c["t"]>0]
        ax.scatter(*zip(*vals, strict=False),s=16,alpha=.45,color=PALETTE[idx],label=key)
    style(ax,r"$\log_{10}(N_6/X)$",r"$s_\kappa$",
          "Prime vs. squarefree-modulus profiles, $X=2\\times10^5$")
    ax.legend()

def parity(fig, ax):
    j=load("s020")["settings"]["rational"]["classes"]
    for idx,mod in enumerate([1,7]):
        xs=[]
        ys=[]
        groups={}
        for row in j:
            if row["k"]!=2 or row["N_mod_12"]!=mod:
                continue
            for part,s in row["s_by_part"].items():
                groups.setdefault(int(part),[]).append(s)
        for part in sorted(groups):
            xs.append(part)
            ys.append(sum(groups[part])/len(groups[part]))
        if xs:
            ax.plot(xs,ys,marker=SHAPES[idx],color=PALETTE[idx],label=f"N mod 12 = {mod}")
    style(ax,r"Row part $j=(\rho/\pi)_6$ exponent",r"Mean partitioned $s$",
          "Exploratory row-prime partition, exponent 2")
    ax.legend()

def plateau(fig, ax):
    j=load("s021")
    d=j["stored_trend_K1"]
    d.update({str(k):v for k,v in j["score"]["H+"]["K1"].items()})
    data=sorted((float(k.replace("e5","e5").replace("e6","e6")),v) for k,v in d.items())
    ax.plot([x/1e6 for x,_ in data],[v for _,v in data],color=PALETTE[2],marker="o")
    ax.axhline(1,ls="--",color="grey",label="Open question $F(0^+)=1$")
    style(ax,r"$X$ ($10^6$)",r"$K_1$: small-$t$ band mean","Small-aspect plateau trend")
    ax.legend()

def prereg(fig, ax):
    stages=["S015","S016","S017","S019","S020","S021"]
    events=["FAIL", "EXPLORE", "PASS / FAIL", "PASS", "PASS", "PASS"]
    colors=[PALETTE[1], "#777777",PALETTE[1],PALETTE[2],PALETTE[2],PALETTE[2]]
    for i,(stage,event) in enumerate(zip(stages,events, strict=False)):
        ax.scatter([i],[0],color=colors[i],s=170,zorder=3)
        ax.text(i,.22,event,ha="center",fontsize=8,rotation=30)
        ax.text(i,-.25,stage,ha="center")
    ax.plot(range(len(stages)),[0]*len(stages),color="gray")
    ax.set(xlim=(-.6,5.6),ylim=(-.65,.8),title="Registered tests retain their failures")
    ax.axis("off")

def regimes(fig, ax):
    xx=np.linspace(-2,6,300)
    for X in [5,6]:
        # log10 t = log10 N6 - log10 X
        ax.plot(xx,np.full_like(xx,X),ls="--",lw=1,label=fr"$t=1$ at $\log_{{10}}X={X}$")
    ax.fill_between(xx,xx+2,xx+5,where=(xx+2<=xx+5),alpha=.10,color=PALETTE[0])
    ax.text(1.0,5.8,"fixed class: $N_6$ fixed,\n$X\\to\\infty$ is a separate boundary",fontsize=9)
    style(ax,r"$\log_{10}N_6$",r"$\log_{10}X$","Parameter regions; conceptual, not evidence")
    ax.set_ylim(3,8)
    ax.legend(fontsize=7)

def verification(fig, ax):
    ax.axis("off")
    names=["C residue engine","Stored test fixtures","Lean finite model",
           "1,764-entry faithfulness","26 exact theorems","Comparator / NanoDa"]
    for i,name in enumerate(names):
        xpos=.06+i*.155
        ax.text(xpos,.5,name,rotation=90,ha="center",va="center",fontsize=10,
                bbox=dict(boxstyle="round",facecolor="#eef2f7",edgecolor=PALETTE[0]))
    ax.text(.02,.05,"Verified finite algebra only — not the asymptotic conjectures",
            transform=ax.transAxes,fontsize=9,color=PALETTE[1])

def normalisation(fig, ax):
    j=load("s022")["normalizations"]
    keys=["frozen","control","raw"]
    x=np.arange(3)
    y=[j[k]["median_across_X_spread_of_bin_means"] for k in keys]
    ax.bar(x,y,color=[PALETTE[0],PALETTE[2],PALETTE[1]])
    ax.set_xticks(x,["baseline-normalised","control-referenced","unnormalised"])
    style(ax,"",r"Median across-$X$ bin spread","Normalisation audit; same 600 finite points")
    ax.tick_params(axis="x",labelrotation=12)

def phase(fig,ax):
    j=load("s016")["analysis"]["collapse_bins_t_eq_N6_over_X"]
    for i,k in enumerate(["k2","k3","k4","k5"]):
        pts=j[k]
        ax.plot([a["log10_t_lo"]+.25 for a in pts],
                [a["mean_s"] for a in pts],marker=SHAPES[i],label=f"exponent {k[1:]}",
                color=PALETTE[i])
    style(ax,r"$\log_{10}(N_6/X)$",r"$s_\kappa$",
          "Discovery bin means by exponent class")
    ax.legend()

DRAW = {
    "visual_abstract": overview,
    "primary_lattice": lattice,
    "r1_growth": baseline,
    "crossover": collapse,
    "holdout_residuals": residuals,
    "exponent_five": pi5,
    "moduli": moduli,
    "rho_parity": parity,
    "plateau": plateau,
    "prereg_timeline": prereg,
    "regime_map": regimes,
    "verification": verification,
    "normalisation": normalisation,
    "exponent_profiles": phase,
}
if __name__ == "__main__":
    for name, draw in DRAW.items():
        make(name,draw)
    print(f"Generated {len(DRAW)} vector/PDF + PNG figure pairs in {OUT}")

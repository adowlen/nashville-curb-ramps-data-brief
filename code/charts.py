import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
PKG=os.path.normpath(os.path.join(os.path.dirname(__file__),"..")); S=json.load(open(os.path.join(PKG,"stats.json")))
CHAR="#232323"; AMBER="#e8a33d"; TEAL="#2a9d8f"; LIGHT="#f2f2f2"; GREY="#9a9a9a"; RED="#d95f4b"
plt.rcParams.update({"text.color":LIGHT,"axes.edgecolor":LIGHT,"axes.labelcolor":LIGHT,"xtick.color":LIGHT,"ytick.color":LIGHT,"figure.facecolor":CHAR,"axes.facecolor":CHAR,"savefig.facecolor":CHAR})
os.makedirs(os.path.join(PKG,"charts"),exist_ok=True)
def save(fig,n): fig.tight_layout(); fig.savefig(os.path.join(PKG,"charts",n),dpi=200); plt.close(fig)
# 1. Conformance distribution (full denominator printed)
labels=["Yes","No","Maximum Extent\nFeasible","Technically\nInfeasible","No Ramp","Unknown","Blank"]
keys=["Yes","No","Maximum Extent Feasible","Technically Infeasible","No Ramp","Unknown","Blank"]
vals=[S["conform_counter"][k] for k in keys]; cols=[TEAL,RED,AMBER,"#c98a2d",GREY,GREY,"#6f6f6f"]
fig,ax=plt.subplots(figsize=(8.6,4.8)); ax.barh(labels[::-1],vals[::-1],color=cols[::-1])
for i,v in enumerate(vals[::-1]): ax.text(v+220,i,f"{v:,} ({S['conform_pct'][keys[::-1][i]]}%)",va="center",fontsize=9.5)
ax.set_xlim(0,12200)
ax.set_xlabel("Records (share of all 18,388 audited curb-ramp records)\nConformID normalized: case/spelling variants merged; Unknown and Blank carried on the full denominator", fontsize=9)
ax.set_title("Curb-ramp conformance as recorded - Nashville Curb Ramps, Nov 11, 2026"); save(fig,"chart_conform_distribution.png")
# 2. Lowest Yes shares by district (district-known base printed; all districts n>=110 except none below - smallest district in panel is 48, flag in caption)
items=sorted([(d,v) for d,v in S["by_district"].items() if v["n"]>=100], key=lambda x: x[1]["yes_pct"])[:8]
fig,ax=plt.subplots(figsize=(8.6,4.8)); ax.barh([f"District {d}" for d,_ in items],[v["yes_pct"] for _,v in items],color=RED)
for i,(d,v) in enumerate(items): ax.text(v["yes_pct"]+1.0,i,f"{v['yes_pct']}% Yes  ({v['Yes_n']:,} of {v['n']:,})",va="center",fontsize=9)
ax.set_xlim(0,62)
ax.set_xlabel("Share of the district's audited ramp records recorded Yes (conforming)\nDistrict-known records only: 17,524 of 18,388; districts with 100+ records", fontsize=9)
ax.set_title("Lowest conforming (Yes) shares by council district"); save(fig,"chart_yes_share_by_district.png")
# 3. Audit era (DateAudited era bases printed; era is audit date, not construction date)
eras=["Audited before 2010","Audited 2010-2019","Audited 2020-2026"]
vals3=[S["eras"][e]["yes_pct"] for e in eras]; ns=[S["eras"][e]["n"] for e in eras]
fig,ax=plt.subplots(figsize=(8.6,4.6)); ax.barh(eras[::-1],vals3[::-1],color=AMBER)
for i,(v,n) in enumerate(zip(vals3[::-1],ns[::-1])): ax.text(v+1.2,i,f"{v}% Yes  (n={n:,})",va="center",fontsize=9.5)
ax.set_xlim(0,86)
ax.set_xlabel("Share recorded Yes, by DateAudited era - the era is when the audit was recorded,\nnot when the ramp was built; the 2023 wave (7,899 records) is concentrated in Districts 19, 21, 17 and 6", fontsize=9)
ax.set_title("Conforming share by audit era - do not read as a construction trend"); save(fig,"chart_yes_share_by_era.png")
# 4. No Ramp and DetectableWarning profile (each bar's base printed in its label)
cats=["No Ramp records\n(of 18,388 records)","No Ramp with ProjectType\nUNKNOWN (of 961 No Ramp)","DetectableWarning = 1\n(of 17,758 coded records)","DW = 1 among Yes\n(of 9,100 coded Yes)","DW = 1 among No\n(of 4,034 coded No)"]
dw=S["detectable_warning"]
vals4=[100*S["conform_counter"]["No Ramp"]/S["rows"],100*S["no_ramp_profile"]["project_unknown_n"]/S["no_ramp_profile"]["n"],dw["one_pct_of_coded"],dw["by_conform"]["Yes"]["one_pct_of_coded"],dw["by_conform"]["No"]["one_pct_of_coded"]]
fig,ax=plt.subplots(figsize=(8.6,5.0)); ax.barh(cats[::-1],vals4[::-1],color=TEAL)
for i,v in enumerate(vals4[::-1]): ax.text(v+1.5,i,f"{v:.1f}%",va="center",fontsize=10)
ax.set_xlim(0,112)
ax.set_xlabel("Percent of the base printed in each row label (each bar has its own base)\nDetectableWarning coding (0/1) is not defined in the layer metadata;\nvalues are reported as recorded", fontsize=9)
ax.set_title("No Ramp records are a separate subpopulation; detectable-warning coding"); save(fig,"chart_no_ramp_and_dw.png")
print("charts done")

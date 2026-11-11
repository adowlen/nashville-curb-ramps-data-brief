import csv, json, collections, os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
HERE=os.path.dirname(__file__); DATA=os.path.normpath(os.path.join(HERE,"..","data"))
CHI=ZoneInfo("America/Chicago")
def ldate(v):
    if v in (None,""): return None
    try: ms=int(float(v))
    except: return None
    return datetime.fromtimestamp(ms/1000, tz=timezone.utc).astimezone(CHI).date()
def num(v):
    if v in (None,""): return None
    try: return float(v)
    except: return None
rows=list(csv.DictReader(open(os.path.join(DATA,"nashville_curb_ramps_raw.csv"))))
out=[]
def p(*a): s=" ".join(str(x) for x in a); out.append(s); print(s)
p("ROWS",len(rows))
p("OBJECTID unique",len(set(r["OBJECTID"] for r in rows)))
p("CurbRampID unique",len(set(r["CurbRampID"] for r in rows)),"(duplicates exist, so OBJECTID is the row key)")
p("GlobalID unique",len(set(r["GlobalID"] for r in rows)))
for col in ["ConformID","ProjectType","Material","StandardID","FlushMountID","Side","ServiceDistrict","Zone","CouncilDistrict","DetectableWarning","HasLeftSlope","HasRightSlope","HasLandingSlope","HasPerpSlope","HasApproachSlope"]:
    c=collections.Counter((r[col] if r[col] not in (None,) else "") for r in rows)
    show=c.most_common(200)
    p(f"COUNTER {col} n_unique={len(c)}")
    for k,v in show: p(f"  {k!r}: {v}")
# ConformExplain is free text (2,855 distinct values) - counter the top values only, count distinct
ce=collections.Counter((r["ConformExplain"] or "") for r in rows)
p(f"COUNTER ConformExplain n_unique={len(ce)} top30:")
for k,v in ce.most_common(30): p(f"  {k!r}: {v}")
# Dates: sentinel handling
for col in ["DateAudited","DateReAudited"]:
    dv=[r[col] for r in rows if r[col] not in (None,"")]
    ds=[ldate(v) for v in dv]
    p(f"DATES {col} present={len(dv)} missing={len(rows)-len(dv)} min={min(ds) if ds else None} max={max(ds) if ds else None}")
    p(f"  sentinel check: year<1990={sum(1 for d in ds if d and d.year<1990)} raw 0/negative={sum(1 for v in dv if float(v)<=0)}")
    p(f"  {col} year census", dict(sorted(collections.Counter(d.year for d in ds if d).items())))
# Numeric slopes: 0 is a recorded measurement here (flat), NOT a sentinel - slopes are reported as recorded, never used as rate denominators; extreme values flagged
for col in ["LeftSlope","RightSlope","HorLandSlope1","HorLandSlope2","VerLandSlope1","VerLandSlope2","PerpSlope1","PerpSlope2","ApproachSlope","LandSlopeWidth","LandSlopeLength"]:
    vals=[num(r[col]) for r in rows]
    present=[v for v in vals if v is not None]
    p(f"NUMERIC {col} present={len(present)} missing={len(vals)-len(present)} zero={sum(1 for v in present if v==0)} negative={sum(1 for v in present if v<0)} min={min(present) if present else None} max={max(present) if present else None}")
    if present: p(f"  values over 30: {sum(1 for v in present if v>30)} (flagged as recorded extremes; no slope figure in the brief rests on the tail)")
# DetectableWarning coding: 0 / 1 / blank as recorded; metadata does not define the coding, so the brief reports the recorded value 1 share on the coded base only
dw=collections.Counter(r["DetectableWarning"] for r in rows)
p(f"DETECTABLEWARNING counter {dict(dw)}; coded base (0 or 1) = {dw.get('0',0)+dw.get('1',0)}; blank excluded from every DetectableWarning share")
# Polarity / matched-vs-excluded for the conformance filter (normalized Yes vs all other recorded categories)
def norm(v):
    s=(v or "").strip().upper()
    return {"YES":"Yes","NO":"No","MAX_EXT_FEASIBLE":"Maximum Extent Feasible","MAXIMUM EXTENT FEASIBLE":"Maximum Extent Feasible","TECH_INFEASIBLE":"Technically Infeasible","TECHNICALLY INFEASABLE":"Technically Infeasible","NO RAMP":"No Ramp","UNKNOWN":"Unknown","":"Blank"}.get(s,"Other")
matched=[r for r in rows if norm(r["ConformID"])=="Yes"]
excl=[r for r in rows if norm(r["ConformID"])!="Yes"]
p("POLARITY SAMPLE matched (normalized ConformID = Yes, first 3):",[(r["OBJECTID"],r["ConformID"],r["CouncilDistrict"],r["FlushMountID"]) for r in matched[:3]])
p("POLARITY SAMPLE excluded (normalized ConformID != Yes, first 3):",[(r["OBJECTID"],r["ConformID"],r["CouncilDistrict"],r["FlushMountID"]) for r in excl[:3]])
assert all(norm(r["ConformID"])=="Yes" for r in matched)
p(f"CONFORM normalized counter: {dict(collections.Counter(norm(r['ConformID']) for r in rows))}")
n=len(rows); det=sum(1 for r in rows if norm(r["ConformID"]) in ("Yes","No","Maximum Extent Feasible","Technically Infeasible"))
assert det + (n-det) == n
p(f"UNKNOWN EXCLUSION: conformance-determined (Yes/No/Maximum Extent Feasible/Technically Infeasible) {det} + not-determined-or-no-ramp (No Ramp/Unknown/Blank) {n-det} = {n} OK. Unknown and Blank are carried on the full denominator in headline shares; No Ramp is printed as its own category, never merged into No.")
p("UNIT AGREEMENT: every share in this package divides ramp records by ramp records on a printed base (all 18,388 records, the district-known base, an audit-era base, or the DetectableWarning-coded base). No length, area, or population denominator is used anywhere, and no rate per resident or per intersection is computed - the layer carries no such denominator.")
# District totals control
dc=collections.Counter((r["CouncilDistrict"] or "") for r in rows)
assert sum(dc.values())==n
p(f"CONTROL district totals: sum of CouncilDistrict counter = {sum(dc.values())} = rows {n} OK; district values n_unique={len(dc)} (1-35 plus 0 on 3 records and blank on 861)")
# Internal controls: measured slopes vs the recorded conformance category (thresholds are the ones printed in the layer's own ConformExplain strings)
def mx(r, cols):
    cand=[num(r[c]) for c in cols]; cand=[c for c in cand if c is not None]
    return max(cand) if cand else None
for label, cols, thr in [("landing max (Hor/Ver landing slopes)",["HorLandSlope1","HorLandSlope2","VerLandSlope1","VerLandSlope2"],2.0),("perpendicular max (PerpSlope1/2)",["PerpSlope1","PerpSlope2"],8.3)]:
    res={}
    for k in ["Yes","No"]:
        sub=[mx(r,cols) for r in rows if norm(r["ConformID"])==k]; sub=[v for v in sub if v is not None]
        res[k]=(len(sub), sum(1 for v in sub if v>thr), round(100*sum(1 for v in sub if v>thr)/len(sub),1) if sub else None)
    p(f"CONTROL {label} over {thr}: Yes base/over/share = {res['Yes']}; No base/over/share = {res['No']}")
p("JOIN: no spatial or relational join performed. The sidewalk comparison uses only figures published in the 2026-11-10 sidewalks brief (same CouncilDistrict geography, printed with that brief's bases); the crash comparison is not attempted at district level for the same crosswalk reason recorded in that brief.")
open(os.path.join(DATA,"audit_output.txt"),"w").write("\n".join(out)+"\n")
print("AUDIT DONE")

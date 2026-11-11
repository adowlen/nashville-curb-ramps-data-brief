import csv, json, collections, os, statistics
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
HERE=os.path.dirname(__file__); PKG=os.path.normpath(os.path.join(HERE,"..")); DATA=os.path.join(PKG,"data")
CHI=ZoneInfo("America/Chicago")
def ld(v):
    if v in (None,""): return None
    return datetime.fromtimestamp(int(float(v))/1000, tz=timezone.utc).astimezone(CHI).date()
def yr(v):
    d=ld(v); return d.year if d else None
def num(v):
    if v in (None,""): return None
    try: return float(v)
    except: return None
rows=list(csv.DictReader(open(os.path.join(DATA,"nashville_curb_ramps_raw.csv"))))
N=len(rows)
def pct(n,d): return round(100*n/d,1) if d else None
def norm(v):
    s=(v or "").strip().upper()
    return {"YES":"Yes","NO":"No","MAX_EXT_FEASIBLE":"Maximum Extent Feasible","MAXIMUM EXTENT FEASIBLE":"Maximum Extent Feasible","TECH_INFEASIBLE":"Technically Infeasible","TECHNICALLY INFEASABLE":"Technically Infeasible","NO RAMP":"No Ramp","UNKNOWN":"Unknown","":"Blank"}.get(s,"Other")
CATS=["Yes","No","Maximum Extent Feasible","Technically Infeasible","No Ramp","Unknown","Blank"]
conf_raw=collections.Counter((r["ConformID"] if r["ConformID"] is not None else "") for r in rows)
conf=collections.Counter(norm(r["ConformID"]) for r in rows)
determined=sum(conf[c] for c in ["Yes","No","Maximum Extent Feasible","Technically Infeasible"])
# District panel: CouncilDistrict is a clean integer field; blank (861) and 0 (3) excluded from district figures, printed as excluded
dist_rows=collections.defaultdict(list); dist_excluded=0
for r in rows:
    s=(r["CouncilDistrict"] or "").strip()
    if s.isdigit() and 1<=int(s)<=35: dist_rows[int(s)].append(r)
    else: dist_excluded+=1
district_panel={}
for d in sorted(dist_rows):
    sub=dist_rows[d]; n=len(sub); c=collections.Counter(norm(r["ConformID"]) for r in sub)
    district_panel[str(d)]={"n":n, **{f"{k}_n":c[k] for k in CATS}, "yes_pct":pct(c["Yes"],n), "no_pct":pct(c["No"],n), "no_ramp_pct":pct(c["No Ramp"],n), "small_base_flag": n<30}
district_known=sum(len(v) for v in dist_rows.values())
# Audit eras by DateAudited year (Chicago local date): pre-2010 / 2010-2019 / 2020-2026 / no date
def era(r):
    y=yr(r["DateAudited"])
    if y is None: return "No audit date"
    if y<2010: return "Audited before 2010"
    if y<=2019: return "Audited 2010-2019"
    return "Audited 2020-2026"
eras={}
for e in ["Audited before 2010","Audited 2010-2019","Audited 2020-2026","No audit date"]:
    sub=[r for r in rows if era(r)==e]; c=collections.Counter(norm(r["ConformID"]) for r in sub)
    eras[e]={"n":len(sub), **{f"{k}_n":c[k] for k in CATS}, "yes_pct":pct(c["Yes"],len(sub)), "no_pct":pct(c["No"],len(sub))}
audit_years=collections.Counter(yr(r["DateAudited"]) for r in rows if yr(r["DateAudited"]))
y2023=[r for r in rows if yr(r["DateAudited"])==2023]
y2023_dist=collections.Counter((r["CouncilDistrict"] or "").strip() for r in y2023)
# DetectableWarning: recorded 0/1/blank; shares on the coded base only
dw_all=collections.Counter(r["DetectableWarning"] for r in rows)
dw_by_conf={}
for k in CATS:
    sub=[r for r in rows if norm(r["ConformID"])==k]; c=collections.Counter(r["DetectableWarning"] for r in sub)
    coded=c.get("0",0)+c.get("1",0)
    dw_by_conf[k]={"n":len(sub),"coded_n":coded,"one_n":c.get("1",0),"one_pct_of_coded":pct(c.get("1",0),coded)}
# No-category explanations (free text, trimmed, top values) + blank-ish share
no_sub=[r for r in rows if norm(r["ConformID"])=="No"]
no_explain=collections.Counter((r["ConformExplain"] or "").strip() for r in no_sub)
explain_blankish=sum(1 for r in rows if (r["ConformExplain"] or "").strip() in ("","."))
# No Ramp subpopulation profile
nr=[r for r in rows if norm(r["ConformID"])=="No Ramp"]
nr_profile={"n":len(nr),"dated_n":sum(1 for r in nr if r["DateAudited"]),"project_unknown_n":sum(1 for r in nr if r["ProjectType"]=="UNKNOWN"),"dw_blank_n":sum(1 for r in nr if r["DetectableWarning"]==""),"dw_one_n":sum(1 for r in nr if r["DetectableWarning"]=="1")}
# Reaudits
re=[r for r in rows if r["DateReAudited"]]
re_conf=collections.Counter(norm(r["ConformID"]) for r in re)
# Internal controls: measured slopes vs category (thresholds printed in the layer's own ConformExplain strings)
def mx(r, cols):
    cand=[num(r[c]) for c in cols]; cand=[c for c in cand if c is not None]
    return max(cand) if cand else None
def control(cols, thr):
    out={}
    for k in ["Yes","No"]:
        vals=[mx(r,cols) for r in rows if norm(r["ConformID"])==k]; vals=[v for v in vals if v is not None]
        out[k]={"base_n":len(vals),"over_n":sum(1 for v in vals if v>thr),"over_pct":pct(sum(1 for v in vals if v>thr),len(vals))}
    return out
controls={"landing_over_2pct":control(["HorLandSlope1","HorLandSlope2","VerLandSlope1","VerLandSlope2"],2.0),"perp_over_8_3pct":control(["PerpSlope1","PerpSlope2"],8.3)}
# Flush mount coherence control
fm={}
for k in ["Yes","No"]:
    sub=[r for r in rows if norm(r["ConformID"])==k]; c=collections.Counter(r["FlushMountID"] for r in sub)
    fm[k]={"n":len(sub),"less_1_4_code_n":c.get("LESS_1_4_INCH",0),"greater_1_4_code_n":c.get("GREATER_1_4_INCH",0)}
stats={
 "dataset":"Nashville Curb Ramps (Curb_Ramps_view, layer 0)","snapshot_date":"2026-11-11","rows":N,
 "unit":"one row = one audited curb-ramp record as served by the view","server_count":18388,
 "conform_raw_counter":{k:v for k,v in conf_raw.most_common()},
 "conform_counter":{k:conf[k] for k in CATS},"conform_pct":{k:pct(conf[k],N) for k in CATS},
 "conform_determined_n":determined,"yes_pct_of_determined":pct(conf["Yes"],determined),
 "not_yes_n":N-conf["Yes"],"not_yes_pct":pct(N-conf["Yes"],N),
 "district_known_n":district_known,"district_excluded_n":dist_excluded,"districts_with_ramps":len(district_panel),
 "by_district":district_panel,"eras":eras,
 "audit_year_counter":{str(k):v for k,v in sorted(audit_years.items())},
 "audit_2023":{"n":len(y2023),"share_of_all_pct":pct(len(y2023),N),"top_districts":y2023_dist.most_common(6)},
 "dateaudited_range":[str(min(ld(r["DateAudited"]) for r in rows if ld(r["DateAudited"]))),str(max(ld(r["DateAudited"]) for r in rows if ld(r["DateAudited"])))],
 "dateaudited_present_n":sum(1 for r in rows if r["DateAudited"]),"datereaudited_n":len(re),
 "datereaudited_range":[str(min(ld(r["DateReAudited"]) for r in re)),str(max(ld(r["DateReAudited"]) for r in re))],
 "reaudit_conform":{k:re_conf[k] for k in CATS},
 "detectable_warning":{"counter":{("blank" if k=="" else k):v for k,v in dw_all.items()},"coded_n":dw_all.get("0",0)+dw_all.get("1",0),"one_pct_of_coded":pct(dw_all.get("1",0),dw_all.get("0",0)+dw_all.get("1",0)),"by_conform":dw_by_conf},
 "no_explain_top":[list(x) for x in no_explain.most_common(12)],"conform_explain_blankish_n":explain_blankish,
 "no_ramp_profile":nr_profile,"controls_slope":controls,"controls_flush_mount":fm,
 "comparison_published":{"sidewalks_2026_11_10":{"segments":14938,"poor_district11_pct":30.7,"poor_district11_n":175,"poor_district11_base":570,"district21_poor_n":212,"repo":"https://github.com/adowlen/nashville-sidewalks-data-brief"}},
}
json.dump(stats, open(os.path.join(PKG,"stats.json"),"w"), indent=2)
with open(os.path.join(DATA,"conform_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["conform_normalized","records","pct_of_all_records"])
    for k in CATS: w.writerow([k,conf[k],pct(conf[k],N)])
with open(os.path.join(DATA,"conform_raw_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["conform_as_recorded","records"])
    for k,v in conf_raw.most_common(): w.writerow([k if k!="" else "(blank)",v])
with open(os.path.join(DATA,"district_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["district","records","yes_n","yes_pct","no_n","no_pct","max_extent_feasible_n","technically_infeasible_n","no_ramp_n","no_ramp_pct","unknown_n","blank_n","small_base_flag"])
    for d,v in district_panel.items(): w.writerow([d,v["n"],v["Yes_n"],v["yes_pct"],v["No_n"],v["no_pct"],v["Maximum Extent Feasible_n"],v["Technically Infeasible_n"],v["No Ramp_n"],v["no_ramp_pct"],v["Unknown_n"],v["Blank_n"],v["small_base_flag"]])
with open(os.path.join(DATA,"era_panel.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["audit_era","records","yes_n","yes_pct","no_n","no_pct","max_extent_feasible_n","technically_infeasible_n","no_ramp_n","unknown_n","blank_n"])
    for e,v in eras.items(): w.writerow([e,v["n"],v["Yes_n"],v["yes_pct"],v["No_n"],v["no_pct"],v["Maximum Extent Feasible_n"],v["Technically Infeasible_n"],v["No Ramp_n"],v["Unknown_n"],v["Blank_n"]])
print(json.dumps({"conform":stats["conform_counter"],"pct":stats["conform_pct"],"determined":determined,"yes_of_determined":stats["yes_pct_of_determined"]},indent=1))
print("districts by yes_pct:", sorted([(d,v["yes_pct"],v["n"]) for d,v in district_panel.items()], key=lambda x:x[1])[:6])
print("districts by no count:", sorted([(d,v["No_n"],v["n"]) for d,v in district_panel.items()], key=lambda x:-x[1])[:5])
print("eras:", {k:(v["n"],v["yes_pct"]) for k,v in eras.items()})
print("dw:", stats["detectable_warning"]["one_pct_of_coded"], stats["no_ramp_profile"], stats["controls_slope"])

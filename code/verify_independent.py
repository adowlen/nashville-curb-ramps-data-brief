# Second implementation (pandas) + live server count; independent of build_stats.py
import pandas as pd, json, os, urllib.request, urllib.parse
PKG=os.path.normpath(os.path.join(os.path.dirname(__file__),".."))
S=json.load(open(os.path.join(PKG,"stats.json")))
df=pd.read_csv(os.path.join(PKG,"data","nashville_curb_ramps_raw.csv"), dtype=str, keep_default_na=False)
MAP={"YES":"Yes","NO":"No","MAX_EXT_FEASIBLE":"Maximum Extent Feasible","MAXIMUM EXTENT FEASIBLE":"Maximum Extent Feasible","TECH_INFEASIBLE":"Technically Infeasible","TECHNICALLY INFEASABLE":"Technically Infeasible","NO RAMP":"No Ramp","UNKNOWN":"Unknown","":"Blank"}
conf=df["ConformID"].str.strip().str.upper().map(lambda s: MAP.get(s,"Other"))
dist=pd.to_numeric(df["CouncilDistrict"], errors="coerce")
checks=[]
def chk(name, got, want, tol=0): checks.append({"check":name,"got":got,"want":want,"pass":bool(abs((got or 0)-(want or 0))<=tol) if isinstance(got,(int,float)) and isinstance(want,(int,float)) else bool(got==want)})
chk("rows", len(df), S["rows"])
chk("server_count_live", json.load(urllib.request.urlopen("https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Curb_Ramps_view/FeatureServer/0/query?"+urllib.parse.urlencode({"where":"1=1","returnCountOnly":"true","f":"json"}), timeout=60))["count"], S["server_count"])
for c in ["Yes","No","Maximum Extent Feasible","Technically Infeasible","No Ramp","Unknown","Blank"]: chk(f"conform_{c}", int((conf==c).sum()), S["conform_counter"][c])
chk("yes_pct", round(100*(conf=="Yes").mean(),1), S["conform_pct"]["Yes"])
chk("determined_n", int(conf.isin(["Yes","No","Maximum Extent Feasible","Technically Infeasible"]).sum()), S["conform_determined_n"])
chk("district_known_n", int(((dist>=1)&(dist<=35)).sum()), S["district_known_n"])
chk("district19_n", int((dist==19).sum()), S["by_district"]["19"]["n"]); chk("district19_no", int(((dist==19)&(conf=="No")).sum()), S["by_district"]["19"]["No_n"])
chk("district18_yes_pct", round(100*(conf[dist==18]=="Yes").mean(),1), S["by_district"]["18"]["yes_pct"])
chk("district11_no_ramp", int(((dist==11)&(conf=="No Ramp")).sum()), S["by_district"]["11"]["No Ramp_n"])
chk("dw_one_n", int((df["DetectableWarning"]=="1").sum()), S["detectable_warning"]["counter"]["1"])
chk("dw_coded_n", int(df["DetectableWarning"].isin(["0","1"]).sum()), S["detectable_warning"]["coded_n"])
chk("reaudited_n", int((df["DateReAudited"]!="").sum()), S["datereaudited_n"])
chk("no_ramp_project_unknown", int(((conf=="No Ramp")&(df["ProjectType"]=="UNKNOWN")).sum()), S["no_ramp_profile"]["project_unknown_n"])
aud=pd.to_datetime(df["DateAudited"], unit="ms", utc=True, errors="coerce").dt.tz_convert("America/Chicago")
chk("audited_2023_n", int((aud.dt.year==2023).sum()), S["audit_year_counter"]["2023"])
def mx(cols):
    # DataFrame.max(axis=1) skips missing values; a Series.combine(max) would propagate NaN from a blank first column (root-caused 2026-11-11: exactly 2 records, OBJECTID 16662 and 16792, differ between the two forms)
    return pd.DataFrame({c: pd.to_numeric(df[c], errors="coerce") for c in cols}).max(axis=1)
land=mx(["HorLandSlope1","HorLandSlope2","VerLandSlope1","VerLandSlope2"])
chk("control_no_landing_over2", int(((conf=="No")&(land>2)).sum()), S["controls_slope"]["landing_over_2pct"]["No"]["over_n"])
chk("control_yes_landing_over2", int(((conf=="Yes")&(land>2)).sum()), S["controls_slope"]["landing_over_2pct"]["Yes"]["over_n"])
res={"checks":checks,"pass":sum(1 for c in checks if c["pass"]),"total":len(checks)}
json.dump(res, open(os.path.join(PKG,"data","verify_independent_output.json"),"w"), indent=2)
print(res["pass"],"/",res["total"]); [print("FAIL",c) for c in checks if not c["pass"]]

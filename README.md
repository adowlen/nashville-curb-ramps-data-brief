# Nashville Curb Ramps - a Machine Readable data brief

![9,103 of 18,388 audited Nashville curb-ramp records (49.5 percent) are recorded Yes (conforming)](hero.png)

Of **18,388 audited curb-ramp records** in Nashville's Curb Ramps layer, **9,103 (49.5 percent) are recorded Yes for conformance, 4,035 (21.9 percent) No, 2,425 (13.2 percent) Maximum Extent Feasible, and 1,226 (6.7 percent) Technically Infeasible**, with 961 (5.2 percent) recorded No Ramp, 470 Unknown, and 168 blank. District 18 records the lowest Yes share (36.3 percent, 273 of 752); District 11 records a 39.8 percent Yes share and the highest No Ramp share (134 of 704, 19.0 percent). The No Ramp records are a separate, mostly undated subpopulation (91.2 percent carry ProjectType UNKNOWN) and are never merged into No.

Full brief: [brief-draft.md](brief-draft.md) | Sources: [sources.md](sources.md) | Verification: [verification.md](verification.md)

## Contents

- `brief-draft.md` - the brief
- `hero.png` - headline graphic (generated illustration, brand palette, headline composited on top)
- `charts/` - conformance distribution, lowest Yes shares by council district, Yes share by audit era, No Ramp and detectable-warning profile
- `stats.json` - every headline figure with its population printed
- `data/` - panels (conformance, conformance as recorded, district, audit era), the raw snapshot CSV (the layer carries no personal data - street names and ramp measurement fields only, checked in verification.md), the pre-flight audit output, the pull log, the source layer metadata, and the independent verifier output
- `code/` - `pull_data.py`, `audit_section10.py`, `build_stats.py`, `verify_independent.py`, `charts.py`, `hero_composite.py`
- `verification.md` - pre-flight audit, methods checklist, sync gate, story gate

## Reproduce

```
python3 code/pull_data.py          # full-layer pull from the live service (snapshot will drift from the archived one)
python3 code/audit_section10.py    # writes data/audit_output.txt
python3 code/build_stats.py        # writes stats.json and data/*_panel.csv
python3 code/verify_independent.py # second implementation (pandas) + live server count
python3 code/charts.py
python3 code/hero_composite.py     # composites the headline over the art in hero_source/
```

Dependencies (matching the code's actual imports): Python 3 standard library plus pandas (verifier only), matplotlib (charts only), and Pillow (hero composite only). The pull, audit, and build scripts use only the standard library.

## Source

Curb Ramps (Curb_Ramps_view), Metropolitan Government of Nashville and Davidson County via the Nashville Open Data Portal, ArcGIS FeatureServer layer 0 (services2.arcgis.com/HdTo6HJqh92wn4D8). Snapshot November 11, 2026.

## License

Brief text and derived data products: CC BY 4.0 (see LICENSE). Underlying records are Metro Nashville government open data.

*Machine Readable is a public-good civic data project by Alex Dowlen.*

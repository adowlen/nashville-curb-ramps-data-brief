# Reviewer notes - Nashville Curb Ramps brief (2026-11-11)

## Thesis recorded before district/era analysis (Standards Section 13.1)
Written after the pull and the Section 10 audit counters, before district, era, and explanation analysis: "About half of Nashville's audited curb-ramp records are recorded as conforming, nonconformance concentrates in a small number of council districts, and a distinct set of records describes locations with no ramp at all."

## Thesis revision (after the audit-era and subpopulation analysis, before drafting)
The concentration clause held in a specific form: District 18 records the lowest Yes share (36.3 percent), District 11 the second-lowest among larger districts (39.8 percent) plus the highest No Ramp share (19.0 percent), and District 19 the largest No count (610). The analysis added two findings the original thesis did not carry: (1) the No Ramp records are a distinct administrative subpopulation (91.2 percent ProjectType UNKNOWN, 64.3 percent undated), so they are printed as their own category and never merged into No; (2) audit-era Yes shares (63.5 / 54.4 / 45.1 percent) cannot be read as a construction trend, because DateAudited is an audit date, the layer carries no construction date, and the 2023 wave (43.0 percent of the layer) is concentrated in Districts 19, 21, 17, and 6. Revised thesis, which the findings are ordered to serve: "About 1 in 2 of Nashville's audited curb-ramp records is recorded Yes (conforming) and 4,035 are recorded No, with the lowest Yes shares in Districts 18 and 11 - and 961 records describe locations with no ramp, recorded as a separate, mostly undated register, so the layer reads as an audit program plus a no-ramp list, not a single failure rate."

## Claims most likely to be challenged
- The category names: the layer metadata defines none of the ConformID categories. The brief reports each under its recorded name, prints the full raw counter (13 values), and asks NDOT for definitions in Who can act. A reader with program documentation may hold definitions that refine "Maximum Extent Feasible" or "Technically Infeasible"; the brief claims only the recorded distribution.
- The DetectableWarning reading: the metadata does not define the 0/1 coding. The brief reports the recorded value 1 and its shares on the coded base (17,758 records) only, and does not assert what a 1 certifies beyond the field name.
- District 11's No Ramp share (19.0 percent): it is a share of audited records, not of corners. The brief prints that caveat in the district section itself, because the layer holds no unaudited-corner count.
- The audit-era figures: a reader could cite the 63.5-to-45.1 percent era decline as a construction-quality trend. The brief pre-empts this in the era section's heading, text, and chart title: DateAudited is not a construction date, and the 2023 wave's district concentration is printed with the figures.

## Incomplete checks
- No official definitions exist in the layer metadata for ConformID, DetectableWarning, ProjectType, or StandardID; none could be checked beyond the metadata archived in the package. Recorded as an incomplete check; the brief restricts each field to its recorded values accordingly.
- No district-level crash comparison could be performed: the crash layer's published geography is precinct and ZIP, this layer's is council district, and no verified crosswalk exists in this package. The brief states this limitation in its own comparison section.
- ConformExplain is free text (2,855 distinct values; 10,479 records blank, space, or punctuation only), so no exhaustive classification of No reasons is possible; the brief counts only the most common exact strings and labels them as such.
- Slope tails: individual slope fields carry extreme recorded values (LeftSlope maximum 307.0). No brief figure uses a slope average; the controls use over-threshold shares only. The tails are recorded in the audit output, not investigated further.

## Surprises
- The No Ramp subpopulation's profile: 876 of 961 carry ProjectType UNKNOWN (of only 924 such records layer-wide), and 618 of the layer's 724 undated records are No Ramp records.
- The 2023 audit wave: 7,899 records, 43.0 percent of the whole layer, in a single year - and 853 of them carry no district.
- Even among records recorded Yes, only 50.9 percent of coded records carry DetectableWarning = 1.
- CurbRampID is not unique (18,156 distinct values on 18,388 records); OBJECTID is the row key.

## Blocking defects
None. Hero image was generated and composited in this run (headline 49.5 percent) and viewed before publication - narrative scene (audit worker measuring a ramp with tactile warnings, a wheelchair user at a corner with no ramp, Nashville skyline), brand palette, headline fully legible on the dark scrim field.

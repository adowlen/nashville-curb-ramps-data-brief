# Sources

## Primary source for every figure in this brief

1. **Curb Ramps (Curb_Ramps_view), Metropolitan Government of Nashville and Davidson County, Nashville Open Data Portal.** ArcGIS FeatureServer layer 0, services2.arcgis.com/HdTo6HJqh92wn4D8. Snapshot pulled November 11, 2026: 18,388 records, verified at pull time against the server's own returnCountOnly count (18,388). Layer metadata archived in this package at data/source-metadata-layer.json; the layer's data was last edited November 10, 2026 per the service listing (editingInfo.dataLastEditDate).
   - Service: https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Curb_Ramps_view/FeatureServer/0
   - Fields used: CurbRampID, DateAudited, DateReAudited, ProjectType, OnStreet, FromStreet, ToStreet, Side, CouncilDistrict, Material, StandardID, ConformID, ConformExplain, FlushMountID, DetectableWarning, and the recorded slope fields (LeftSlope, RightSlope, HorLandSlope1, HorLandSlope2, VerLandSlope1, VerLandSlope2, PerpSlope1, PerpSlope2). The metadata does not define the ConformID categories, the DetectableWarning coding, or the ProjectType codes; the brief records that absence and assigns no definitions.
   - Personal-data check: the layer's fields are street names, ramp measurements, conformance and audit fields, and district. It carries no personal data (no individual names, contact fields, or parcel-owner fields), so the raw snapshot CSV ships in this repository.

## Comparison source (published Machine Readable brief only)

2. **Nashville Sidewalks Inventory (Machine Readable, November 10, 2026)** - 14,938 inventoried sidewalk segments, 3,762 (25.2 percent) recorded Fair or Poor; District 11 Poor share 30.7 percent (175 of 570 segments). Used with that brief's bases printed; both layers use Metro Council districts, and no combined rate was computed (different populations and units). Repository: https://github.com/adowlen/nashville-sidewalks-data-brief

## Repository and license

Full code, charts, panels, and verification notes: https://github.com/adowlen/nashville-curb-ramps-data-brief
Brief text and data products: CC BY 4.0 (LICENSE in the package). The underlying records are published by Metro Nashville as government open data.

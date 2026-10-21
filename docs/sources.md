# Sources and fact checks

Each bullet states what was checked and the limit of that check. Official source content was reviewed on 2026-10-21; live pages may change.

## Competition / format

- [DrivenData problem description, page 967](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/) — defines the task as predicting geological faults indicative of geothermal resources; says test faults were manually identified by experts and are not in the current public USGS database; describes GeoDAWN/INGENIOUS datasets, the distance-weighted Tversky metric, α=0.2, β=0.8, and a 300 m triangular kernel; specifies EPSG:32611, 100 m, matching bounds, one float32 band, predictions in [0,1], and null/NaN outside bounds. This is the authoritative source for the submission contract used here.
- [DrivenData competition home](https://www.drivendata.org/competitions/306/competition-doe-gems/) — competition entry point, prize and process overview.
- [DrivenData data page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/) — official data download location. Access requires signing in/enrolling; no data files were present in this checkout and no auth was used.
- [DrivenData public leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/) — dynamic public standings. The page displayed xiaofanhu at 0.4413 on 2026-10-21. This is a public-board observation, not a receipt for a GEMSDOE81 file and not a private-test result.
- [DOE/NLR Official Rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf) — September 2026 official rules; link retained for eligibility, data-use, submission, and prize-round conditions. The PDF was opened; this project does not claim a full legal review.
- [DrivenData reference solution](https://github.com/drivendataorg/gems-prize-reference-solution) — organizer-published baseline implementation. The reference repository is not a substitute for the shared holdout evaluator required by this project's run protocol.

## Official study data

- [USGS GeoDAWN airborne magnetic/radiometric data release](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and) — USGS describes the airborne magnetic, radiometric, and lidar acquisition and links DOI 10.5066/P93LGLVQ. This supports the provenance of GeoDAWN layers, not any candidate score.
- [DOE GDR INGENIOUS regional dataset compilation, DOI 10.15121/1881483](https://gdr.openei.org/submissions/1391) — page states publicly accessible under CC BY 4.0 and lists data for 2 m temperature probes, geodetic shear/dilation, heat flow, MT conductance, magnetics/gravity, paleogeothermal features, seismicity, springs/wells, and chemistry. The landing page and resource list were checked; this checkout did not fetch the archives or verify their bytes.
- [Great Basin Center for Geothermal Energy — INGENIOUS](https://gbcge.org/current-projects/ingenious/) — project scope, goals, collaborators, and linked publications; source for context, not a competition score.
- [USGS blind geothermal play-fairway report](https://www.usgs.gov/publications/discovering-blind-geothermal-systems-great-basin-region-integrated-geologic-and) — reports blind-system cases supported by multiple data types including structural setting, geophysics, shallow temperature, and well-water geothermometry. This is regional scientific context, not a validation of H81-A.

## Candidate external sources checked

- [USGS Open-File Report 2013–1139, ASTER hydrothermal alteration maps](https://pubs.usgs.gov/publication/ofr20131139) and [USGS MRData spatial page](https://mrdata.usgs.gov/surficial-mineralogy/ofr-2013-1139/) — official report maps hydrothermal silica-rich, propylitic, argillic, and phyllic units; MRData lists spatial services and downloadable products. The report describes central and southern Basin and Range coverage; exact overlap with GeoDAWN was not checked. Therefore not a cleared input.
- [USGS Landsat Collection 2 Surface Temperature](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature) — describes global Level-2 temperature products, Landsat availability, download route, scale factors, and no use restrictions. Specific scene coverage/cloudiness over the target grid was not checked.
- [USGS Landsat Collection 2 Surface Reflectance](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-reflectance) — describes Level-2 reflectance and access; no imagery was downloaded.
- [NASA/ASF DAAC Sentinel-1 data](https://asf.alaska.edu/data-sets/sar-data-sets/sentinel-1/sentinel-1-data-and-imagery/) — describes Sentinel-1 access via ASF; ASF requires a free Earthdata Login and EULA for downloads. No account, scene-pair search, or download was available here.

## Provenance of H33 discussion

- [GEMSDOE32 site](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html) — original page describes the H33-2-B2 artifact and explicitly says its 0.2747 value is a model projection, not a score, and that no organizer score existed for its artifacts at that time.
- [GEMSDOE32 artifact audit](https://github.com/buffedlizard55-lab/GEMSDOE32/blob/main/docs/downloads/gemsdoe32-h33-h33-2-b2-20261004T220000Z-e5eb6e7e-audit.json) — first-party audit of the historical file. Its bytes were not copied into this repository and its measurements were not independently reproduced here.
- [GEMSDOE77 later H33 forensic report](https://github.com/buffedlizard55-lab/GEMSDOE77/blob/main/reports/why_02778.md) — secondary analysis reported by a sibling project. It is not an official receipt and was not independently rerun in this checkout.

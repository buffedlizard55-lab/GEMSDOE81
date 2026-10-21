# Provisional hypothesis screen — not implementation authorization

**Status:** this checkout has no assigned method paragraph, data, shared feature cache, evaluator/writer, or registry. The items below are a *screening shortlist*, not proof that a method is unique across all GEMSDOE repositories. A registry-wide novelty/overlap scan is mandatory before selecting one. No surface has been calculated, no leakage canary or holdout was run, and no weekly slot is authorized.

Ranks below are qualitative expected value per implementation cost, not predicted scores. No numeric DTI projection is made. The non-fault mimic is named for each hypothesis. The top candidate is H81-A, but it cannot be validated until its data, the shared template, and an assigned lane are present.

| rank | candidate | scientific upside | cost / blocker | novelty confidence |
|---:|---|---|---|---|
| 1 | H81-A — chemistry-conditioned hydrothermal conduit residuals | high, conditional on point coverage | medium; DOE GDR dataset is publicly listed, but files are not in this checkout | low-to-medium; related thermal/geothermal lanes exist, chemistry-specific features need registry scan |
| 2 | H81-B — hydrothermal alteration mineral boundaries | high if the footprint overlaps | high; large USGS vector dataset and AOI coverage unresolved | medium; not present locally, cross-repository scan needed |
| 3 | H81-C — multi-date surface-temperature residual lineaments | medium; direct heat proxy but sparse | medium-to-high; exact scenes, clouds, and time coverage not checked | low-to-medium; older temperature proxies exist, satellite residual method needs registry scan |
| 4 | H81-D — stream-profile knickzone and basin-response graph | medium, with useful no-new-data falsification | low-to-medium once the stack exists; related drainage/terrain work exists | low; adjacent to prior drainage-chain hypotheses, do not treat as a new lane without proof |
| 5 | H81-E — Sentinel-1 InSAR deformation linked to geothermal fault pathways | low-to-medium for the full fault target; potentially useful in active areas | very high; free account, EULA, scene search, processing, and coverage required | medium; no matching implementation identified in this local checkout, but global registry scan absent |

## H81-A — chemistry-conditioned hydrothermal conduit residuals (rank 1)

- **Layers/data:** INGENIOUS 2 m temperature probes and the well/spring temperature-and-chemistry tables, intersected with the competition's allowed study-area grid. Do not use public fault geometry or held-out catalogue segments as an input to the geochemical surface.
- **Physical signature:** spatially coherent residuals in geothermometer temperature and hydrothermal-fluid chemistry (e.g., silica/major-ion patterns), evaluated as plume/corridor geometry around candidate structural relays rather than simple nearest-spring distance. This is a hypothesis; no feature has been computed here.
- **Why it might find an unlisted fault:** the USGS Great Basin play-fairway report describes a blind-system case where shallow temperature, low resistivity, structural setting, and water-well geothermometry jointly supported an otherwise blind system. Hydrothermal discharge/chemistry can therefore reveal fluid pathways even where no surface fault trace was catalogued.
- **Difference from known work:** temperature probes and hydrothermal proximity are present in prior project narratives; the proposed discriminant is the *chemistry-conditioned spatial residual*, not just temperature or a mapped spring/conduit distance. This distinction still needs a full registry scan and a frozen preregistration.
- **Named non-fault mimic:** mixing of shallow groundwater with different source lithologies, seasonal recharge, sample-density bias, and anthropogenic pumping.
- **Official source and access check:** the [DOE Geothermal Data Repository INGENIOUS dataset](https://gdr.openei.org/submissions/1391) is marked publicly accessible under CC BY 4.0 and lists both `2m Temperature Probes.zip` and `Well and Spring Temperature and Chemistry.zip` (the latter is listed at about 19.85 MB). The landing page and download links were inspected; the data bytes were **not** downloaded in this sandbox, so actual file/hash/coverage validation remains blocked. The official [USGS blind-systems project summary](https://www.usgs.gov/publications/discovering-blind-geothermal-systems-great-basin-region-integrated-geologic-and) supports the multi-parameter mechanism, not the predictive value of this proposed feature.
- **Decision:** top *research* candidate only. Not viable to test now; no lane, input files, stack, or holdout are available.

## H81-B — alteration-mineral boundary corridors (rank 2)

- **Layers/data:** hydrothermal silica-rich, argillic, propylitic, and phyllic polygons from [USGS Open-File Report 2013–1139](https://pubs.usgs.gov/publication/ofr20131139), with competition-grid topography/geophysics only for independent structural context.
- **Physical signature:** thin, linear boundaries or intersections in alteration-mineral units; use them as a fluid-pathway prior, not as fault labels. The report maps potential hydrothermal silica-rich, propylitic, argillic, and phyllic rocks from ASTER data.
- **Why it might find an unlisted fault:** blind systems may preserve older hydrothermal deposits or alteration near fluid pathways even when a fault has no obvious present-day scarp.
- **Difference from known work:** external mapped mineralogical alteration classes are not the same as the provided radiometric/MT layers or terrain edges. Whether any prior family project already used this exact product is unknown and must be checked.
- **Named non-fault mimic:** non-geothermal ore-related hydrothermal alteration, primary lithology, mining, and ancient alteration no longer connected to an active fault.
- **Official source and access check:** USGS's report page and USGS MRData spatial-data page were inspected. The report describes the central and southern Basin and Range; MRData lists a full 587 MB download and per-class shapefile downloads. The link exists, but the GeoDAWN footprint's actual overlap with the mapped coverage has **not** been checked, and the data bytes were not downloaded. Therefore this is not yet a viable candidate for this AOI.

## H81-C — multi-date Landsat surface-temperature residual lineaments (rank 3)

- **Layers/data:** USGS Landsat Collection 2 Level-2 Surface Temperature (ST), combined with surface reflectance/quality masks and competition-grid elevation/land-cover controls.
- **Physical signature:** a repeatable, locally anomalous surface-temperature residual after controlling for acquisition date, elevation, slope/aspect, emissivity/cover, and cloud/quality flags; only coherent elongated residuals are considered.
- **Why it might find an unlisted fault:** geothermal heat transfer can create a surface thermal anomaly above a blind or concealed fluid pathway, even without a mapped surface scarp. A temperature anomaly is evidence of possible heat flow, not proof of a fault.
- **Difference from known work:** prior project narratives include shallow temperature or thermal-population ideas; this proposal uses multi-date satellite ST residuals and terrain/cover controls. Novelty is uncertain pending registry scan.
- **Named non-fault mimic:** illumination/aspect, emissivity differences, water/vegetation, wildfire, mining, roads, and irrigated land.
- **Official source and access check:** the [USGS Landsat Collection 2 Surface Temperature page](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature) says the products are global, available for Landsat 8/9 from 2013/2022 onward, downloadable from EarthExplorer, and have no use restrictions; the [Surface Reflectance page](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-reflectance) describes Level-2 surface reflectance. No specific scene search, cloud audit, or external download was performed. This is source-level availability, not confirmed usable coverage of every target pixel.

## H81-D — channel-profile knickzone and basin-response graph (rank 4)

- **Layers/data:** provided detrended elevation and detrended-elevation slope, plus geodetic shear/dilation layers if present in the cached stack.
- **Physical signature:** stream longitudinal-profile convexities/knickzones and upstream/downstream asymmetry that repeat across tributaries along a consistent structural corridor. This must be a profile-based process model, not a generic valley-chain or ridge detector.
- **Why it might find an unlisted fault:** blind displacement or differential uplift can perturb channel profiles and drainage organization without a preserved, catalogue-visible scarp.
- **Difference from known work:** earlier project material includes valley-chain/lineament work. A profile-response graph could be distinct, but the family resemblance is substantial; registry uniqueness and a method-level review must clear it before testing.
- **Named non-fault mimic:** resistant lithologic contacts, drainage capture, basin base-level change, roads/dams, and differential erosion.
- **External source:** none beyond the official competition-provided raster stack. The stack is absent here; no feature has been computed.

## H81-E — InSAR deformation coupled to geothermal fault pathways (rank 5)

- **Layers/data:** Sentinel-1 interferometric products from NASA's Alaska Satellite Facility (ASF DAAC), with the competition grid as the target.
- **Physical signature:** persistent line-of-sight deformation gradients or localized subsidence/uplift near geothermal prospects, tested as evidence for active fluid pathways rather than a generic fault lineament.
- **Why it might find an unlisted fault:** active fluid movement or reservoir pressure changes can reveal a permeable fault system not represented in a static surface-fault catalogue.
- **Difference from known work:** time-dependent radar deformation is distinct from static terrain, geophysics, or shallow chemistry. It will miss inactive faults and should not be used as a universal fault detector.
- **Named non-fault mimic:** groundwater extraction, mining, seasonal hydrology, earthquake deformation, atmospheric phase delay, and decorrelation.
- **Official source and access check:** [ASF DAAC Sentinel-1](https://asf.alaska.edu/data-sets/sar-data-sets/sentinel-1/sentinel-1-data-and-imagery/) states Sentinel-1 data are available through ASF tools and that ASF downloads require a free NASA Earthdata Login and agreement to its EULA. The source is public/free, but no local account exists here and no AOI scene pair, tasking, or data download was checked; this is blocked, not viable now.

## Required next step

Do not implement or create a TIFF from this shortlist in the current checkout. First resolve the missing lane assignment, obtain the shared template and its pinned tools, restore the authorized data/cache/registry, then preregister the selected hypothesis and run its individual-feature leakage canary and buffered-segment holdout. If the selected candidate does not beat the frozen holdout best with the required CI and pass the duplicate check, keep the negative result and do not spend a submission slot.

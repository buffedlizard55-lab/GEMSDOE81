# Ranked candidate hypotheses — session 2026-10-21 (lane: radiometric-discordance gate)

Generated BEFORE implementation, per protocol. The single lane for this session is
**H1**; the others are recorded so the lane choice is auditable and not silently widened.

| Rank | Hypothesis | Layers (exact) | Physical signature | Why it should catch a fault missing from USGS/INGENIOUS catalogue | Differs from repo (ASB shipped, verdict negative) | Expected DTI effect / cost |
|---|---|---|---|---|---|---|
| 1 | **RAD-ASB: radiometric-ratio discordance gate on the ASB coincidence surface** | `geodawn_extensions_u8.tif` bands 1–3 (ThK, UK, UTh contractor ratio grids, USGS GeoDAWN DOI 10.5066/P93LGLVQ) × ASB surface (`lidar_scarp_features_u8` bands 4/5/3 × `training_features.tif` bands 15/17) | Geometric mean of within-footprint ranks of gradient-magnitude of ThK, UK, UTh (= ratio-discordance edge `R`); final `F = sqrt(rank(ASB) · rank(R))` | A blind fault is a fluid conduit: hydrothermal fluid leaches/redistributes K, U, Th differently, so a *ratio* edge can cross a fault with no mapped trace and no scarp; catalogued faults were mapped mainly from topography/geology, not ratio discordance | ASB used no radiometric layer at all; registry rank-2 idea "Th/K discordance" was listed NOT TESTED because the 3-experiment budget was spent. Not H33 orientation consensus, not catalogue-flank pruning | Medium expected gain if alteration edges are real (gate removes ASB dots on terrace/pinch-out mimics that lack alteration); low cost (bands already restored, hash-verified) |
| 2 | Magnetic-fabric truncation gate (add TMI_up150 gradient) | `geodawn_extensions_u8.tif` band 4 (TMI upward-continued 150 m) gradient rank, as third geometric-mean factor | Long straight magnetic gradient ridge coincident with ASB+RAD | Fault juxtaposition terminates magnetic fabric across a buried fault | Partially overlaps ASB component B (conductivity/basement gradient); risk of diluting with a smooth 150 m-continued field | Lower expected gain, low cost — tested only as E1 variant `F3`, not shipped unless it wins holdout |
| 3 | Cross-strike profile displacement | `training_features.tif` bands 2 (rtp), 13 (iso_grav_anom), 17 (cond_surf); normalised cross-correlation shift of adjacent parallel profiles | Consistent signed lateral displacement over several windows | Buried displacement survives scarp erosion | Not implemented anywhere in this repo; medium–high implementation cost, seam mimics | Deferred (not in lane; >1 new transform) |
| 4 | Supervised HGB/U-Net on cached stack + DTI-optimal dotted emission | All 19 `training_features` bands + lidar/rad u8 stacks | Learned P(fault) surface, Poisson/greedy dotted emission, 2 px catalogue prune (winner's lesson) | Learns multi-layer combinations mappers under-weighted | Family ML attempts scored 0.018–0.043 live (organizer-reported in prompt ledger) when emitted densely; dotted emission might rescue, but leakage canary + spatial-CV burden is high and 3 GB RAM limits training | Deferred: high cost, family evidence poor |
| 5 | Sub-km seismicity lineaments | USGS ComCat FDSN raw events (free official: https://earthquake.usgs.gov/fdsnws/event/1/) | Epicentre collinearity + nodal-plane strike coherence | Actively straining blind faults need no scarp | No repo surface uses raw events; source is obtainable (FDSN verified as official route in prior registry) but not fetched/checked for AOI density this session | Not viable this session without AOI event-density check |

**Named non-fault mimic for H1:** a lithologic contact / paleo-shoreline where a
sedimentary pinch-out produces both an antithetic terrace pair *and* a radiometric
ratio edge (different bedrock radioelement ratios across the contact) with no fault.
The holdout (hide-and-recover whole fault components) is the arbiter, not the story.

**Decision rule (preregistered):** ship only the E1/E2 holdout winner; if it does not
beat the same-instrument d28 control HOLDOUT-DTI measured in the same run, the run-card
verdict is `negative` even though the TIF is format-valid and downloadable.
No score above 0.2778 is claimed for any raster here; live scores are UNSCORED until
an organizer receipt exists.

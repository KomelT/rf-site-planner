# RF Site Planner – RSSI analysis

- Generated: 2026-01-08 17:55:44

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 119 | 0 | 46 | 119 | 17.646 | 21.453 | 17.642 | 35.674 | 14.3% | 0.409 |
| !7369fb6a | 134 | 0 | 31 | 134 | 28.109 | 30.914 | 28.109 | 46.708 | 0.0% | 0.510 |
| !da5ad56c | 123 | 0 | 42 | 123 | 21.370 | 25.342 | 21.362 | 42.604 | 12.2% | 0.482 |

## Gateway: `!75f19024`

- Completed requests: **119**
- Failed requests: **0**
- Skipped rows (missing RSSI): **46**
- Number of samples (N): **119**
- Pearson correlation (path loss vs measured): **0.409**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 38 | 31.9% |
| Line of sight obstructed | 58 | 48.7% |
| 60% of first Fresnel zone obstructed | 13 | 10.9% |
| First Fresnel zone obstructed | 10 | 8.4% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 119 | 38 | 58 | 13 | 10 |
| Average error / bias (mean of path loss − measured) [dB] | 17.642 | 15.078 | 18.325 | 23.295 | 16.072 |
| Standard deviation of error [dB] | 12.258 | 8.050 | 14.801 | 11.706 | 7.334 |
| Mean absolute error [dB] | 17.646 | 15.078 | 18.334 | 23.295 | 16.072 |
| Root mean square error [dB] | 21.453 | 17.042 | 23.476 | 25.868 | 17.513 |
| Median error [dB] | 13.390 | 14.215 | 11.725 | 21.520 | 16.505 |
| Median absolute deviation (robust spread) [dB] | 5.760 | 6.080 | 4.280 | 8.130 | 3.370 |
| 90th percentile of absolute error [dB] | 35.674 | 24.596 | 44.124 | 35.792 | 21.491 |
| 95th percentile of absolute error [dB] | 44.969 | 28.214 | 45.959 | 41.768 | 25.725 |
| Minimum error [dB] | -0.260 | 1.800 | -0.260 | 7.660 | 4.810 |
| Maximum error [dB] | 54.510 | 34.540 | 54.510 | 49.250 | 29.960 |
| Share within ±3 dB | 6.7% | 5.3% | 10.3% | 0.0% | 0.0% |
| Share within ±6 dB | 14.3% | 15.8% | 15.5% | 0.0% | 20.0% |
| Share within ±10 dB | 22.7% | 28.9% | 22.4% | 7.7% | 20.0% |

## Gateway: `!7369fb6a`

- Completed requests: **134**
- Failed requests: **0**
- Skipped rows (missing RSSI): **31**
- Number of samples (N): **134**
- Pearson correlation (path loss vs measured): **0.510**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 11.9% |
| Line of sight obstructed | 68 | 50.7% |
| 60% of first Fresnel zone obstructed | 28 | 20.9% |
| First Fresnel zone obstructed | 22 | 16.4% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 134 | 16 | 68 | 28 | 22 |
| Average error / bias (mean of path loss − measured) [dB] | 28.109 | 27.639 | 28.830 | 26.809 | 27.875 |
| Standard deviation of error [dB] | 12.915 | 11.000 | 14.893 | 11.567 | 9.279 |
| Mean absolute error [dB] | 28.109 | 27.639 | 28.830 | 26.809 | 27.875 |
| Root mean square error [dB] | 30.914 | 29.620 | 32.399 | 29.116 | 29.312 |
| Median error [dB] | 24.370 | 25.160 | 22.820 | 26.820 | 26.930 |
| Median absolute deviation (robust spread) [dB] | 8.385 | 7.745 | 7.690 | 9.230 | 6.210 |
| 90th percentile of absolute error [dB] | 46.708 | 42.770 | 50.205 | 39.182 | 40.441 |
| 95th percentile of absolute error [dB] | 52.242 | 43.973 | 58.088 | 43.754 | 41.415 |
| Minimum error [dB] | 8.310 | 10.510 | 10.350 | 9.190 | 8.310 |
| Maximum error [dB] | 66.470 | 47.460 | 66.470 | 58.250 | 45.600 |
| Share within ±3 dB | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Share within ±6 dB | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Share within ±10 dB | 1.5% | 0.0% | 0.0% | 3.6% | 4.5% |

## Gateway: `!da5ad56c`

- Completed requests: **123**
- Failed requests: **0**
- Skipped rows (missing RSSI): **42**
- Number of samples (N): **123**
- Pearson correlation (path loss vs measured): **0.482**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 14 | 11.4% |
| Line of sight obstructed | 77 | 62.6% |
| 60% of first Fresnel zone obstructed | 19 | 15.4% |
| First Fresnel zone obstructed | 13 | 10.6% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 123 | 14 | 77 | 19 | 13 |
| Average error / bias (mean of path loss − measured) [dB] | 21.362 | 10.944 | 24.387 | 22.086 | 13.605 |
| Standard deviation of error [dB] | 13.690 | 6.134 | 15.187 | 8.592 | 6.455 |
| Mean absolute error [dB] | 21.370 | 10.965 | 24.396 | 22.086 | 13.605 |
| Root mean square error [dB] | 25.342 | 12.438 | 28.677 | 23.617 | 14.952 |
| Median error [dB] | 18.970 | 12.615 | 20.690 | 24.370 | 10.970 |
| Median absolute deviation (robust spread) [dB] | 7.740 | 1.815 | 9.710 | 3.970 | 7.440 |
| 90th percentile of absolute error [dB] | 42.604 | 14.264 | 46.466 | 31.734 | 21.506 |
| 95th percentile of absolute error [dB] | 48.743 | 18.172 | 53.516 | 32.842 | 22.272 |
| Minimum error [dB] | -0.330 | -0.150 | -0.330 | 3.170 | 3.310 |
| Maximum error [dB] | 56.780 | 25.140 | 56.780 | 33.310 | 22.470 |
| Share within ±3 dB | 6.5% | 14.3% | 7.8% | 0.0% | 0.0% |
| Share within ±6 dB | 12.2% | 21.4% | 10.4% | 10.5% | 15.4% |
| Share within ±10 dB | 16.3% | 35.7% | 14.3% | 10.5% | 15.4% |


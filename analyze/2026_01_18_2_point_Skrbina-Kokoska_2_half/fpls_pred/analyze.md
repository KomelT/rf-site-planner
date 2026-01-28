# RF Site Planner – RSSI analysis

- Generated: 2026-01-28 12:43:42

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 155 | 0 | 33 | 155 | 15.419 | 15.994 | 19.671 | 11.524 | 32.854 | 27.7% | 0.471 |
| !7369fb6a | 182 | 0 | 6 | 182 | 27.751 | 9.450 | 29.139 | 27.573 | 36.802 | 0.0% | 0.839 |

## Gateway: `!75f19024`

- Completed requests: **155**
- Failed requests: **0**
- Skipped rows (missing RSSI): **33**
- Number of samples (N): **155**
- Pearson correlation (path loss vs measured): **0.471**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 25 | 16.1% |
| Line of sight obstructed | 81 | 52.3% |
| 60% of first Fresnel zone obstructed | 33 | 21.3% |
| First Fresnel zone obstructed | 16 | 10.3% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 155 | 25 | 81 | 33 | 16 |
| Average error / bias (mean of path loss − measured) [dB] | 11.524 | 8.413 | 12.045 | 9.503 | 17.916 |
| Standard deviation of error [dB] | 15.994 | 8.634 | 17.857 | 16.267 | 13.099 |
| Mean absolute error [dB] | 15.419 | 10.349 | 16.310 | 14.675 | 20.362 |
| Root mean square error [dB] | 19.671 | 11.930 | 21.448 | 18.626 | 21.951 |
| Median error [dB] | 9.280 | 9.210 | 8.070 | -0.410 | 22.890 |
| Median absolute deviation (robust spread) [dB] | 13.480 | 4.250 | 15.060 | 10.580 | 4.530 |
| 90th percentile of absolute error [dB] | 32.854 | 15.000 | 35.780 | 30.902 | 27.905 |
| 95th percentile of absolute error [dB] | 36.014 | 18.896 | 38.190 | 32.796 | 28.655 |
| Minimum error [dB] | -12.230 | -12.230 | -12.230 | -11.990 | -12.010 |
| Maximum error [dB] | 52.230 | 28.800 | 52.230 | 34.880 | 30.770 |
| Share within ±3 dB | 14.2% | 8.0% | 13.6% | 24.2% | 6.2% |
| Share within ±6 dB | 27.7% | 24.0% | 30.9% | 33.3% | 6.2% |
| Share within ±10 dB | 43.2% | 52.0% | 46.9% | 42.4% | 12.5% |

## Gateway: `!7369fb6a`

- Completed requests: **182**
- Failed requests: **0**
- Skipped rows (missing RSSI): **6**
- Number of samples (N): **182**
- Pearson correlation (path loss vs measured): **0.839**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 8.8% |
| Line of sight obstructed | 70 | 38.5% |
| 60% of first Fresnel zone obstructed | 77 | 42.3% |
| First Fresnel zone obstructed | 19 | 10.4% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 182 | 16 | 70 | 77 | 19 |
| Average error / bias (mean of path loss − measured) [dB] | 27.573 | 25.287 | 31.724 | 25.534 | 22.468 |
| Standard deviation of error [dB] | 9.450 | 8.306 | 9.941 | 7.323 | 10.879 |
| Mean absolute error [dB] | 27.751 | 25.287 | 31.986 | 25.534 | 23.207 |
| Root mean square error [dB] | 29.139 | 26.536 | 33.224 | 26.550 | 24.838 |
| Median error [dB] | 28.920 | 26.950 | 31.975 | 26.100 | 26.180 |
| Median absolute deviation (robust spread) [dB] | 4.315 | 6.415 | 3.455 | 5.490 | 6.040 |
| 90th percentile of absolute error [dB] | 36.802 | 34.130 | 39.175 | 33.632 | 33.062 |
| 95th percentile of absolute error [dB] | 38.460 | 34.890 | 41.633 | 35.658 | 36.513 |
| Minimum error [dB] | -9.140 | 8.130 | -9.140 | 8.990 | -7.020 |
| Maximum error [dB] | 80.540 | 36.810 | 80.540 | 39.930 | 37.260 |
| Share within ±3 dB | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Share within ±6 dB | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Share within ±10 dB | 2.7% | 6.2% | 1.4% | 2.6% | 5.3% |


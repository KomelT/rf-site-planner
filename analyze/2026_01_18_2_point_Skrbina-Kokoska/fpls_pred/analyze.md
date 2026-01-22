# RF Site Planner – RSSI analysis

- Generated: 2026-01-22 12:57:04

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 358 | 0 | 78 | 358 | 15.218 | 16.984 | 18.215 | 6.642 | 29.931 | 19.8% | 0.437 |
| !7369fb6a | 429 | 0 | 7 | 429 | 22.817 | 9.943 | 24.418 | 22.307 | 31.616 | 1.4% | 0.784 |

## Gateway: `!75f19024`

- Completed requests: **358**
- Failed requests: **0**
- Skipped rows (missing RSSI): **78**
- Number of samples (N): **358**
- Pearson correlation (path loss vs measured): **0.437**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 51 | 14.2% |
| Line of sight obstructed | 181 | 50.6% |
| 60% of first Fresnel zone obstructed | 80 | 22.3% |
| First Fresnel zone obstructed | 46 | 12.8% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 358 | 51 | 181 | 80 | 46 |
| Average error / bias (mean of path loss − measured) [dB] | 6.642 | 8.026 | 6.746 | 4.053 | 9.202 |
| Standard deviation of error [dB] | 16.984 | 9.765 | 18.253 | 17.411 | 17.229 |
| Mean absolute error [dB] | 15.218 | 10.009 | 15.830 | 15.542 | 18.017 |
| Root mean square error [dB] | 18.215 | 12.566 | 19.413 | 17.770 | 19.366 |
| Median error [dB] | 4.040 | 6.140 | 1.800 | -4.420 | 15.965 |
| Median absolute deviation (robust spread) [dB] | 14.945 | 5.320 | 13.790 | 11.580 | 9.815 |
| 90th percentile of absolute error [dB] | 29.931 | 19.960 | 31.560 | 28.264 | 26.895 |
| 95th percentile of absolute error [dB] | 31.775 | 24.785 | 34.260 | 30.586 | 29.867 |
| Minimum error [dB] | -17.980 | -17.230 | -17.230 | -17.980 | -17.010 |
| Maximum error [dB] | 47.230 | 25.820 | 47.230 | 33.560 | 35.560 |
| Share within ±3 dB | 8.7% | 17.6% | 9.9% | 3.8% | 2.2% |
| Share within ±6 dB | 19.8% | 41.2% | 19.9% | 15.0% | 4.3% |
| Share within ±10 dB | 38.8% | 60.8% | 43.1% | 31.2% | 10.9% |

## Gateway: `!7369fb6a`

- Completed requests: **429**
- Failed requests: **0**
- Skipped rows (missing RSSI): **7**
- Number of samples (N): **429**
- Pearson correlation (path loss vs measured): **0.784**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 33 | 7.7% |
| Line of sight obstructed | 190 | 44.3% |
| 60% of first Fresnel zone obstructed | 163 | 38.0% |
| First Fresnel zone obstructed | 43 | 10.0% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 429 | 33 | 190 | 163 | 43 |
| Average error / bias (mean of path loss − measured) [dB] | 22.307 | 16.705 | 26.376 | 20.080 | 17.073 |
| Standard deviation of error [dB] | 9.943 | 10.942 | 9.483 | 8.323 | 9.877 |
| Mean absolute error [dB] | 22.817 | 18.472 | 26.470 | 20.623 | 18.329 |
| Root mean square error [dB] | 24.418 | 19.879 | 28.020 | 21.727 | 19.667 |
| Median error [dB] | 23.240 | 19.270 | 26.865 | 21.400 | 19.820 |
| Median absolute deviation (robust spread) [dB] | 5.460 | 6.030 | 4.050 | 4.440 | 4.290 |
| 90th percentile of absolute error [dB] | 31.616 | 27.752 | 33.724 | 28.970 | 26.184 |
| 95th percentile of absolute error [dB] | 33.814 | 29.274 | 35.959 | 30.832 | 30.079 |
| Minimum error [dB] | -15.170 | -15.130 | -8.970 | -15.170 | -13.990 |
| Maximum error [dB] | 76.930 | 33.040 | 76.930 | 42.670 | 31.290 |
| Share within ±3 dB | 0.7% | 3.0% | 0.0% | 0.6% | 2.3% |
| Share within ±6 dB | 1.4% | 3.0% | 0.0% | 1.2% | 7.0% |
| Share within ±10 dB | 7.0% | 12.1% | 3.7% | 8.0% | 14.0% |


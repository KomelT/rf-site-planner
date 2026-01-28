# RF Site Planner – RSSI analysis

- Generated: 2026-01-28 17:24:17

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 157 | 0 | 33 | 157 | 15.187 | 16.032 | 19.481 | 11.141 | 32.796 | 28.7% | 0.461 |
| !7369fb6a | 183 | 0 | 6 | 183 | 27.835 | 9.448 | 29.219 | 27.658 | 36.794 | 0.0% | 0.840 |

## Gateway: `!75f19024`

- Completed requests: **157**
- Failed requests: **0**
- Skipped rows (missing RSSI): **33**
- Number of samples (N): **157**
- Pearson correlation (path loss vs measured): **0.461**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 25 | 15.9% |
| Line of sight obstructed | 83 | 52.9% |
| 60% of first Fresnel zone obstructed | 33 | 21.0% |
| First Fresnel zone obstructed | 16 | 10.2% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 157 | 25 | 83 | 33 | 16 |
| Average error / bias (mean of path loss − measured) [dB] | 11.141 | 8.413 | 11.656 | 9.503 | 16.104 |
| Standard deviation of error [dB] | 16.032 | 8.634 | 17.835 | 16.267 | 14.298 |
| Mean absolute error [dB] | 15.187 | 10.349 | 16.056 | 14.675 | 19.297 |
| Root mean square error [dB] | 19.481 | 11.930 | 21.216 | 18.626 | 21.236 |
| Median error [dB] | 9.110 | 9.210 | 6.930 | -0.410 | 22.360 |
| Median absolute deviation (robust spread) [dB] | 13.530 | 4.250 | 13.920 | 10.580 | 5.545 |
| 90th percentile of absolute error [dB] | 32.796 | 15.000 | 35.634 | 30.902 | 27.905 |
| 95th percentile of absolute error [dB] | 35.936 | 18.896 | 38.175 | 32.796 | 28.655 |
| Minimum error [dB] | -12.230 | -12.230 | -12.230 | -11.990 | -12.010 |
| Maximum error [dB] | 52.230 | 28.800 | 52.230 | 34.880 | 30.770 |
| Share within ±3 dB | 14.6% | 8.0% | 14.5% | 24.2% | 6.2% |
| Share within ±6 dB | 28.7% | 24.0% | 31.3% | 33.3% | 12.5% |
| Share within ±10 dB | 44.6% | 52.0% | 48.2% | 42.4% | 18.8% |

## Gateway: `!7369fb6a`

- Completed requests: **183**
- Failed requests: **0**
- Skipped rows (missing RSSI): **6**
- Number of samples (N): **183**
- Pearson correlation (path loss vs measured): **0.840**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 8.7% |
| Line of sight obstructed | 71 | 38.8% |
| 60% of first Fresnel zone obstructed | 78 | 42.6% |
| First Fresnel zone obstructed | 18 | 9.8% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 183 | 16 | 71 | 78 | 18 |
| Average error / bias (mean of path loss − measured) [dB] | 27.658 | 25.287 | 31.762 | 25.642 | 22.318 |
| Standard deviation of error [dB] | 9.448 | 8.306 | 9.876 | 7.338 | 11.174 |
| Mean absolute error [dB] | 27.835 | 25.287 | 32.019 | 25.642 | 23.098 |
| Root mean square error [dB] | 29.219 | 26.536 | 33.241 | 26.658 | 24.820 |
| Median error [dB] | 29.190 | 26.950 | 31.990 | 26.235 | 26.495 |
| Median absolute deviation (robust spread) [dB] | 4.370 | 6.415 | 3.380 | 5.375 | 6.435 |
| 90th percentile of absolute error [dB] | 36.794 | 34.130 | 39.030 | 34.210 | 33.483 |
| 95th percentile of absolute error [dB] | 38.441 | 34.890 | 41.620 | 35.556 | 36.555 |
| Minimum error [dB] | -9.140 | 8.130 | -9.140 | 8.990 | -7.020 |
| Maximum error [dB] | 80.540 | 36.810 | 80.540 | 39.930 | 37.260 |
| Share within ±3 dB | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Share within ±6 dB | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Share within ±10 dB | 2.7% | 6.2% | 1.4% | 2.6% | 5.6% |


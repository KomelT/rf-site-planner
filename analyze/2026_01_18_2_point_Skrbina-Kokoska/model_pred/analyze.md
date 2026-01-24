# RF Site Planner – RSSI analysis

- Generated: 2026-01-24 10:49:48

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 361 | 0 | 78 | 361 | 32.402 | 24.787 | 39.589 | 30.897 | 65.590 | 15.5% | 0.322 |
| !7369fb6a | 427 | 0 | 7 | 427 | 14.314 | 18.747 | 19.893 | 6.718 | 37.026 | 33.3% | 0.676 |

## Gateway: `!75f19024`

- Completed requests: **361**
- Failed requests: **0**
- Skipped rows (missing RSSI): **78**
- Number of samples (N): **361**
- Pearson correlation (predicted vs measured): **0.322**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 53 | 14.7% |
| Line of sight obstructed | 183 | 50.7% |
| 60% of first Fresnel zone obstructed | 78 | 21.6% |
| First Fresnel zone obstructed | 47 | 13.0% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 361 | 53 | 183 | 78 | 47 |
| Average error / bias (mean of predicted − measured) [dB] | 30.897 | 13.330 | 46.706 | 17.031 | 12.163 |
| Standard deviation of error [dB] | 24.787 | 10.009 | 21.711 | 17.198 | 17.344 |
| Mean absolute error [dB] | 32.402 | 14.131 | 47.235 | 20.155 | 15.573 |
| Root mean square error [dB] | 39.589 | 16.612 | 51.480 | 24.125 | 21.032 |
| Median error [dB] | 30.340 | 14.680 | 50.580 | 27.115 | 5.600 |
| Median absolute deviation (robust spread) [dB] | 19.950 | 5.530 | 15.010 | 9.455 | 10.820 |
| 90th percentile of absolute error [dB] | 65.590 | 24.822 | 68.374 | 36.553 | 36.774 |
| 95th percentile of absolute error [dB] | 68.500 | 29.238 | 78.782 | 37.560 | 36.780 |
| Minimum error [dB] | -14.970 | -5.260 | -14.510 | -12.970 | -14.970 |
| Maximum error [dB] | 104.360 | 37.800 | 104.360 | 38.560 | 37.580 |
| Share within ±3 dB | 8.6% | 13.2% | 1.6% | 12.8% | 23.4% |
| Share within ±6 dB | 15.5% | 24.5% | 2.7% | 24.4% | 40.4% |
| Share within ±10 dB | 21.9% | 32.1% | 4.9% | 35.9% | 53.2% |

## Gateway: `!7369fb6a`

- Completed requests: **427**
- Failed requests: **0**
- Skipped rows (missing RSSI): **7**
- Number of samples (N): **427**
- Pearson correlation (predicted vs measured): **0.676**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 32 | 7.5% |
| Line of sight obstructed | 190 | 44.5% |
| 60% of first Fresnel zone obstructed | 161 | 37.7% |
| First Fresnel zone obstructed | 44 | 10.3% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 427 | 32 | 190 | 161 | 44 |
| Average error / bias (mean of predicted − measured) [dB] | 6.718 | -1.802 | 19.572 | -4.403 | -1.902 |
| Standard deviation of error [dB] | 18.747 | 12.379 | 19.547 | 8.473 | 10.069 |
| Mean absolute error [dB] | 14.314 | 9.585 | 22.130 | 7.734 | 8.082 |
| Root mean square error [dB] | 19.893 | 12.317 | 27.625 | 9.525 | 10.134 |
| Median error [dB] | 1.460 | -3.880 | 17.480 | -5.440 | -4.760 |
| Median absolute deviation (robust spread) [dB] | 9.660 | 6.695 | 14.450 | 4.790 | 4.400 |
| 90th percentile of absolute error [dB] | 37.026 | 19.751 | 46.487 | 13.790 | 15.099 |
| 95th percentile of absolute error [dB] | 45.462 | 28.167 | 50.113 | 16.780 | 15.691 |
| Minimum error [dB] | -62.860 | -27.010 | -62.860 | -22.770 | -15.720 |
| Maximum error [dB] | 68.380 | 30.690 | 68.380 | 30.730 | 29.540 |
| Share within ±3 dB | 13.8% | 18.8% | 10.0% | 17.4% | 13.6% |
| Share within ±6 dB | 33.3% | 37.5% | 21.1% | 42.9% | 47.7% |
| Share within ±10 dB | 55.3% | 68.8% | 34.2% | 72.7% | 72.7% |


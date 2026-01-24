# RF Site Planner – RSSI analysis

- Generated: 2026-01-24 10:49:49

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 361 | 0 | 78 | 361 | 14.938 | 16.964 | 17.010 | -1.536 | 24.880 | 18.8% | 0.436 |
| !7369fb6a | 427 | 0 | 7 | 427 | 22.893 | 9.941 | 24.485 | -22.381 | 31.682 | 1.4% | 0.786 |

## Gateway: `!75f19024`

- Completed requests: **361**
- Failed requests: **0**
- Skipped rows (missing RSSI): **78**
- Number of samples (N): **361**
- Pearson correlation (path loss vs measured): **0.436**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 53 | 14.7% |
| Line of sight obstructed | 183 | 50.7% |
| 60% of first Fresnel zone obstructed | 78 | 21.6% |
| First Fresnel zone obstructed | 47 | 13.0% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 361 | 53 | 183 | 78 | 47 |
| Average error / bias (mean of path loss − measured) [dB] | -1.536 | -2.562 | -1.544 | 0.531 | -3.773 |
| Standard deviation of error [dB] | 16.964 | 9.997 | 18.257 | 17.418 | 17.293 |
| Mean absolute error [dB] | 14.938 | 7.696 | 16.055 | 16.397 | 16.332 |
| Root mean square error [dB] | 17.010 | 10.228 | 18.273 | 17.314 | 17.519 |
| Median error [dB] | 1.000 | -1.030 | 3.600 | 8.785 | -9.970 |
| Median absolute deviation (robust spread) [dB] | 14.980 | 5.210 | 13.390 | 12.215 | 10.810 |
| 90th percentile of absolute error [dB] | 24.880 | 18.612 | 26.552 | 23.552 | 22.318 |
| 95th percentile of absolute error [dB] | 26.730 | 20.814 | 29.192 | 25.658 | 24.729 |
| Minimum error [dB] | -42.230 | -20.820 | -42.230 | -28.560 | -30.560 |
| Maximum error [dB] | 22.980 | 22.230 | 22.230 | 22.980 | 22.010 |
| Share within ±3 dB | 10.2% | 35.8% | 9.3% | 0.0% | 2.1% |
| Share within ±6 dB | 18.8% | 56.6% | 17.5% | 1.3% | 10.6% |
| Share within ±10 dB | 27.7% | 66.0% | 25.1% | 12.8% | 19.1% |

## Gateway: `!7369fb6a`

- Completed requests: **427**
- Failed requests: **0**
- Skipped rows (missing RSSI): **7**
- Number of samples (N): **427**
- Pearson correlation (path loss vs measured): **0.786**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 32 | 7.5% |
| Line of sight obstructed | 190 | 44.5% |
| 60% of first Fresnel zone obstructed | 161 | 37.7% |
| First Fresnel zone obstructed | 44 | 10.3% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 427 | 32 | 190 | 161 | 44 |
| Average error / bias (mean of path loss − measured) [dB] | -22.381 | -16.508 | -26.372 | -20.150 | -17.585 |
| Standard deviation of error [dB] | 9.941 | 11.058 | 9.485 | 8.309 | 10.019 |
| Mean absolute error [dB] | 22.893 | 18.330 | 26.466 | 20.699 | 18.813 |
| Root mean square error [dB] | 24.485 | 19.774 | 28.017 | 21.786 | 20.183 |
| Median error [dB] | -23.510 | -19.135 | -26.865 | -21.400 | -20.320 |
| Median absolute deviation (robust spread) [dB] | 5.410 | 6.110 | 4.050 | 4.380 | 4.290 |
| 90th percentile of absolute error [dB] | 31.682 | 27.881 | 33.724 | 28.930 | 26.710 |
| 95th percentile of absolute error [dB] | 33.843 | 29.402 | 35.959 | 30.850 | 30.761 |
| Minimum error [dB] | -76.930 | -33.040 | -76.930 | -42.670 | -31.290 |
| Maximum error [dB] | 15.170 | 15.130 | 8.970 | 15.170 | 13.990 |
| Share within ±3 dB | 0.7% | 3.1% | 0.0% | 0.6% | 2.3% |
| Share within ±6 dB | 1.4% | 3.1% | 0.0% | 1.2% | 6.8% |
| Share within ±10 dB | 7.0% | 12.5% | 3.7% | 8.1% | 13.6% |


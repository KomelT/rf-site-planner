# RF Site Planner – RSSI analysis

- Generated: 2026-01-28 12:42:53

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 205 | 0 | 45 | 205 | 31.199 | 26.148 | 37.522 | -26.973 | 58.530 | 8.8% | 0.291 |
| !7369fb6a | 245 | 0 | 1 | 245 | 16.599 | 19.826 | 20.937 | -6.846 | 36.632 | 23.7% | 0.632 |

## Gateway: `!75f19024`

- Completed requests: **205**
- Failed requests: **0**
- Skipped rows (missing RSSI): **45**
- Number of samples (N): **205**
- Pearson correlation (predicted vs measured): **0.291**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 7.8% |
| Line of sight obstructed | 133 | 64.9% |
| 60% of first Fresnel zone obstructed | 37 | 18.0% |
| First Fresnel zone obstructed | 19 | 9.3% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 205 | 16 | 133 | 37 | 19 |
| Average error / bias (mean of predicted − measured) [dB] | -26.973 | -0.030 | -39.244 | -7.641 | -1.412 |
| Standard deviation of error [dB] | 26.148 | 8.838 | 21.892 | 19.772 | 13.091 |
| Mean absolute error [dB] | 31.199 | 7.898 | 40.141 | 19.735 | 10.548 |
| Root mean square error [dB] | 37.522 | 8.557 | 44.897 | 20.946 | 12.820 |
| Median error [dB] | -26.960 | -3.815 | -43.620 | -17.640 | 2.470 |
| Median absolute deviation (robust spread) [dB] | 22.140 | 5.735 | 14.400 | 10.120 | 7.290 |
| 90th percentile of absolute error [dB] | 58.530 | 12.650 | 59.750 | 27.738 | 21.964 |
| 95th percentile of absolute error [dB] | 61.146 | 15.062 | 68.388 | 27.800 | 23.657 |
| Minimum error [dB] | -95.840 | -10.240 | -95.840 | -28.750 | -25.790 |
| Maximum error [dB] | 24.780 | 15.070 | 23.710 | 24.780 | 13.220 |
| Share within ±3 dB | 4.9% | 0.0% | 4.5% | 2.7% | 15.8% |
| Share within ±6 dB | 8.8% | 25.0% | 6.0% | 2.7% | 26.3% |
| Share within ±10 dB | 20.0% | 81.2% | 9.8% | 8.1% | 63.2% |

## Gateway: `!7369fb6a`

- Completed requests: **245**
- Failed requests: **0**
- Skipped rows (missing RSSI): **1**
- Number of samples (N): **245**
- Pearson correlation (predicted vs measured): **0.632**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 13 | 5.3% |
| Line of sight obstructed | 145 | 59.2% |
| 60% of first Fresnel zone obstructed | 81 | 33.1% |
| First Fresnel zone obstructed | 6 | 2.4% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 245 | 13 | 145 | 81 | 6 |
| Average error / bias (mean of predicted − measured) [dB] | -6.846 | 3.891 | -17.555 | 9.923 | 2.292 |
| Standard deviation of error [dB] | 19.826 | 14.303 | 17.853 | 8.103 | 13.435 |
| Mean absolute error [dB] | 16.599 | 11.865 | 20.151 | 11.476 | 10.202 |
| Root mean square error [dB] | 20.937 | 14.282 | 24.994 | 12.780 | 12.477 |
| Median error [dB] | -1.920 | 7.340 | -17.310 | 11.080 | 5.090 |
| Median absolute deviation (robust spread) [dB] | 14.170 | 5.900 | 13.600 | 3.820 | 4.750 |
| 90th percentile of absolute error [dB] | 36.632 | 23.654 | 40.044 | 19.230 | 18.015 |
| 95th percentile of absolute error [dB] | 40.628 | 24.208 | 42.738 | 21.080 | 20.873 |
| Minimum error [dB] | -68.170 | -24.880 | -68.170 | -24.920 | -23.730 |
| Maximum error [dB] | 64.410 | 23.230 | 64.410 | 22.850 | 12.300 |
| Share within ±3 dB | 11.0% | 7.7% | 13.1% | 6.2% | 33.3% |
| Share within ±6 dB | 23.7% | 30.8% | 24.1% | 21.0% | 33.3% |
| Share within ±10 dB | 36.3% | 46.2% | 33.8% | 38.3% | 50.0% |


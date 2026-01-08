# RF Site Planner – RSSI analysis

- Generated: 2026-01-08 17:55:43

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 119 | 0 | 46 | 119 | 18.321 | 22.042 | 6.208 | 33.232 | 11.8% | 0.328 |
| !7369fb6a | 134 | 0 | 31 | 134 | 23.004 | 25.910 | 13.984 | 38.619 | 11.9% | 0.343 |
| !da5ad56c | 123 | 0 | 42 | 123 | 16.495 | 19.870 | 5.075 | 30.172 | 16.3% | 0.512 |

## Gateway: `!75f19024`

- Completed requests: **119**
- Failed requests: **0**
- Skipped rows (missing RSSI): **46**
- Number of samples (N): **119**
- Pearson correlation (predicted vs measured): **0.328**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 38 | 31.9% |
| Line of sight obstructed | 58 | 48.7% |
| 60% of first Fresnel zone obstructed | 13 | 10.9% |
| First Fresnel zone obstructed | 10 | 8.4% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 119 | 38 | 58 | 13 | 10 |
| Average error / bias (mean of predicted − measured) [dB] | 6.208 | 19.743 | -9.276 | 25.302 | 19.753 |
| Standard deviation of error [dB] | 21.240 | 7.980 | 19.406 | 11.175 | 7.231 |
| Mean absolute error [dB] | 18.321 | 19.743 | 15.577 | 25.302 | 19.753 |
| Root mean square error [dB] | 22.042 | 21.256 | 21.358 | 27.486 | 20.910 |
| Median error [dB] | 9.650 | 19.250 | -7.215 | 22.350 | 19.935 |
| Median absolute deviation (robust spread) [dB] | 12.860 | 6.080 | 10.575 | 8.370 | 3.965 |
| 90th percentile of absolute error [dB] | 33.232 | 29.119 | 37.206 | 39.776 | 25.385 |
| 95th percentile of absolute error [dB] | 41.655 | 33.027 | 53.911 | 43.544 | 29.232 |
| Minimum error [dB] | -60.020 | 6.450 | -60.020 | 8.930 | 9.180 |
| Maximum error [dB] | 46.970 | 38.950 | 22.510 | 46.970 | 33.080 |
| Share within ±3 dB | 5.9% | 0.0% | 12.1% | 0.0% | 0.0% |
| Share within ±6 dB | 11.8% | 0.0% | 24.1% | 0.0% | 0.0% |
| Share within ±10 dB | 30.3% | 15.8% | 46.6% | 7.7% | 20.0% |

## Gateway: `!7369fb6a`

- Completed requests: **134**
- Failed requests: **0**
- Skipped rows (missing RSSI): **31**
- Number of samples (N): **134**
- Pearson correlation (predicted vs measured): **0.343**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 11.9% |
| Line of sight obstructed | 68 | 50.7% |
| 60% of first Fresnel zone obstructed | 28 | 20.9% |
| First Fresnel zone obstructed | 22 | 16.4% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 134 | 16 | 68 | 28 | 22 |
| Average error / bias (mean of predicted − measured) [dB] | 13.984 | 30.041 | 1.252 | 25.229 | 27.345 |
| Standard deviation of error [dB] | 21.894 | 13.156 | 22.359 | 10.561 | 9.846 |
| Mean absolute error [dB] | 23.004 | 30.041 | 19.028 | 25.229 | 27.345 |
| Root mean square error [dB] | 25.910 | 32.630 | 22.229 | 27.277 | 28.987 |
| Median error [dB] | 20.365 | 28.645 | 1.945 | 21.825 | 25.240 |
| Median absolute deviation (robust spread) [dB] | 9.905 | 10.370 | 20.465 | 5.110 | 6.220 |
| 90th percentile of absolute error [dB] | 38.619 | 47.095 | 33.290 | 41.552 | 43.124 |
| 95th percentile of absolute error [dB] | 45.218 | 48.290 | 37.019 | 45.356 | 44.845 |
| Minimum error [dB] | -46.930 | 9.050 | -46.930 | 5.580 | 12.700 |
| Maximum error [dB] | 51.770 | 51.770 | 39.780 | 50.820 | 45.810 |
| Share within ±3 dB | 8.2% | 0.0% | 16.2% | 0.0% | 0.0% |
| Share within ±6 dB | 11.9% | 0.0% | 22.1% | 3.6% | 0.0% |
| Share within ±10 dB | 14.2% | 6.2% | 25.0% | 3.6% | 0.0% |

## Gateway: `!da5ad56c`

- Completed requests: **123**
- Failed requests: **0**
- Skipped rows (missing RSSI): **42**
- Number of samples (N): **123**
- Pearson correlation (predicted vs measured): **0.512**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 14 | 11.4% |
| Line of sight obstructed | 77 | 62.6% |
| 60% of first Fresnel zone obstructed | 19 | 15.4% |
| First Fresnel zone obstructed | 13 | 10.6% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 123 | 14 | 77 | 19 | 13 |
| Average error / bias (mean of predicted − measured) [dB] | 5.075 | 14.583 | -2.915 | 22.141 | 17.220 |
| Standard deviation of error [dB] | 19.289 | 8.467 | 19.591 | 8.216 | 6.099 |
| Mean absolute error [dB] | 16.495 | 15.790 | 15.108 | 22.141 | 17.220 |
| Root mean square error [dB] | 19.870 | 16.710 | 19.680 | 23.540 | 18.190 |
| Median error [dB] | 9.460 | 17.280 | -3.710 | 21.820 | 15.040 |
| Median absolute deviation (robust spread) [dB] | 12.040 | 1.785 | 11.620 | 3.640 | 6.070 |
| 90th percentile of absolute error [dB] | 30.172 | 18.646 | 35.538 | 29.302 | 23.278 |
| 95th percentile of absolute error [dB] | 37.034 | 22.630 | 40.278 | 31.031 | 24.582 |
| Minimum error [dB] | -58.120 | -8.450 | -58.120 | 1.920 | 7.740 |
| Maximum error [dB] | 50.870 | 29.760 | 50.870 | 37.160 | 26.490 |
| Share within ±3 dB | 5.7% | 0.0% | 7.8% | 5.3% | 0.0% |
| Share within ±6 dB | 16.3% | 0.0% | 24.7% | 5.3% | 0.0% |
| Share within ±10 dB | 35.0% | 21.4% | 46.8% | 10.5% | 15.4% |


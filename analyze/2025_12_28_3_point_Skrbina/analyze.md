# RF Site Planner – RSSI analysis

- Generated: 2025-12-31 12:52:58

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 119 | 0 | 46 | 119 | 18.100 | 21.679 | 6.449 | 31.054 | 14.3% | 0.335 |
| !7369fb6a | 134 | 0 | 31 | 134 | 23.378 | 26.212 | 13.888 | 39.456 | 8.2% | 0.347 |
| !da5ad56c | 123 | 0 | 42 | 123 | 16.423 | 19.674 | 4.637 | 29.672 | 18.7% | 0.520 |

## Gateway: `!75f19024`

- Completed requests: **119**
- Failed requests: **0**
- Skipped rows (missing RSSI): **46**
- Number of samples (N): **119**
- Pearson correlation (predicted vs measured): **0.335**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 42 | 35.3% |
| Line of sight obstructed | 58 | 48.7% |
| 60% of first Fresnel zone obstructed | 13 | 10.9% |
| First Fresnel zone obstructed | 6 | 5.0% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 119 | 42 | 58 | 13 | 6 |
| Average error / bias (mean of predicted − measured) [dB] | 6.449 | 20.313 | -8.316 | 23.271 | 15.690 |
| Standard deviation of error [dB] | 20.785 | 8.090 | 19.557 | 10.939 | 5.451 |
| Mean absolute error [dB] | 18.100 | 20.313 | 15.587 | 23.271 | 15.690 |
| Root mean square error [dB] | 21.679 | 21.829 | 21.096 | 25.534 | 16.460 |
| Median error [dB] | 11.610 | 19.250 | -5.620 | 21.820 | 17.330 |
| Median absolute deviation (robust spread) [dB] | 12.550 | 6.080 | 11.090 | 6.540 | 3.435 |
| 90th percentile of absolute error [dB] | 31.054 | 30.332 | 32.900 | 39.028 | 20.765 |
| 95th percentile of absolute error [dB] | 41.517 | 32.734 | 55.022 | 43.356 | 21.123 |
| Minimum error [dB] | -58.540 | 6.450 | -58.540 | 9.020 | 8.680 |
| Maximum error [dB] | 46.500 | 38.950 | 26.160 | 46.500 | 21.480 |
| Share within ±3 dB | 5.0% | 0.0% | 10.3% | 0.0% | 0.0% |
| Share within ±6 dB | 14.3% | 0.0% | 29.3% | 0.0% | 0.0% |
| Share within ±10 dB | 28.6% | 14.3% | 43.1% | 7.7% | 33.3% |

## Gateway: `!7369fb6a`

- Completed requests: **134**
- Failed requests: **0**
- Skipped rows (missing RSSI): **31**
- Number of samples (N): **134**
- Pearson correlation (predicted vs measured): **0.347**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 24 | 17.9% |
| Line of sight obstructed | 62 | 46.3% |
| 60% of first Fresnel zone obstructed | 32 | 23.9% |
| First Fresnel zone obstructed | 16 | 11.9% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 134 | 24 | 62 | 32 | 16 |
| Average error / bias (mean of predicted − measured) [dB] | 13.888 | 28.740 | -1.929 | 26.880 | 26.917 |
| Standard deviation of error [dB] | 22.314 | 10.579 | 21.898 | 10.230 | 12.191 |
| Mean absolute error [dB] | 23.378 | 28.740 | 18.580 | 26.880 | 26.917 |
| Root mean square error [dB] | 26.212 | 30.549 | 21.806 | 28.704 | 29.391 |
| Median error [dB] | 19.775 | 27.295 | -1.940 | 24.285 | 24.940 |
| Median absolute deviation (robust spread) [dB] | 10.775 | 4.730 | 19.840 | 5.390 | 10.245 |
| 90th percentile of absolute error [dB] | 39.456 | 44.865 | 31.507 | 43.460 | 42.340 |
| 95th percentile of absolute error [dB] | 44.718 | 46.872 | 36.477 | 44.296 | 46.618 |
| Minimum error [dB] | -42.450 | 8.510 | -42.450 | 9.220 | 9.980 |
| Maximum error [dB] | 51.770 | 47.130 | 46.220 | 50.820 | 51.770 |
| Share within ±3 dB | 7.5% | 0.0% | 16.1% | 0.0% | 0.0% |
| Share within ±6 dB | 8.2% | 0.0% | 17.7% | 0.0% | 0.0% |
| Share within ±10 dB | 14.2% | 4.2% | 25.8% | 3.1% | 6.2% |

## Gateway: `!da5ad56c`

- Completed requests: **123**
- Failed requests: **0**
- Skipped rows (missing RSSI): **42**
- Number of samples (N): **123**
- Pearson correlation (predicted vs measured): **0.520**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 14 | 11.4% |
| Line of sight obstructed | 78 | 63.4% |
| 60% of first Fresnel zone obstructed | 25 | 20.3% |
| First Fresnel zone obstructed | 6 | 4.9% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 123 | 14 | 78 | 25 | 6 |
| Average error / bias (mean of predicted − measured) [dB] | 4.637 | 14.583 | -3.264 | 20.514 | 17.987 |
| Standard deviation of error [dB] | 19.197 | 8.467 | 19.456 | 6.208 | 8.155 |
| Mean absolute error [dB] | 16.423 | 15.790 | 15.106 | 20.514 | 17.987 |
| Root mean square error [dB] | 19.674 | 16.710 | 19.605 | 21.397 | 19.466 |
| Median error [dB] | 8.010 | 17.280 | -3.155 | 21.110 | 21.185 |
| Median absolute deviation (robust spread) [dB] | 12.900 | 1.785 | 11.215 | 4.350 | 3.715 |
| 90th percentile of absolute error [dB] | 29.672 | 18.646 | 33.548 | 27.092 | 24.900 |
| 95th percentile of absolute error [dB] | 36.085 | 22.630 | 38.190 | 28.996 | 25.695 |
| Minimum error [dB] | -54.990 | -8.450 | -54.990 | 10.820 | 7.740 |
| Maximum error [dB] | 49.130 | 29.760 | 49.130 | 37.160 | 26.490 |
| Share within ±3 dB | 6.5% | 0.0% | 10.3% | 0.0% | 0.0% |
| Share within ±6 dB | 18.7% | 0.0% | 29.5% | 0.0% | 0.0% |
| Share within ±10 dB | 33.3% | 21.4% | 46.2% | 0.0% | 33.3% |


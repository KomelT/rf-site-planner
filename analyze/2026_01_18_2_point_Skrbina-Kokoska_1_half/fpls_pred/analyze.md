# RF Site Planner – RSSI analysis

- Generated: 2026-01-28 12:42:55

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 205 | 0 | 45 | 205 | 16.840 | 17.725 | 21.147 | 11.599 | 35.700 | 27.3% | 0.403 |
| !7369fb6a | 245 | 0 | 1 | 245 | 29.219 | 10.318 | 30.633 | 28.850 | 38.500 | 0.4% | 0.713 |

## Gateway: `!75f19024`

- Completed requests: **205**
- Failed requests: **0**
- Skipped rows (missing RSSI): **45**
- Number of samples (N): **205**
- Pearson correlation (path loss vs measured): **0.403**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 7.8% |
| Line of sight obstructed | 133 | 64.9% |
| 60% of first Fresnel zone obstructed | 37 | 18.0% |
| First Fresnel zone obstructed | 19 | 9.3% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 205 | 16 | 133 | 37 | 19 |
| Average error / bias (mean of path loss − measured) [dB] | 11.599 | 15.934 | 11.425 | 8.677 | 14.864 |
| Standard deviation of error [dB] | 17.725 | 8.390 | 18.474 | 19.763 | 13.136 |
| Mean absolute error [dB] | 16.840 | 15.934 | 16.470 | 17.999 | 17.929 |
| Root mean square error [dB] | 21.147 | 17.886 | 21.662 | 21.338 | 19.606 |
| Median error [dB] | 8.160 | 12.055 | 4.150 | 2.240 | 19.970 |
| Median absolute deviation (robust spread) [dB] | 15.820 | 5.220 | 12.010 | 14.250 | 6.170 |
| 90th percentile of absolute error [dB] | 35.700 | 27.870 | 36.552 | 32.922 | 26.706 |
| 95th percentile of absolute error [dB] | 38.086 | 30.812 | 38.568 | 35.760 | 28.970 |
| Minimum error [dB] | -12.980 | 5.820 | -11.920 | -12.980 | -10.040 |
| Maximum error [dB] | 50.970 | 30.820 | 50.970 | 40.560 | 28.970 |
| Share within ±3 dB | 12.2% | 0.0% | 16.5% | 8.1% | 0.0% |
| Share within ±6 dB | 27.3% | 6.2% | 34.6% | 18.9% | 10.5% |
| Share within ±10 dB | 42.0% | 37.5% | 51.9% | 18.9% | 21.1% |

## Gateway: `!7369fb6a`

- Completed requests: **245**
- Failed requests: **0**
- Skipped rows (missing RSSI): **1**
- Number of samples (N): **245**
- Pearson correlation (path loss vs measured): **0.713**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 13 | 5.3% |
| Line of sight obstructed | 145 | 59.2% |
| 60% of first Fresnel zone obstructed | 81 | 33.1% |
| First Fresnel zone obstructed | 6 | 2.4% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 245 | 13 | 145 | 81 | 6 |
| Average error / bias (mean of path loss − measured) [dB] | 28.850 | 19.697 | 31.837 | 25.765 | 18.155 |
| Standard deviation of error [dB] | 10.318 | 14.300 | 9.704 | 8.074 | 13.485 |
| Mean absolute error [dB] | 29.219 | 22.335 | 31.878 | 26.186 | 20.818 |
| Root mean square error [dB] | 30.633 | 24.015 | 33.273 | 26.985 | 21.935 |
| Median error [dB] | 29.690 | 23.100 | 32.350 | 26.820 | 20.970 |
| Median absolute deviation (robust spread) [dB] | 5.950 | 5.890 | 4.550 | 3.900 | 4.675 |
| 90th percentile of absolute error [dB] | 38.500 | 31.438 | 39.564 | 34.980 | 28.165 |
| 95th percentile of absolute error [dB] | 41.252 | 34.846 | 41.976 | 36.180 | 28.247 |
| Minimum error [dB] | -9.170 | -9.130 | -2.970 | -9.170 | -7.990 |
| Maximum error [dB] | 82.930 | 39.040 | 82.930 | 38.600 | 28.330 |
| Share within ±3 dB | 0.4% | 0.0% | 0.7% | 0.0% | 0.0% |
| Share within ±6 dB | 0.4% | 0.0% | 0.7% | 0.0% | 0.0% |
| Share within ±10 dB | 2.9% | 15.4% | 0.7% | 3.7% | 16.7% |


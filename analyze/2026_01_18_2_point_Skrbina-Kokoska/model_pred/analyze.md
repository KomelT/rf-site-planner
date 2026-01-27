# RF Site Planner – RSSI analysis

- Generated: 2026-01-25 20:28:53

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 360 | 0 | 78 | 360 | 28.590 | 25.382 | 35.129 | -24.323 | 57.606 | 11.1% | 0.325 |
| !7369fb6a | 427 | 0 | 7 | 427 | 15.522 | 19.271 | 19.612 | -3.759 | 34.018 | 24.6% | 0.674 |

## Gateway: `!75f19024`

- Completed requests: **360**
- Failed requests: **0**
- Skipped rows (missing RSSI): **78**
- Number of samples (N): **360**
- Pearson correlation (predicted vs measured): **0.325**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 41 | 11.4% |
| Line of sight obstructed | 214 | 59.4% |
| 60% of first Fresnel zone obstructed | 70 | 19.4% |
| First Fresnel zone obstructed | 35 | 9.7% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 360 | 41 | 214 | 70 | 35 |
| Average error / bias (mean of predicted − measured) [dB] | -24.323 | -4.698 | -37.673 | -7.192 | 0.051 |
| Standard deviation of error [dB] | 25.382 | 9.357 | 22.121 | 18.083 | 12.985 |
| Mean absolute error [dB] | 28.590 | 8.604 | 38.844 | 17.939 | 10.611 |
| Root mean square error [dB] | 35.129 | 10.367 | 43.661 | 19.341 | 12.799 |
| Median error [dB] | -23.435 | -6.720 | -41.465 | -16.635 | 4.220 |
| Median absolute deviation (robust spread) [dB] | 20.540 | 3.680 | 15.395 | 11.115 | 6.140 |
| 90th percentile of absolute error [dB] | 57.606 | 15.070 | 60.324 | 26.970 | 22.626 |
| 95th percentile of absolute error [dB] | 65.012 | 16.830 | 71.909 | 27.750 | 24.131 |
| Minimum error [dB] | -95.840 | -27.990 | -95.840 | -28.750 | -27.770 |
| Maximum error [dB] | 24.780 | 15.070 | 23.710 | 24.780 | 15.020 |
| Share within ±3 dB | 5.3% | 9.8% | 3.7% | 4.3% | 11.4% |
| Share within ±6 dB | 11.1% | 34.1% | 6.1% | 5.7% | 25.7% |
| Share within ±10 dB | 21.4% | 70.7% | 9.3% | 12.9% | 54.3% |

## Gateway: `!7369fb6a`

- Completed requests: **427**
- Failed requests: **0**
- Skipped rows (missing RSSI): **7**
- Number of samples (N): **427**
- Pearson correlation (predicted vs measured): **0.674**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 29 | 6.8% |
| Line of sight obstructed | 215 | 50.4% |
| 60% of first Fresnel zone obstructed | 158 | 37.0% |
| First Fresnel zone obstructed | 25 | 5.9% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 427 | 29 | 215 | 158 | 25 |
| Average error / bias (mean of predicted − measured) [dB] | -3.759 | 7.211 | -16.149 | 9.620 | 5.524 |
| Standard deviation of error [dB] | 19.271 | 11.820 | 18.621 | 7.994 | 11.415 |
| Mean absolute error [dB] | 15.522 | 11.614 | 19.934 | 11.029 | 10.506 |
| Root mean square error [dB] | 19.612 | 13.671 | 24.616 | 12.491 | 12.475 |
| Median error [dB] | 1.280 | 11.090 | -16.590 | 10.730 | 9.070 |
| Median absolute deviation (robust spread) [dB] | 12.030 | 7.180 | 13.830 | 4.560 | 5.800 |
| 90th percentile of absolute error [dB] | 34.018 | 21.606 | 40.468 | 19.126 | 21.012 |
| 95th percentile of absolute error [dB] | 40.506 | 23.548 | 43.962 | 21.080 | 22.484 |
| Minimum error [dB] | -68.170 | -24.880 | -68.170 | -24.920 | -23.730 |
| Maximum error [dB] | 64.410 | 23.230 | 64.410 | 24.090 | 21.340 |
| Share within ±3 dB | 12.6% | 13.8% | 12.1% | 12.0% | 20.0% |
| Share within ±6 dB | 24.6% | 27.6% | 24.2% | 23.4% | 32.0% |
| Share within ±10 dB | 37.0% | 41.4% | 31.6% | 42.4% | 44.0% |


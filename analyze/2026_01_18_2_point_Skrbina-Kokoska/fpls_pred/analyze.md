# RF Site Planner – RSSI analysis

- Generated: 2026-01-25 20:28:55

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (path loss vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 360 | 0 | 78 | 360 | 16.228 | 16.978 | 20.525 | 11.567 | 34.897 | 27.5% | 0.436 |
| !7369fb6a | 427 | 0 | 7 | 427 | 28.593 | 9.966 | 30.005 | 28.306 | 37.682 | 0.2% | 0.786 |

## Gateway: `!75f19024`

- Completed requests: **360**
- Failed requests: **0**
- Skipped rows (missing RSSI): **78**
- Number of samples (N): **360**
- Pearson correlation (path loss vs measured): **0.436**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 41 | 11.4% |
| Line of sight obstructed | 214 | 59.4% |
| 60% of first Fresnel zone obstructed | 70 | 19.4% |
| First Fresnel zone obstructed | 35 | 9.7% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 360 | 41 | 214 | 70 | 35 |
| Average error / bias (mean of path loss − measured) [dB] | 11.567 | 11.348 | 11.659 | 9.067 | 16.259 |
| Standard deviation of error [dB] | 16.978 | 9.215 | 18.203 | 18.074 | 13.017 |
| Mean absolute error [dB] | 16.228 | 12.529 | 16.410 | 16.432 | 19.041 |
| Root mean square error [dB] | 20.525 | 14.547 | 21.581 | 20.105 | 20.711 |
| Median error [dB] | 9.005 | 9.600 | 4.910 | 1.945 | 21.960 |
| Median absolute deviation (robust spread) [dB] | 14.960 | 3.870 | 12.560 | 13.925 | 5.900 |
| 90th percentile of absolute error [dB] | 34.897 | 22.840 | 36.548 | 32.781 | 27.914 |
| 95th percentile of absolute error [dB] | 36.745 | 28.800 | 38.567 | 34.088 | 28.970 |
| Minimum error [dB] | -12.980 | -12.230 | -12.230 | -12.980 | -12.010 |
| Maximum error [dB] | 52.230 | 30.820 | 52.230 | 40.560 | 30.770 |
| Share within ±3 dB | 13.1% | 4.9% | 15.4% | 15.7% | 2.9% |
| Share within ±6 dB | 27.5% | 17.1% | 33.2% | 25.7% | 8.6% |
| Share within ±10 dB | 42.5% | 46.3% | 50.0% | 30.0% | 17.1% |

## Gateway: `!7369fb6a`

- Completed requests: **427**
- Failed requests: **0**
- Skipped rows (missing RSSI): **7**
- Number of samples (N): **427**
- Pearson correlation (path loss vs measured): **0.786**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 29 | 6.8% |
| Line of sight obstructed | 215 | 50.4% |
| 60% of first Fresnel zone obstructed | 158 | 37.0% |
| First Fresnel zone obstructed | 25 | 5.9% |

### Error statistics by category (error = path loss − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 427 | 29 | 215 | 158 | 25 |
| Average error / bias (mean of path loss − measured) [dB] | 28.306 | 22.781 | 31.800 | 25.652 | 21.433 |
| Standard deviation of error [dB] | 9.966 | 11.515 | 9.759 | 7.693 | 11.409 |
| Mean absolute error [dB] | 28.593 | 23.964 | 31.913 | 25.868 | 22.634 |
| Root mean square error [dB] | 30.005 | 25.437 | 33.257 | 26.774 | 24.173 |
| Median error [dB] | 29.240 | 25.270 | 32.250 | 26.810 | 25.160 |
| Median absolute deviation (robust spread) [dB] | 5.640 | 6.450 | 4.320 | 4.645 | 5.810 |
| 90th percentile of absolute error [dB] | 37.682 | 34.058 | 39.564 | 34.769 | 31.600 |
| 95th percentile of absolute error [dB] | 39.843 | 35.786 | 41.941 | 36.254 | 35.588 |
| Minimum error [dB] | -9.170 | -9.130 | -9.140 | -9.170 | -7.990 |
| Maximum error [dB] | 82.930 | 39.040 | 82.930 | 39.930 | 37.260 |
| Share within ±3 dB | 0.2% | 0.0% | 0.5% | 0.0% | 0.0% |
| Share within ±6 dB | 0.2% | 0.0% | 0.5% | 0.0% | 0.0% |
| Share within ±10 dB | 2.8% | 10.3% | 0.9% | 3.2% | 8.0% |


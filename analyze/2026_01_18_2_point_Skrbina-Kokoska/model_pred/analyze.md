# RF Site Planner – RSSI analysis

- Generated: 2026-01-23 12:42:35

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 358 | 0 | 78 | 358 | 28.967 | 24.769 | 35.723 | -25.774 | 60.394 | 13.7% | 0.323 |
| !7369fb6a | 429 | 0 | 7 | 429 | 14.376 | 18.778 | 19.990 | -6.915 | 37.338 | 33.6% | 0.675 |

## Gateway: `!75f19024`

- Completed requests: **358**
- Failed requests: **0**
- Skipped rows (missing RSSI): **78**
- Number of samples (N): **358**
- Pearson correlation (predicted vs measured): **0.323**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 51 | 14.2% |
| Line of sight obstructed | 181 | 50.6% |
| 60% of first Fresnel zone obstructed | 80 | 22.3% |
| First Fresnel zone obstructed | 46 | 12.8% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 358 | 51 | 181 | 80 | 46 |
| Average error / bias (mean of predicted − measured) [dB] | -25.774 | -7.872 | -41.546 | -12.446 | -6.742 |
| Standard deviation of error [dB] | 24.769 | 9.792 | 21.756 | 17.189 | 17.290 |
| Mean absolute error [dB] | 28.967 | 10.433 | 42.412 | 18.633 | 14.587 |
| Root mean square error [dB] | 35.723 | 12.488 | 46.870 | 21.134 | 18.382 |
| Median error [dB] | -25.090 | -9.510 | -45.290 | -22.185 | 0.400 |
| Median absolute deviation (robust spread) [dB] | 20.055 | 5.600 | 15.020 | 9.385 | 9.610 |
| 90th percentile of absolute error [dB] | 60.394 | 17.710 | 62.870 | 31.560 | 31.775 |
| 95th percentile of absolute error [dB] | 62.964 | 21.270 | 73.820 | 32.560 | 31.780 |
| Minimum error [dB] | -99.360 | -32.800 | -99.360 | -33.560 | -32.580 |
| Maximum error [dB] | 19.970 | 10.260 | 19.510 | 17.970 | 19.970 |
| Share within ±3 dB | 7.3% | 15.7% | 3.3% | 7.5% | 13.0% |
| Share within ±6 dB | 13.7% | 25.5% | 3.9% | 17.5% | 32.6% |
| Share within ±10 dB | 22.3% | 49.0% | 5.5% | 27.5% | 50.0% |

## Gateway: `!7369fb6a`

- Completed requests: **429**
- Failed requests: **0**
- Skipped rows (missing RSSI): **7**
- Number of samples (N): **429**
- Pearson correlation (predicted vs measured): **0.675**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 33 | 7.7% |
| Line of sight obstructed | 190 | 44.3% |
| 60% of first Fresnel zone obstructed | 163 | 38.0% |
| First Fresnel zone obstructed | 43 | 10.0% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 429 | 33 | 190 | 163 | 43 |
| Average error / bias (mean of predicted − measured) [dB] | -6.915 | 1.972 | -19.988 | 4.336 | 1.378 |
| Standard deviation of error [dB] | 18.778 | 12.224 | 19.473 | 8.486 | 9.924 |
| Mean absolute error [dB] | 14.376 | 9.520 | 22.447 | 7.702 | 7.744 |
| Root mean square error [dB] | 19.990 | 12.198 | 27.869 | 9.506 | 9.904 |
| Median error [dB] | -1.880 | 4.320 | -18.255 | 5.430 | 4.260 |
| Median absolute deviation (robust spread) [dB] | 9.380 | 6.950 | 14.965 | 4.810 | 4.280 |
| 90th percentile of absolute error [dB] | 37.338 | 19.492 | 46.487 | 14.278 | 14.356 |
| 95th percentile of absolute error [dB] | 45.456 | 28.038 | 50.113 | 16.728 | 15.701 |
| Minimum error [dB] | -68.380 | -30.690 | -68.380 | -30.730 | -29.540 |
| Maximum error [dB] | 62.860 | 27.010 | 62.860 | 22.770 | 15.720 |
| Share within ±3 dB | 14.0% | 18.2% | 9.5% | 17.8% | 16.3% |
| Share within ±6 dB | 33.6% | 36.4% | 20.5% | 43.6% | 51.2% |
| Share within ±10 dB | 55.2% | 69.7% | 33.2% | 73.0% | 74.4% |


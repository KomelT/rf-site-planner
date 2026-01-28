# RF Site Planner – RSSI analysis

- Generated: 2026-01-28 17:24:16

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 157 | 0 | 33 | 157 | 18.689 | 19.511 | 23.143 | -12.543 | 37.402 | 15.3% | 0.379 |
| !7369fb6a | 183 | 0 | 6 | 183 | 11.556 | 11.877 | 13.791 | 7.063 | 21.642 | 27.9% | 0.760 |

## Gateway: `!75f19024`

- Completed requests: **157**
- Failed requests: **0**
- Skipped rows (missing RSSI): **33**
- Number of samples (N): **157**
- Pearson correlation (predicted vs measured): **0.379**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 25 | 15.9% |
| Line of sight obstructed | 83 | 52.9% |
| 60% of first Fresnel zone obstructed | 33 | 21.0% |
| First Fresnel zone obstructed | 16 | 10.2% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 157 | 25 | 83 | 33 | 16 |
| Average error / bias (mean of predicted − measured) [dB] | -12.543 | -7.685 | -18.749 | -6.687 | -0.020 |
| Standard deviation of error [dB] | 19.511 | 8.561 | 21.722 | 16.273 | 14.218 |
| Mean absolute error [dB] | 18.689 | 9.056 | 24.058 | 15.924 | 11.596 |
| Root mean square error [dB] | 23.143 | 11.376 | 28.595 | 17.364 | 13.766 |
| Median error [dB] | -11.990 | -6.890 | -19.570 | -16.270 | 4.710 |
| Median absolute deviation (robust spread) [dB] | 13.516 | 4.170 | 14.672 | 10.480 | 6.955 |
| 90th percentile of absolute error [dB] | 37.402 | 16.530 | 43.750 | 25.612 | 22.530 |
| 95th percentile of absolute error [dB] | 44.876 | 24.918 | 52.810 | 26.744 | 24.425 |
| Minimum error [dB] | -71.392 | -27.990 | -71.392 | -27.750 | -27.770 |
| Maximum error [dB] | 26.067 | 13.050 | 26.067 | 19.030 | 15.020 |
| Share within ±3 dB | 7.0% | 16.0% | 4.8% | 6.1% | 6.2% |
| Share within ±6 dB | 15.3% | 40.0% | 8.4% | 9.1% | 25.0% |
| Share within ±10 dB | 28.0% | 64.0% | 19.3% | 18.2% | 37.5% |

## Gateway: `!7369fb6a`

- Completed requests: **183**
- Failed requests: **0**
- Skipped rows (missing RSSI): **6**
- Number of samples (N): **183**
- Pearson correlation (predicted vs measured): **0.760**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 8.7% |
| Line of sight obstructed | 71 | 38.8% |
| 60% of first Fresnel zone obstructed | 78 | 42.6% |
| First Fresnel zone obstructed | 18 | 9.8% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 183 | 16 | 71 | 78 | 18 |
| Average error / bias (mean of predicted − measured) [dB] | 7.063 | 9.909 | 4.004 | 9.415 | 6.405 |
| Standard deviation of error [dB] | 11.877 | 8.935 | 15.243 | 7.930 | 11.208 |
| Mean absolute error [dB] | 11.556 | 11.411 | 12.797 | 10.658 | 10.687 |
| Root mean square error [dB] | 13.791 | 13.154 | 15.656 | 12.277 | 12.636 |
| Median error [dB] | 9.280 | 12.205 | 3.751 | 10.325 | 10.600 |
| Median absolute deviation (robust spread) [dB] | 7.514 | 6.175 | 11.116 | 5.395 | 6.490 |
| 90th percentile of absolute error [dB] | 21.642 | 19.775 | 26.425 | 18.452 | 20.766 |
| 95th percentile of absolute error [dB] | 25.254 | 21.095 | 28.704 | 19.779 | 21.554 |
| Minimum error [dB] | -29.931 | -7.940 | -29.931 | -15.710 | -22.770 |
| Maximum error [dB] | 33.305 | 21.200 | 33.305 | 24.090 | 21.340 |
| Share within ±3 dB | 16.4% | 18.8% | 14.1% | 17.9% | 16.7% |
| Share within ±6 dB | 27.9% | 25.0% | 29.6% | 25.6% | 33.3% |
| Share within ±10 dB | 45.4% | 37.5% | 47.9% | 46.2% | 38.9% |


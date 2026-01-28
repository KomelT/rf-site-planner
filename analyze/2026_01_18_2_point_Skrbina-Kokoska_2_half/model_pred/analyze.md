# RF Site Planner – RSSI analysis

- Generated: 2026-01-28 12:43:41

## Summary per gateway

| Gateway (site id) | Completed requests | Failed requests | Skipped rows (missing RSSI) | Number of samples (N) | Mean absolute error [dB] | Standard deviation of error [dB] | Root mean square error [dB] | Average error / bias [dB] | 90th percentile of absolute error [dB] | Share within ±6 dB | Pearson correlation (predicted vs measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| !75f19024 | 155 | 0 | 33 | 155 | 25.140 | 23.968 | 31.688 | -20.818 | 52.188 | 14.2% | 0.354 |
| !7369fb6a | 182 | 0 | 6 | 182 | 14.072 | 17.717 | 17.673 | 0.398 | 28.127 | 25.8% | 0.702 |

## Gateway: `!75f19024`

- Completed requests: **155**
- Failed requests: **0**
- Skipped rows (missing RSSI): **33**
- Number of samples (N): **155**
- Pearson correlation (predicted vs measured): **0.354**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 25 | 16.1% |
| Line of sight obstructed | 81 | 52.3% |
| 60% of first Fresnel zone obstructed | 33 | 21.3% |
| First Fresnel zone obstructed | 16 | 10.3% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 155 | 25 | 81 | 33 | 16 |
| Average error / bias (mean of predicted − measured) [dB] | -20.818 | -7.685 | -35.093 | -6.687 | 1.787 |
| Standard deviation of error [dB] | 23.968 | 8.561 | 22.387 | 16.273 | 13.062 |
| Mean absolute error [dB] | 25.140 | 9.056 | 36.713 | 15.924 | 10.685 |
| Root mean square error [dB] | 31.688 | 11.376 | 41.551 | 17.364 | 12.773 |
| Median error [dB] | -19.370 | -6.890 | -39.280 | -16.270 | 6.690 |
| Median absolute deviation (robust spread) [dB] | 18.430 | 4.170 | 13.880 | 10.480 | 4.975 |
| 90th percentile of absolute error [dB] | 52.188 | 16.530 | 65.430 | 25.612 | 19.420 |
| 95th percentile of absolute error [dB] | 66.459 | 24.918 | 72.510 | 26.744 | 24.425 |
| Minimum error [dB] | -79.360 | -27.990 | -79.360 | -27.750 | -27.770 |
| Maximum error [dB] | 21.560 | 13.050 | 21.560 | 19.030 | 15.020 |
| Share within ±3 dB | 5.8% | 16.0% | 2.5% | 6.1% | 6.2% |
| Share within ±6 dB | 14.2% | 40.0% | 6.2% | 9.1% | 25.0% |
| Share within ±10 dB | 23.2% | 64.0% | 8.6% | 18.2% | 43.8% |

## Gateway: `!7369fb6a`

- Completed requests: **182**
- Failed requests: **0**
- Skipped rows (missing RSSI): **6**
- Number of samples (N): **182**
- Pearson correlation (predicted vs measured): **0.702**

### Distribution by visibility category

| Category | N | Share |
| --- | --- | --- |
| Line of sight clear (no obstructions) | 16 | 8.8% |
| Line of sight obstructed | 70 | 38.5% |
| 60% of first Fresnel zone obstructed | 77 | 42.3% |
| First Fresnel zone obstructed | 19 | 10.4% |

### Error statistics by category (error = predicted − measured)

| Metric | All samples | Line of sight clear | Line of sight obstructed | Fresnel 60% obstructed | First Fresnel obstructed |
| --- | --- | --- | --- | --- | --- |
| Number of samples (N) | 182 | 16 | 70 | 77 | 19 |
| Average error / bias (mean of predicted − measured) [dB] | 0.398 | 9.909 | -13.237 | 9.300 | 6.545 |
| Standard deviation of error [dB] | 17.717 | 8.935 | 19.938 | 7.917 | 10.910 |
| Mean absolute error [dB] | 14.072 | 11.411 | 19.486 | 10.559 | 10.602 |
| Root mean square error [dB] | 17.673 | 13.154 | 23.814 | 12.180 | 12.474 |
| Median error [dB] | 4.880 | 12.205 | -14.630 | 10.310 | 10.140 |
| Median absolute deviation (robust spread) [dB] | 9.355 | 6.175 | 14.560 | 5.360 | 6.310 |
| 90th percentile of absolute error [dB] | 28.127 | 19.775 | 41.357 | 17.844 | 20.684 |
| 95th percentile of absolute error [dB] | 38.534 | 21.095 | 45.351 | 19.882 | 21.483 |
| Minimum error [dB] | -50.520 | -7.940 | -50.520 | -15.710 | -22.770 |
| Maximum error [dB] | 25.710 | 21.200 | 25.710 | 24.090 | 21.340 |
| Share within ±3 dB | 14.8% | 18.8% | 10.0% | 18.2% | 15.8% |
| Share within ±6 dB | 25.8% | 25.0% | 24.3% | 26.0% | 31.6% |
| Share within ±10 dB | 37.9% | 37.5% | 27.1% | 46.8% | 42.1% |


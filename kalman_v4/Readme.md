
## Planned Enhancements (v4 – Temporal Robustness)

Version 4 will focus on **behavioral robustness** rather than estimator accuracy.  
The objective is to improve decision stability and evaluation clarity under short-lived, real-time operation (~30 minutes).

v4 does **not** change the estimator model or confidence formulation introduced in v3.  
Instead, it refines **when and how** extrapolation decisions are allowed and evaluated.

---

### 1. Confidence Hysteresis

In v3, Kalman extrapolation may be enabled by a single high-confidence tick.  
While correct, this can allow short-lived activations caused by transient noise.

v4 will introduce **temporal hysteresis**, requiring confidence to exceed the threshold for **N consecutive time steps** (default: `N = 2`) before enabling extrapolation.

This ensures that:
- Kalman activation reflects sustained structure
- Single-tick false positives are suppressed
- Decision logic behaves more like a debounced control system

---

### 2. Kalman-Active Window Tracking

Rather than treating each forecast independently, v4 will explicitly track **Kalman-active windows**.

For each window, the system will record:
- start and end timestamps  
- duration (minutes)  
- mean confidence  
- mean estimated velocity  

This allows analysis at the **event level**, which is more informative than point-wise statistics under limited runtime.

---

### 3. Kalman-Only Error Reporting

Global error metrics are misleading when extrapolation is intentionally sparse.

In v4:
- Forecast error metrics (MAE / RMSE) will be computed **only for Kalman-active windows**
- The number of Kalman forecasts will always be reported alongside error metrics

This ensures that performance evaluation reflects **when the system chose to act**, rather than being dominated by persistence fallback periods.

---

### Design Rationale

These enhancements are motivated by practical constraints:
- short live runtimes  
- highly non-stationary noise  
- limited number of coherent intervals  

v4 prioritizes **decision hygiene, interpretability, and honest evaluation** over increased prediction frequency.

---

### Summary

v4 extends the v3 architecture by adding **temporal consistency and event-level evaluation**, without increasing model complexity.

The guiding principle remains unchanged:

> *In chaotic environments, disciplined restraint outperforms frequent low-confidence action.*

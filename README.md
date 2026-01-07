Adaptive Online Kalman Estimator

Short-Horizon Forecasting Under Non-Stationarity

Overview

This repository implements a real-time adaptive Kalman state-space estimator for short-horizon forecasting and evaluates it against simple, widely used baselines.

The focus of this project is estimation quality under non-stationary noise, not trading signals or profitability.

Key characteristics:

Online operation only (no replay, no backtesting)

Walk-forward validation

Explicit baseline comparison

Transparent limitations

Problem Statement

Short-horizon forecasting in real systems (financial markets, industrial sensors, energy signals) is dominated by:

Non-stationarity

Noise bursts and regime changes

Lag in static smoothing methods

The core question addressed here is:

Can an adaptive state-space estimator reduce magnitude error and recover faster from disturbances compared to naïve models?

This project deliberately avoids claims about market predictability or trading performance.

Model Formulation

The estimator is implemented as a linear state-space model with explicit, interpretable dynamics.
Equations are rendered as images to ensure consistent display across GitHub themes and devices.

State Vector

The latent state is defined as:

𝑥
𝑡
=
[
𝑝
𝑡


𝑣
𝑡
]
x
t
	​

=[
p
t
	​

v
t
	​

	​

]

Where:

𝑝
𝑡
p
t
	​

 is the estimated price

𝑣
𝑡
v
t
	​

 is the estimated short-term velocity

Why this formulation

Separates level (price) from dynamics (velocity)

Enables short-horizon extrapolation without lagged smoothing

Keeps the model minimal and physically interpretable

State Transition Model (Constant Velocity)

The system dynamics are modeled using a constant-velocity linear transition:

𝑥
𝑡
+
1
=
[
1
	
1


0
	
1
]
𝑥
𝑡
+
𝑤
𝑡
x
t+1
	​

=[
1
0
	​

1
1
	​

]x
t
	​

+w
t
	​


Where:

𝑥
𝑡
x
t
	​

 is the current state

𝑤
𝑡
w
t
	​

 represents process noise capturing model uncertainty

Design rationale

Assumes locally linear motion over short horizons

Avoids overfitting by limiting model complexity

Stable under online estimation

Well-suited for noisy, high-frequency signals

A physical bound is applied to the velocity state to prevent unrealistic extrapolations during transient conditions.

Measurement Model

The measurement equation relates the latent state to the observed price:

𝑧
𝑡
=
[
1
  
  
0
]
 
𝑥
𝑡
+
𝑣
𝑡
z
t
	​

=[10]x
t
	​

+v
t
	​


Where:

𝑧
𝑡
z
t
	​

 is the observed price

𝑣
𝑡
v
t
	​

 represents measurement noise

Only the price component of the state is directly observed.

Adaptive Noise Handling

To operate under changing noise conditions:

Measurement noise (R) is adapted using innovation variance

Process noise (Q) adapts slowly to reflect model mismatch

Key principles:

No indicator-driven noise manipulation

No hindsight or retrospective fitting

Clear separation between estimation and evaluation

A warm-up phase is enforced to avoid initialization artifacts.

Baseline Models

The Kalman estimator is benchmarked against:

Persistence (Random Walk)

𝑝
^
𝑡
+
ℎ
=
𝑝
𝑡
p
^
	​

t+h
	​

=p
t
	​


EMA(10)

EMA(20)

These baselines represent minimal-assumption methods commonly used in practice and serve as hard performance benchmarks.

Evaluation Methodology
Online Walk-Forward Validation

Predictions are generated at time 
𝑡
t

Validation occurs only after the forecast horizon matures

No replay or retrospective fitting

Forecast horizons:

+5 minutes

+10 minutes

+20 minutes

Metrics

For each model and horizon:

Mean Absolute Error (MAE)

Root Mean Squared Error (RMSE)

Directional Accuracy (sign only)

No binary “pass/fail” logic is used.

Observed Behavior (Live Runs)

Empirical observations from live execution show that:

Direction frequently fails for all models during micro-reversals

EMA and persistence remain competitive at very short horizons

The Kalman estimator often:

Reduces magnitude error at longer horizons

Re-anchors faster after volatility disturbances

Exhibits lower lag than exponential smoothing

These behaviors are consistent with state estimation, not directional prediction.

Limitations

This project explicitly does not claim:

Trading profitability

Directional market predictability

Optimal parameter tuning

Known constraints:

Linear dynamics assumption

No regime classification

No nonlinear or asymmetric state modeling

These limitations are intentional to preserve interpretability and methodological clarity.

Why This Matters Beyond Finance

Although demonstrated on BTC price data, the methodology applies directly to:

Industrial sensor estimation

Energy demand smoothing

Control systems under noisy measurements

Predictive maintenance signals

Real-time monitoring systems

The asset is incidental — the estimator is the contribution.

Repository Structure
adaptive-kalman-estimator/
│
├── kalman.py          # Online estimator & data collection
├── results.csv        # Logged predictions and observations
├── analysis.ipynb     # Offline evaluation & metrics
├── README.md
└── figures/
    ├── state_vector.png
    ├── state_transition.png
    └── measurement_model.png

Future Work

Potential extensions include:

Regime-aware switching models

Higher-order (acceleration) dynamics

Confidence-weighted directional gating

Application to industrial or energy datasets

Final Note

This project is intentionally conservative.

In a domain dominated by overfitting and narrative bias,
transparent methodology and honest benchmarking are the result.

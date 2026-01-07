#Adaptive Online Kalman Estimator
Short-Horizon Forecasting under Non-Stationarity
A disciplined benchmark study of an online adaptive Kalman filter versus naïve baselines in a noisy, non-stationary time series.
________________________________________
What This Is
This repository implements a real-time, online Kalman state-space estimator for short-horizon forecasting and benchmarks it against simple baselines.
The goal is estimation quality, not trading signals.
No back tests.
No hindsight.
No profit claims.
________________________________________
Problem
Short-horizon forecasting in real systems is dominated by:
•	Noise bursts
•	Regime changes
•	Lagging baseline models
The core question:
Can an adaptive state-space estimator reduce magnitude error and recover faster after disturbances compared to naïve models?
________________________________________
Model Summary
State Vector
 


Dynamics
Constant-velocity linear model:
 
Measurement
Observed price only:
 

Key Design Choices
•	Online operation only (no replay)
•	Adaptive Q/R via innovation statistics
•	Warm-up phase to avoid initialization artefacts
•	Physical constraints on velocity state
________________________________________
Baselines
The estimator is compared against:
•	Persistence (Random Walk)
•	EMA(10)
•	EMA(20)
These baselines represent what simple, widely used methods achieve with minimal assumptions.
________________________________________
Evaluation Protocol
•	Walk-forward validation only
•	Forecast horizons:
o	+5 min
o	+10 min
o	+20 min
•	Validation occurs strictly after horizon maturity
Metrics
•	Mean Absolute Error (MAE)
•	Root Mean Squared Error (RMSE)
•	Directional Accuracy (sign only)
No binary “pass/fail” logic.
________________________________________
Observed Behaviour (Live Runs)
Empirical observations from live execution:
•	Direction frequently fails for all models during micro-reversals
•	EMA and persistence are competitive at very short horizons
•	The Kalman estimator often:
o	Reduces magnitude error at longer horizons
o	Re-anchors faster after volatility spikes
o	Exhibits lower lag than EMA smoothing
These behaviours are consistent with state estimation, not directional prediction.
________________________________________
Limitations (Explicit)
This project does not claim:
•	Trading profitability
•	Directional edge
•	Optimal tuning
Known constraints:
•	Linear dynamics
•	No regime classification
•	No nonlinear or asymmetric states
These are deliberate to preserve interpretability.
________________________________________
Why This Matters Beyond Finance
Although demonstrated on BTC price data, the methodology applies to:
•	Industrial sensors
•	Energy demand estimation
•	Control systems
•	Predictive maintenance
•	Real-time monitoring under noise
The asset is incidental — the estimator is the point.
________________________________________
Future Work
•	Regime-aware switching models
•	Higher-order (acceleration) dynamics
•	Confidence-weighted directional gating
•	Application to industrial datasets
________________________________________
Final Note
This project is intentionally conservative.
In a field dominated by overfitting and narrative bias,
honest benchmarking and reproducibility are the result.


"""
kalman_v2.py
-----------------
Adaptive Kalman Filter used strictly as a FAIR-PRICE ESTIMATOR
under noisy, non-stationary market data.

No forecasting.
No horizons.
No validation logic.

Author intent:
- Estimate latent fair price + velocity
- Suppress microstructure noise
- Preserve responsiveness vs EMA
"""

import time
import csv
import argparse
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import ccxt


# ===============================
# Argument parsing
# ===============================
def parse_args():
    p = argparse.ArgumentParser(description="Kalman v2 – Fair Price Estimator")
    p.add_argument("--symbol", type=str, default="BTC/USDT")
    p.add_argument("--timeframe", type=str, default="1m")
    p.add_argument("--exchange", type=str, default="binance")
    p.add_argument("--out", type=str, default="results_v2.csv")
    return p.parse_args()


# ===============================
# Exchange
# ===============================
def init_exchange(name):
    ex = getattr(ccxt, name)()
    ex.load_markets()
    return ex


# ===============================
# Kalman initialization
# ===============================
def init_kalman():
    # State: [price, velocity]
    x = np.array([[0.0], [0.0]])

    # Covariance
    P = np.eye(2) * 10.0

    # Transition (constant velocity)
    F = np.array([[1.0, 1.0],
                  [0.0, 1.0]])

    # Measurement matrix (price only)
    H = np.array([[1.0, 0.0]])

    # Base noise (will adapt)
    Q_base = np.array([[0.01, 0.0],
                       [0.0, 0.001]])

    R_base = np.array([[0.1]])

    return x, P, F, H, Q_base, R_base


# ===============================
# CSV logger
# ===============================
def init_csv(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "symbol",
            "raw_price",
            "fair_price",
            "fair_velocity",
            "Q_scale",
            "R_scale"
        ])


def append_csv(path, row):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


# ===============================
# Main loop
# ===============================
def run():
    args = parse_args()
    ex = init_exchange(args.exchange)

    symbol = args.symbol
    tf = args.timeframe
    out_csv = args.out

    init_csv(out_csv)

    # Kalman
    x, P, F, H, Q_base, R_base = init_kalman()

    Q_scale = 1.0
    R_scale = 1.0

    last_ts = None

    print("[INFO] Kalman v2 started (fair-price estimator only)")
    print("[INFO] Press Ctrl+C to stop")

    while True:
        try:
            ohlcv = ex.fetch_ohlcv(symbol, tf, limit=2)
            ts, _, _, _, close, _ = ohlcv[-1]

            close_dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)

            if last_ts == close_dt:
                time.sleep(1)
                continue

            last_ts = close_dt
            z = np.array([[float(close)]])

            # ---------- PREDICT ----------
            Q = Q_base * Q_scale
            x = F @ x
            P = F @ P @ F.T + Q

            # ---------- UPDATE ----------
            y = z - (H @ x)                    # innovation
            S = H @ P @ H.T + R_base * R_scale
            K = P @ H.T @ np.linalg.inv(S)

            x = x + K @ y
            P = (np.eye(2) - K @ H) @ P

            # ---------- ADAPT NOISE ----------
            innovation_mag = abs(float(y[0, 0]))

            R_scale = 0.95 * R_scale + 0.05 * min(10.0, innovation_mag)
            Q_scale = 0.98 * Q_scale + 0.02 * min(5.0, innovation_mag)

            # ---------- FAIR PRICE ----------
            fair_price = float(x[0, 0])
            fair_velocity = float(x[1, 0])

            # Velocity sanity clamp
            fair_velocity = float(np.clip(fair_velocity, -2000, 2000))
            x[1, 0] = fair_velocity

            # ---------- LOG ----------
            append_csv(out_csv, [
                close_dt.isoformat(),
                symbol,
                float(close),
                fair_price,
                fair_velocity,
                Q_scale,
                R_scale
            ])

            # ---------- CONSOLE ----------
            print(
                f"[{close_dt.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"raw={close:,.2f} | fair={fair_price:,.2f} | "
                f"vel={fair_velocity:,.2f} | "
                f"Q={Q_scale:.3e} R={R_scale:.3e}"
            )

        except KeyboardInterrupt:
            print("\n[INFO] Stopped by user")
            break
        except Exception as e:
            print("[WARN]", str(e))
            time.sleep(5)


if __name__ == "__main__":
    run()

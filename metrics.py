import joblib

model_metrics = joblib.load("model_metrics.pkl")
trading_metrics = joblib.load("trading_metrics.pkl")

print("\n===== MODEL METRICS =====")
for k, v in model_metrics.items():
    print(f"{k}: {v:.4f}")

print("\n===== TRADING METRICS =====")
for k, v in trading_metrics.items():
    print(f"{k}: {v}")

with open("metrics.txt", "w") as f:
    f.write("MODEL METRICS\n")
    for k, v in model_metrics.items():
        f.write(f"{k}: {v}\n")

    f.write("\nTRADING METRICS\n")
    for k, v in trading_metrics.items():
        f.write(f"{k}: {v}\n")

print("\nMetrics printed and saved to metrics.txt")

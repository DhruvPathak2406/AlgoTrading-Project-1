import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib

df = pd.read_csv("features.csv")

FEATURES = ["SMA_20", "SMA_50", "Return", "Momentum"]
X = df[FEATURES]
y = df["Target"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, shuffle=False, test_size=0.2
)

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    class_weight="balanced",
    random_state=42
)
rf.fit(X_train, y_train)

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

xgb = XGBClassifier(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    eval_metric="logloss",
    random_state=42,
    n_jobs=1,
    scale_pos_weight=scale_pos_weight
)
xgb.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
xgb_pred = xgb.predict(X_test)

print("RF Precision:", precision_score(y_test, rf_pred))
print("RF Recall:", recall_score(y_test, rf_pred))
print("XGB Precision:", precision_score(y_test, xgb_pred))
print("XGB Recall:", recall_score(y_test, xgb_pred))

joblib.dump(rf, "rf_model.pkl")
joblib.dump(xgb, "xgb_model.pkl")

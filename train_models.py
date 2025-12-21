import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

df = pd.read_csv("features.csv")

X = df[["SMA_20", "SMA_50", "Return", "Momentum"]]
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, shuffle=False, test_size=0.2
)
rf = RandomForestClassifier(n_estimators=300, max_depth=6)
rf.fit(X_train, y_train)

xgb = XGBClassifier(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    eval_metric="logloss"
)
xgb.fit(X_train, y_train)

print("RF Accuracy:", accuracy_score(y_test, rf.predict(X_test)))
print("XGB Accuracy:", accuracy_score(y_test, xgb.predict(X_test)))


import joblib
joblib.dump(rf, "rf_model.pkl")
joblib.dump(xgb, "xgb_model.pkl")


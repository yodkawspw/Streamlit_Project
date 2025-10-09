# train_omakase_ohe.py
"""
เทรนโมเดลแนะนำคอร์สโอมากาเสะด้วย OneHotEncoder + RandomForest (balanced)
- อ่านข้อมูลจาก omakase_dataset.xlsx
- เติม missing, รวมหมวดหายาก "(อื่นๆ)"
- ใช้ Pipeline: OneHotEncoder(handle_unknown="ignore") -> RandomForestClassifier
- ตั้ง class_weight="balanced", n_estimators=1000, max_depth จำกัดความลึก
- ประเมินด้วย 5-fold CV + Holdout test
- บันทึกโมเดล (.pkl) + เมทาดาทา (.json) + รายงาน (.txt)
"""

from pathlib import Path
import json
import pandas as pd
from collections import defaultdict

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -------------------- Paths & Config --------------------
ROOT        = Path(__file__).parent.resolve()
DATA_PATH   = ROOT / "omakase_dataset.xlsx"     # <-- ไฟล์ Excel 100 แถว
MODEL_PATH  = ROOT / "omakase_model_ohe.pkl"    # โมเดลที่บันทึก
META_PATH   = ROOT / "preprocess_metadata_ohe.json"
REPORT_PATH = ROOT / "training_report_ohe.txt"

# จำกัดความลึก (ปรับได้): ลึกมากไปจะ overfit กับชุดเล็ก
RF_MAX_DEPTH = 10
RF_ESTIMATORS = 1000
CV_FOLDS = 5
MIN_FREQ = 3  # รวมหมวดที่พบน้อยกว่า MIN_FREQ เป็น "(อื่นๆ)"

# -------------------- Rename columns (TH -> short feature names) --------------------
RENAME_COLS = {
    "วันนี้คุณอยากได้ประสบการณ์แบบไหน?": "experience",
    "คุณชอบรสชาติในแนวไหนมากที่สุด?": "taste",
    "ระดับความผจญภัยของคุณในการลองเมนูใหม่ ๆ": "adventure",
    "ถ้าให้เลือกระหว่าง 'ดั้งเดิม' กับ 'สร้างสรรค์' คุณอยากได้สไตล์มากกว่ากัน?": "style",
    "เนื้อสัตว์หรือวัตถุดิบหลักที่คุณชอบที่สุด?": "main_ing",
    "วัตถุดิบที่คุณไม่อยากเจอในคอร์สนี้?": "avoid",
    "คุณชอบเนื้อสัมผัสของอาหารแบบไหนเป็นพิเศษ": "texture",
    "คุณคาดหวังความอิ่มจากคอร์สมื้อนี้แค่ไหน?": "fullness",
    "มื้อนี้คุณมาทานกับใคร?": "companion",
    "ถ้าให้เลือกความประทับใจหลังจบมื้อ คุณอยากให้เชฟทำให้คุณรู้สึกแบบไหน?": "impression",
    "คอร์สโอมากาเสะที่คุณเลือก/เหมาะสมที่สุด": "target",
}

# -------------------- Load data --------------------
print(f"Loading: {DATA_PATH}")
df = pd.read_excel(DATA_PATH).rename(columns=RENAME_COLS)

# -------------------- EDA (brief) --------------------
eda_lines = []
eda_lines.append(f"Shape: {df.shape[0]} rows x {df.shape[1]} cols")
eda_lines.append("\nMissing values per column:")
eda_lines.append(df.isna().sum().to_string())
eda_lines.append("\n\nTarget distribution:")
eda_lines.append(df["target"].value_counts().to_string())

# -------------------- Preprocess: fill missing + rare category grouping --------------------
df = df.fillna("ไม่ระบุ")
rare_values = defaultdict(list)

for col in df.columns:
    if col == "target":
        continue
    vc = df[col].value_counts(dropna=False)
    rare_cats = vc[vc < MIN_FREQ].index.tolist()
    if rare_cats:
        rare_values[col] = rare_cats
        df[col] = df[col].where(~df[col].isin(rare_cats), other="(อื่นๆ)")

eda_lines.append(f"\n\nRare-category mapping (min_freq = {MIN_FREQ}):")
for k, v in rare_values.items():
    if v:
        eda_lines.append(f"- {k}: {v}")

# -------------------- Split X, y --------------------
X = df.drop(columns=["target"])
y = df["target"]
cat_cols = X.columns.tolist()

# -------------------- Build Pipeline: OneHotEncoder + RandomForest --------------------
preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ]
)

clf = Pipeline(steps=[
    ("prep", preprocess),
    ("rf", RandomForestClassifier(
        n_estimators=RF_ESTIMATORS,
        max_depth=RF_MAX_DEPTH,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

# -------------------- Cross-validation --------------------
cv_scores = cross_val_score(clf, X, y, cv=CV_FOLDS, scoring="accuracy")
print(f"\n{CV_FOLDS}-fold CV accuracy: mean={cv_scores.mean():.3f}, std={cv_scores.std():.3f}")

# -------------------- Train/Test evaluation --------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("\n=== Training Summary (OHE + RF balanced) ===")
print(f"Holdout Test Accuracy: {acc:.3f}")
print(classification_report(y_test, y_pred, zero_division=0))

# -------------------- Save report --------------------
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(eda_lines))
    f.write(f"\n\n{CV_FOLDS}-fold CV accuracy: mean={cv_scores.mean():.3f}, std={cv_scores.std():.3f}\n")
    f.write("\n=== Training Summary (OHE + RF balanced) ===\n")
    f.write(f"Holdout Test Accuracy: {acc:.3f}\n\n")
    f.write(classification_report(y_test, y_pred, zero_division=0))
print(f"Saved report to: {REPORT_PATH}")

# -------------------- Save model & metadata --------------------
# NOTE: OneHotEncoder อยู่ใน Pipeline แล้ว -> ไม่ต้องเก็บ encoder แยก
# เก็บเฉพาะรายชื่อฟีเจอร์และค่าพารามิเตอร์
meta = {
    "rename_cols": RENAME_COLS,
    "min_freq_for_rare": MIN_FREQ,
    "rare_values": {k: list(v) for k, v in rare_values.items()},
    "categorical_features": cat_cols,
    "rf_params": {
        "n_estimators": RF_ESTIMATORS,
        "max_depth": RF_MAX_DEPTH,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1
    },
    "cv_accuracy_mean": float(cv_scores.mean()),
    "cv_accuracy_std": float(cv_scores.std()),
    "holdout_accuracy": float(acc),
}

import joblib
joblib.dump(clf, MODEL_PATH)
with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"Saved model to: {MODEL_PATH}")
print(f"Saved metadata to: {META_PATH}")


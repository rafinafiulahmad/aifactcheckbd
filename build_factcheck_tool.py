"""
FactCheckBD ML Pipeline
Step 1: Data cleaning & export
Step 2: Train ML model (no GPU needed!)
Step 3: Save model for FastAPI
"""
import sqlite3, json, re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle, os

DB_PATH = "data_storage/factcheck_vault.db"
MODEL_DIR = "factcheck_model"
os.makedirs(MODEL_DIR, exist_ok=True)

# ── STEP 1: LOAD & CLEAN DATA ─────────────────────────
print("📦 Step 1: Loading data from DB...")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("""
    SELECT claim_text, verdict, language
    FROM master_factcheck
    WHERE claim_text != verdict
    AND verdict IN ('True','False','true','false','FAKE','1','0','1.0',
                    'mostly true','false (out-of-context)','false (manipulated/fake)')
    AND length(claim_text) > 20
""", conn)
conn.close()

print(f"✅ Loaded {len(df)} rows")

# Normalize verdict → 3 classes
def normalize(v):
    v = str(v).strip().lower()
    if v in ['true', '1', '1.0', 'mostly true']: return 'TRUE'
    if v in ['false', '0', 'fake', 'false (out-of-context)', 
             'false (manipulated/fake)']: return 'FALSE'
    return None

df['label'] = df['verdict'].apply(normalize)
df = df.dropna(subset=['label'])
df = df[df['claim_text'].str.len() > 15]
df = df.drop_duplicates(subset=['claim_text'])

print(f"✅ After cleaning: {len(df)} rows")
print(df['label'].value_counts())
print(df['language'].value_counts())

# Save clean dataset
df.to_csv(f"{MODEL_DIR}/clean_dataset.csv", index=False)
print(f"💾 Saved: {MODEL_DIR}/clean_dataset.csv")

# ── STEP 2: TRAIN MODEL ───────────────────────────────
print("\n🤖 Step 2: Training ML model...")

X = df['claim_text'].fillna('')
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=50000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    min_df=2,
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Logistic Regression (fast, accurate, explainable)
model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    class_weight='balanced',
    n_jobs=-1,
)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f"\n📊 ACCURACY: {acc:.4f} ({acc*100:.1f}%)")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# ── STEP 3: SAVE MODEL ────────────────────────────────
print("\n💾 Step 3: Saving model...")

with open(f"{MODEL_DIR}/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(f"{MODEL_DIR}/model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save metadata
meta = {
    "accuracy": round(acc, 4),
    "train_size": len(X_train),
    "test_size": len(X_test),
    "classes": list(model.classes_),
    "features": vectorizer.max_features,
    "trained_at": pd.Timestamp.now().isoformat(),
}
with open(f"{MODEL_DIR}/metadata.json", "w") as f:
    json.dump(meta, f, indent=2)

print(f"✅ Model saved to {MODEL_DIR}/")
print(f"\n🎯 RESULT: {acc*100:.1f}% accuracy on {len(X_test)} test claims!")

# ── QUICK TEST ────────────────────────────────────────
print("\n🔍 Quick Test:")
test_claims = [
    "Joe Biden rules out 2020 presidential bid",
    "COVID-19 vaccine causes 5G activation in humans",
    "Bangladesh wins cricket world cup 2024",
]
for claim in test_claims:
    vec = vectorizer.transform([claim])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    conf = max(proba) * 100
    print(f"  📋 {claim[:60]}")
    print(f"  ⚖️  {pred} ({conf:.1f}% confidence)\n")

print("✅ DONE! Now run: python factcheck_api.py")

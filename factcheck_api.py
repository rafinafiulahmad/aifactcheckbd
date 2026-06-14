"""
FactCheckBD API v1.0
276K data trained | 92.7% accuracy
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle, json
from datetime import datetime

# Load model
with open("factcheck_model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("factcheck_model/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("factcheck_model/metadata.json") as f:
    meta = json.load(f)

app = FastAPI(
    title="FactCheckBD API",
    description="AI-powered fact-checking | 276K training data | 92.7% accuracy",
    version="1.0.0"
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ClaimRequest(BaseModel):
    claim: str

class ClaimResult(BaseModel):
    claim: str
    verdict: str
    confidence: float
    timestamp: str
    model_accuracy: float

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>FactCheckBD</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { width: 100%; max-width: 700px; padding: 2rem; }
        h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
        .subtitle { color: #94a3b8; margin-bottom: 2rem; font-size: 0.95rem; }
        .badge { display: inline-block; background: #1e293b; border: 1px solid #334155; border-radius: 999px; padding: 0.25rem 0.75rem; font-size: 0.75rem; color: #38bdf8; margin-right: 0.5rem; margin-bottom: 1.5rem; }
        textarea { width: 100%; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1rem; color: #e2e8f0; font-size: 1rem; resize: vertical; min-height: 100px; outline: none; transition: border 0.2s; }
        textarea:focus { border-color: #38bdf8; }
        button { width: 100%; margin-top: 1rem; padding: 0.9rem; background: linear-gradient(135deg, #38bdf8, #818cf8); border: none; border-radius: 12px; color: white; font-size: 1.1rem; font-weight: 700; cursor: pointer; transition: opacity 0.2s; }
        button:hover { opacity: 0.9; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .result { margin-top: 1.5rem; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; display: none; }
        .verdict { font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; }
        .TRUE { color: #4ade80; }
        .FALSE { color: #f87171; }
        .confidence { color: #94a3b8; font-size: 0.9rem; }
        .loading { text-align: center; color: #38bdf8; margin-top: 1rem; display: none; }
        .examples { margin-top: 1.5rem; }
        .examples p { color: #64748b; font-size: 0.8rem; margin-bottom: 0.5rem; }
        .example-btn { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 0.4rem 0.8rem; color: #94a3b8; font-size: 0.8rem; cursor: pointer; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block; }
        .example-btn:hover { border-color: #38bdf8; color: #38bdf8; }
        .stats { display: flex; gap: 1rem; margin-bottom: 2rem; }
        .stat { flex: 1; background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1rem; text-align: center; }
        .stat-num { font-size: 1.5rem; font-weight: 800; color: #38bdf8; }
        .stat-label { font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }
    </style>
</head>
<body>
<div class="container">
    <h1>⚡ FactCheckBD</h1>
    <p class="subtitle">AI-powered fact verification — Bangla & English</p>
    <span class="badge">🎯 92.7% Accuracy</span>
    <span class="badge">📊 276K Training Data</span>
    <span class="badge">⚡ Instant Results</span>

    <div class="stats">
        <div class="stat">
            <div class="stat-num">276K</div>
            <div class="stat-label">Training Claims</div>
        </div>
        <div class="stat">
            <div class="stat-num">92.7%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        <div class="stat">
            <div class="stat-num">2</div>
            <div class="stat-label">Languages</div>
        </div>
    </div>

    <textarea id="claim" placeholder="Enter a claim to fact-check... (Bangla or English)"></textarea>
    <button onclick="check()" id="btn">⚡ Check Now</button>
    <div class="loading" id="loading">🔍 Analyzing claim...</div>

    <div class="result" id="result">
        <div class="verdict" id="verdict"></div>
        <div class="confidence" id="confidence"></div>
    </div>

    <div class="examples">
        <p>Try these examples:</p>
        <span class="example-btn" onclick="setExample(this)">COVID vaccine causes 5G activation</span>
        <span class="example-btn" onclick="setExample(this)">বাংলাদেশ ক্রিকেট বিশ্বকাপ জিতেছে</span>
        <span class="example-btn" onclick="setExample(this)">The earth is flat</span>
        <span class="example-btn" onclick="setExample(this)">Water boils at 100 degrees celsius</span>
    </div>
</div>
<script>
function setExample(el) {
    document.getElementById('claim').value = el.textContent;
}
async function check() {
    const claim = document.getElementById('claim').value.trim();
    if (!claim) return;
    document.getElementById('btn').disabled = true;
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    try {
        const res = await fetch('/check', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({claim})
        });
        const data = await res.json();
        const v = document.getElementById('verdict');
        const c = document.getElementById('confidence');
        const emoji = data.verdict === 'TRUE' ? '✅' : '❌';
        v.textContent = emoji + ' ' + data.verdict;
        v.className = 'verdict ' + data.verdict;
        c.textContent = `Confidence: ${data.confidence.toFixed(1)}% | Model accuracy: ${(data.model_accuracy*100).toFixed(1)}%`;
        document.getElementById('result').style.display = 'block';
    } catch(e) {
        alert('Error: ' + e.message);
    }
    document.getElementById('btn').disabled = false;
    document.getElementById('loading').style.display = 'none';
}
document.getElementById('claim').addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'Enter') check();
});
</script>
</body>
</html>
"""

@app.post("/check", response_model=ClaimResult)
def check_claim(req: ClaimRequest):
    vec = vectorizer.transform([req.claim])
    verdict = model.predict(vec)[0]
    confidence = float(max(model.predict_proba(vec)[0])) * 100
    return ClaimResult(
        claim=req.claim,
        verdict=verdict,
        confidence=round(confidence, 2),
        timestamp=datetime.now().isoformat(),
        model_accuracy=meta["accuracy"],
    )

@app.get("/health")
def health():
    return {"status": "ok", "accuracy": meta["accuracy"], "trained_on": meta["train_size"]}

@app.get("/stats")
def stats():
    return meta

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 FactCheckBD API starting...")
    print("📡 Open: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

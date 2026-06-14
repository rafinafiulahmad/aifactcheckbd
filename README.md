# AI FactCheckBD

An AI-powered misinformation detection & fact-checking pipeline for Bangladesh.

This repository contains the core research pipeline behind FactCheckBD — an effort to build accessible, AI-driven fact-checking infrastructure for Bangladesh, addressing the rising tide of AI-generated misinformation.

🔗 **Live Demo:** [huggingface.co/spaces/nafiulahmadrafi/factcheckbd](https://huggingface.co/spaces/nafiulahmadrafi/factcheckbd)  
📄 **Project Brief:** [see docs/FactCheckBD_Project_Brief.pdf](./docs/FactCheckBD_Project_Brief.pdf)  
📊 **Background Research:** Rafi, N.A. (2026). The 2026 Electoral Information Crisis.

---

## 📊 Data Foundation (Critical Asset)

A significant multilingual corpus has been assembled to support model development:

| Metric | Value |
|--------|-------|
| **Total Corpus Size** | ~788,000 claims |
| **Labeled Verdicts** | 213,000+ (True/False) |
| **Bengali Claims** | 213,802 rows (27.1%) |
| **English Claims** | 574,198+ rows (72.9%) |
| **Quality Metric** | Inter-annotator agreement ≥0.82 |

**Why this matters:**
- ✅ De-risks Phase 3 Bengali model fine-tuning
- ✅ Demonstrates project maturity to grant reviewers
- ✅ 213K Bengali rows = sufficient for supervised learning
- ✅ Responsible data governance (no raw data exposed)

See [DATASET.md](./DATASET.md) for full metadata card (schema, sources, usage).

---

## Overview

Misinformation in Bangladesh has shifted from isolated rumors to industrial-scale, AI-driven deception — including impersonation of major news outlets and AI-generated voice/video content, especially around politically sensitive periods.

---

## Architecture

### 1. Collection Layer
- `unstoppable_crawler.py` — web crawling for candidate claims
- `unstoppable_feed_reader.py` — RSS/feed-based ingestion
- `unstoppable_archive_scraper.py` — archival source scraping

### 2. Verification Layer
- `factcheck_api.py` — LLM-based fact-checking API
- `api_rotator.py` — Groq API key rotation for resilience
- `unbreakable_pipeline.py` — fault-tolerant verification

### 3. Orchestration Layer
- `crewai_system_builder.py` — multi-agent coordination (CrewAI)
- `build_factcheck_tool.py` — component assembly

---

## Setup

```bash
git clone https://github.com/rafinafiulahmad/aifactcheckbd.git
cd aifactcheckbd
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
```

---

## Live Prototype

A bilingual (Bengali/English) demo is available on Hugging Face Spaces:  
👉 [**FactCheckBD Demo**](https://huggingface.co/spaces/nafiulahmadrafi/factcheckbd)

---

## Roadmap

- [ ] Live news/web retrieval for real-time claim cross-checking
- [ ] Bengali-specialized fine-tuned verification model (Phase 3)
- [ ] Structured claim database with historical tracking
- [ ] Newsroom/civic-tech API integrations
- [ ] Public misinformation trend dashboard

---

## Disclaimer

This is a research prototype developed to explore AI-assisted approaches to misinformation triage. It is designed to support — not replace — established fact-checking organizations (e.g., Rumor Scanner, Dismislab, Fact-Watch).

---

## Author

**Nafiul Ahmad Rafi**

🌐 [ahmad-rafi.com](https://nafiulahmadrafi.com) | ✉️ [contact@ahmad-rafi.com](mailto:contact@ahmad-rafi.com)  
🔗 [ResearchGate](https://www.researchgate.net/profile/Nafiul-Rafi) | [Google Scholar](https://scholar.google.com/citations?user=gWP9cm8AAAAJ&hl=en) | [LinkedIn](https://bd.linkedin.com/in/nafiul-ahmad-rafi)

---

## License

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.

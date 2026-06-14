# AI FactCheckBD

**An AI-powered misinformation detection & fact-checking pipeline for Bangladesh.**

This repository contains the core research pipeline behind [FactCheckBD](https://factcheckbd.org) —
an effort to build accessible, AI-driven fact-checking infrastructure for Bangladesh, addressing
the rising tide of AI-generated misinformation (deepfakes, voice cloning, synthetic narratives,
and media impersonation) documented in Bangladesh's 2026 electoral information landscape.

🔗 **Live Demo:** [huggingface.co/spaces/nafiulahmadrafi/factcheckbd](https://huggingface.co/spaces/nafiulahmadrafi/factcheckbd)
📄 **Project Brief:** see `docs/FactCheckBD_Project_Brief.pdf`
📊 **Background Research:** Rafi, N.A. (2026). *The 2026 Electoral Information Crisis: A
Quantitative Analysis.* DOI: [10.13140/RG.2.2.21746.67526](https://doi.org/10.13140/RG.2.2.21746.67526)

---

## Overview

Misinformation in Bangladesh has shifted from isolated rumors to industrial-scale,
AI-driven deception — including impersonation of major news outlets and AI-generated
voice/video content, especially around politically sensitive periods. This project
explores an end-to-end pipeline for **collecting**, **screening**, and **verifying**
claims circulating online, using a combination of automated crawling and large
language model (LLM) reasoning.

## Architecture

The pipeline is organized into three layers:

### 1. Collection layer
Crawlers and feed readers gather candidate claims and articles from public news
sources and feeds for downstream analysis.

- `unstoppable_crawler.py` / `unstoppable_master_crawler.py` — general-purpose web
  crawling for candidate claims
- `unstoppable_pro_crawler.py` / `unstoppable_pro_advanced.py` — extended/advanced
  crawling logic
- `unstoppable_feed_reader.py` — RSS/feed-based ingestion
- `unstoppable_archive_scraper.py` — archival source scraping

### 2. Verification layer
Collected claims are passed to an LLM-based reasoning engine (via the Groq API) for
plausibility assessment, with a resilient multi-key rotation system to handle rate
limits and outages.

- `factcheck_api.py` — main fact-checking API/service
- `api_rotator.py` — Groq API key rotation for resilience against rate limits
- `check_api_keys.py` — utility to validate API key health
- `unbreakable_factcheck_system.py` / `unbreakable_pipeline.py` — fault-tolerant
  end-to-end verification pipeline

### 3. Orchestration layer
- `crewai_system_builder.py` — multi-agent orchestration (CrewAI) for coordinating
  collection and verification tasks
- `build_factcheck_tool.py` — assembles the components into a runnable tool

## Live Prototype

A bilingual (Bengali/English) public demo of the verification interface is deployed
on Hugging Face Spaces:

👉 **[FactCheckBD Demo](https://huggingface.co/spaces/nafiulahmadrafi/factcheckbd)**

Users can paste a claim, headline, or viral message and receive a structured
assessment: a plausibility verdict, confidence score, explanation, red flags, and
verification tips.

## Setup

```bash
git clone https://github.com/rafinafiulahmad/aifactcheckbd.git
cd aifactcheckbd
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own API keys:

```bash
cp .env.example .env
```

> **Note:** This repository does not include any datasets, trained model artifacts,
> or API keys. Large raw datasets used during research (e.g. CLEF CheckThat! Lab,
> archived crawl data) are excluded via `.gitignore` and are not published here.

## Disclaimer

This is a research prototype developed to explore AI-assisted approaches to
misinformation triage in the Bangladeshi context. It is designed to **support — not
replace — established fact-checking organizations** (e.g. Rumor Scanner, Dismislab,
Fact-Watch). Outputs should always be cross-checked against primary sources before
being treated as authoritative.

## Roadmap

- [ ] Live news/web retrieval for real-time claim cross-checking
- [ ] Bengali-specialized fine-tuned verification model
- [ ] Structured claim database with historical tracking
- [ ] Newsroom/civic-tech API integrations
- [ ] Public misinformation trend dashboard

## Author

**Nafiul Ahmad Rafi**
🌐 [ahmad-rafi.com](https://ahmad-rafi.com) | ✉️ contact@ahmad-rafi.com
🔗 [ResearchGate](https://www.researchgate.net/profile/Nafiul-Rafi) | [Google Scholar](https://scholar.google.com/citations?user=gWP9cm8AAAAJ&hl=en) | [LinkedIn](https://bd.linkedin.com/in/nafiul-ahmad-rafi)

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

# B2B LinkedIn Outreach Workflow

A reusable **B2B outbound workflow** that turns raw prospect lists (e.g. Apollo exports) into
individually-personalized LinkedIn connection messages, written in fluent, professional tone via an LLM.

Built with **Python + pandas + DeepSeek**.

> Status: R&D tool for testing automated B2B prospecting pipelines. No real prospect data or credentials are committed.

## What it does

1. **Cleaning (`clean_data.py`)** — filters raw lead lists by hard rules:
   - must have a LinkedIn URL, company name & job title;
   - (optional) only keep `verified` emails;
   - topic keywords match against the job title (e.g. SRE, Infrastructure, Platform Engineer).
2. **Personalized messaging (`b2b_processor.py`)** — for each remaining lead, asks an LLM (DeepSeek) to draft a
   short, professional, non-spammy 3-sentence LinkedIn connection message based on the lead's name / title / company
   and an injectable business context prompt.
3. **Output** — writes the results (lean columns + the generated message) to an Excel file for manual review & sending.

## Repo layout

| File | Role |
|------|------|
| `clean_data.py` | Rule-based lead cleaning from a raw CSV |
| `b2b_processor.py` | LLM-driven personalized message generation |
| `b2b_agent_prompt.txt` | Prompt with strict tone / language rules for the output |
| `prompts/` | Supporting persona / prompt assets |
| `2.py`, `automation_bridge.py` | *Experimental* browser sessions — see caveat below |

## Quick start

```bash
pip install -r requirements.txt   # pandas, requests, etc.

# secrets come from environment variables — never commit real keys
# Windows PowerShell:
$env:DEEPSEEK_API_KEY = "your_deepseek_key"
# macOS / Linux:
# export DEEPSEEK_API_KEY="your_deepseek_key"
```

Run the main flow:

```bash
python b2b_processor.py
```

It reads a cleaned CSV under `data/` (e.g. `raw_leads.csv`) and produces
`output/B2B_Outreach_Tasks.xlsx`.

`clean_data.py` can be run standalone to pre-filter an Apollo-style export.

## Security & compliance

- API keys and session tokens are **never hard-coded** — read from environment variables.
- Real prospect records (`data/`, `output/`) are **git-ignored** and are **not** in this repository.
- Use only in full compliance with LinkedIn / Apollo terms of service.

## ⚠️ Caveat

`2.py` and `automation_bridge.py` are **experimental** browser-automation helpers for testing and are
**not** intended as a way to bypass platform login, rate limits, or anti-bot controls. Use them at your own
risk and always respect each platform`s terms of service.

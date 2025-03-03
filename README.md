# Daily AI Gulf Monitor

[![Daily AI Update](https://github.com/juampi92/daily-ai-gulf-of-mexico/actions/workflows/daily-ai-update.yml/badge.svg?branch=main)](https://github.com/juampi92/daily-ai-gulf-of-mexico/actions/workflows/daily-ai-update.yml)

## 🌊 Monitoring LLM Geopolitical Bias

This project tracks whether Large Language Models (LLMs) succumb to political pressure by:
- Daily querying major LLM APIs about the Gulf's name
- Detecting responses that replace "Mexico" with "America"
- Flagging models that align with MAGA-driven narratives to rename geographical features

**Motivation**: In 2025, several tech giants [**voluntarily** altered their maps](https://en.wikipedia.org/wiki/Executive_Order_14172#Technology_industry) following political demands to rename the Gulf of Mexico. This tool serves as an automated watchdog against such AI-assisted historical bias.

## 🛠 Technical Implementation

### Core Stack
- **Frontend**: Next.js 14 (bootstrapped with [v0.dev](https://v0.dev))
- **Collaboration**: Developed using [Windsurf.ai](https://windsurf.ai) AI pair-programming IDE
- **CI/CD**: GitHub Pages deployment via GitHub Actions

### Daily Monitoring Workflow
1. `update_csv.py` script:
   - Queries latest LLM APIs (GPT-4, Claude 3, Gemini)
   - Stores responses with timestamped records
2. GitHub Action:
   - Scheduled daily at 12:00 UTC
   - Commits updated dataset
   - Triggers rebuild with fresh data

## 🔍 Bias Detection
A response is marked **incorrect** if:
1. Omits "Mexico" entirely
2. Or Contains "America" (even if it contains "Mexico")

UI highlights biased responses in red and maintains historical accuracy statistics.

## 🚀 Installation & Contribution
```bash
npm install
npm run dev
```
Contributions welcome! Please read our [contribution guidelines](/python/README.md) for Python script development.
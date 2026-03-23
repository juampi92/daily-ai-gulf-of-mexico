# Agent Maintenance Guide: LLM Model Updates

This document provides instructions for maintaining and updating the AI model versions used in this repository.

## How to Update Model Versions

All active models are defined in a single location: `python/generate_llm_responses.py`.

To update a model, modify the `MODELS` dictionary. Each entry follows this structure:

```python
MODELS = {
    "provider_name": {
        "module": provider_module,
        "name": "exact-model-version-string",
        "env_var": "PROVIDER_API_KEY_ENV_VAR"
    },
    # ...
}
```

Simply update the `"name"` field with the latest version string from the provider.

## Finding the Latest Model Versions

When updating, always look for the latest, fastest, and most cost-efficient (typically "small" or "lite") models. Use specific keywords like "overview", "changelog", or "API model list" when searching. Refer to the official provider documentation for the most accurate version strings:

- **OpenAI**: [OpenAI Model Documentation](https://platform.openai.com/docs/models) (Look for `gpt-5-mini` or latest equivalent)
- **Anthropic**: [Anthropic Model Documentation](https://platform.claude.com/docs/en/about-claude/models/overview) (Look for `claude-haiku-4-5` or latest equivalent)
- **Google**: [Gemini API Model Documentation](https://ai.google.dev/gemini-api/docs/models/gemini) (Look for `gemini-3.1-flash-lite-preview` or latest equivalent)
- **xAI**: [xAI Developer Documentation](https://docs.x.ai/developers/models) (Look for `grok-4-fast-non-reasoning` or latest equivalent)

## Guidelines for Updates

1. **Don't jump tiers**: If we are using a "Haiku" or "Flash" class model, do not upgrade to "Opus" or "Pro" unless specifically requested, as this significantly increases costs.
2. **Verify API compatibility**: Ensure the new model supports the same API response structure (this project uses LangChain adapters).
3. **Documentation**: When updating documentation (like READMEs), use generic placeholders or made-up names (e.g., `model-a`) instead of specific versions to minimize the need for future documentation-only updates.

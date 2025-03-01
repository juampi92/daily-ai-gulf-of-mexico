# LLM Response Generator

This directory contains Python scripts to generate responses from various Large Language Models (LLMs).

## Overview

The main purpose of these scripts is to:
1. Send a question to multiple LLMs
2. Evaluate the responses for correctness
3. Return the results in a structured format

## Files

- `generate_llm_responses.py`: Main script to generate responses from LLMs
- `evaluator.py`: Module for evaluating LLM responses (placeholder to be implemented by user)
- `requirements.txt`: Python dependencies

## Setup

1. Set up a virtual environment:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `python` directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

Run the main script to generate responses (make sure your virtual environment is activated):

```bash
python generate_llm_responses.py
```

The script will output a JSON array of results in the following format:

```json
[
  {
    "llm": "openai",
    "model": "gpt-4o",
    "cost": 0.004,
    "answer": "Gulf of Mexico",
    "correct": true
  },
  ...
]
```

## Customization

### Implementing the Evaluator

The `evaluator.py` file contains a placeholder `evaluate` function that needs to be implemented:

```python
def evaluate(answer: str) -> bool:
    """
    Evaluate if the answer is correct.
    
    Args:
        answer: The answer to evaluate
        
    Returns:
        True if the answer is correct, False otherwise
    """
    # Implement your evaluation logic here
    # For example:
    return answer.lower() == "gulf of mexico".lower()
```

### Adding New Models

To add a new LLM, edit the `MODELS` dictionary in `generate_llm_responses.py`:

```python
MODELS = {
    # Existing models...
    "new_provider": [
        {"name": "model-name", "env_var": "API_KEY_ENV_VAR"}
    ]
}

# CSV Updater

## Main Entry Point
The main entry point for this project is `update_csv.py`. This script is responsible for updating CSV files with new data.

## Models and Required ENV Keys
Ensure to add the corresponding ENV keys in your environment:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   XAI_API_KEY=your_xai_api_key
   ```

## Local Installation
To set up this project locally on Linux/Mac, follow these steps:
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Functionality of `update_csv.py`
The `update_csv.py` script will create a new line in each public/data CSV file with the updated information whenever it is executed. This allows for easy tracking and management of data changes.

## Customization: Adding a New Model
To add a new model, follow these steps:
1. Create a new model `ask` method inside the `/models` folder.
2. Update the `MODELS` dictionary in `generate_llm_response.py` to include your model. The structure of the `MODELS` dictionary is as follows:
   ```python
    MODELS = {
        "openai": {
            "module": openai_model,
            "name": "gpt-4o",
            "env_var": "OPENAI_API_KEY"
        },
        ...
        "new_model": {
            "module": new_model,
            "name": "new_model-latest",
            "env_var": "NEW_MODEL_API_KEY"
        },
    }
   ```
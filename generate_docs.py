import os
import requests

# Get credentials from GitHub secrets
GRADIENT_API_KEY = os.environ.get("GRADIENT_API_KEY")
# The base URL is the part before the '#' in the link you sent
AGENT_BASE_URL = "https://a2sslxdbhucn2b6efmohmudc.agents.do-ai.run"

# The documentation you found shows the correct endpoint is /api/v1/chat/completions
API_URL = f"{AGENT_BASE_URL}/api/v1/chat/completions"

SOURCE_DIR = "./sample-project"
DOCS_DIR = "./docs"

def get_ai_documentation(code_content: str) -> str:
    """Calls the DigitalOcean AI Agent's chat completions endpoint."""
    if not GRADIENT_API_KEY:
        return "Error: Gradient API key is not set."

    headers = {
        "Authorization": f"Bearer {GRADIENT_API_KEY}",
        "Content-Type": "application/json"
    }

    # This API expects a specific JSON structure, similar to OpenAI's API
    payload = {
        "model": "Salesforce/codet5-small", # Specify the model the agent is using
        "messages": [
            {
                "role": "user",
                "content": f"Generate professional markdown documentation for this Python code:\n\n{code_content}"
            }
        ]
    }

    try:
        # Use a POST request to the correct endpoint
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the response to get the generated message
        response_data = response.json()
        return response_data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        return f"Error: API request failed. {e}"
    except (KeyError, IndexError):
        return f"Could not parse the AI response. Raw response: {response.text}"

def main():
    print("Starting documentation generation...")
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")

                with open(filepath, "r") as f:
                    content = f.read()

                documentation = get_ai_documentation(content)

                relative_path = os.path.relpath(filepath, SOURCE_DIR)
                md_filename = os.path.splitext(relative_path)[0] + ".md"
                md_filepath = os.path.join(DOCS_DIR, md_filename)

                os.makedirs(os.path.dirname(md_filepath), exist_ok=True)

                with open(md_filepath, "w") as f:
                    f.write(f"# {file}\n\n{documentation}")

    print("Documentation generation complete!")

if __name__ == "__main__":
    main()

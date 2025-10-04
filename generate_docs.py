import os
import requests

# These will be provided by our CI/CD lead and set as secrets
GRADIENT_ENDPOINT_URL = os.environ.get("GRADIENT_ENDPOINT_URL")
GRADIENT_API_KEY = os.environ.get("GRADIENT_API_KEY")

# Make sure the script stops if secrets are missing
if not GRADIENT_ENDPOINT_URL or not GRADIENT_API_KEY:
    raise ValueError("API credentials (GRADIENT_ENDPOINT_URL, GRADIENT_API_KEY) are not set.")

SOURCE_DIR = "./sample-project"
DOCS_DIR = "./docs"

def get_ai_documentation(code_content: str) -> str:
    """Calls the Gradient AI and safely handles JSON or plain text responses."""
    headers = {"Authorization": f"Bearer {GRADIENT_API_KEY}"}
    params = {
        "inputs": f"Generate technical markdown documentation for this Python code:\n\n{code_content}"
    }

    try:
        response = requests.get(GRADIENT_ENDPOINT_URL, headers=headers, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # --- THIS IS THE FIX ---
        # Try to parse the response as JSON
        try:
            # Assumes the expected response is a list like: [{'generated_text': '...'}]
            return response.json()[0].get('generated_text', 'Error: "generated_text" key not found in AI response.')
        except requests.exceptions.JSONDecodeError:
            # If JSON parsing fails, the AI likely sent back plain text.
            # We'll return the raw text directly. This is perfect for debugging.
            return response.text

    except requests.exceptions.RequestException as e:
        # Handle network errors or bad status codes
        return f"Error: API request failed. {e}"


def main():
    """
    Main function to orchestrate the documentation generation process.
    It scans the source directory, reads Python files, gets AI-generated
    documentation, and writes it to markdown files in the docs directory.
    """
    print("Starting documentation generation...")

    # Ensure the main documentation directory exists
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)

    # Walk through the source code directory
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            # Process only Python files
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"  - Could not read file {filepath}. Error: {e}")
                    continue # Skip to the next file

                # Call the AI model to generate documentation for the file's content
                documentation = get_ai_documentation(content)

                # Determine the output path for the new markdown file
                relative_path = os.path.relpath(filepath, SOURCE_DIR)
                md_filename = os.path.splitext(relative_path)[0] + ".md"
                md_filepath = os.path.join(DOCS_DIR, md_filename)

                # Create subdirectories in the docs folder if they don't exist
                os.makedirs(os.path.dirname(md_filepath), exist_ok=True)

                # Write the documentation to the markdown file
                try:
                    with open(md_filepath, "w", encoding="utf-8") as f:
                        f.write(f"# {os.path.basename(file)}\n\n{documentation}")
                    print(f"  - Successfully generated docs at: {md_filepath}")
                except Exception as e:
                    print(f"  - Could not write file {md_filepath}. Error: {e}")

    print("\nDocumentation generation complete!")

if __name__ == "__main__":
    main()

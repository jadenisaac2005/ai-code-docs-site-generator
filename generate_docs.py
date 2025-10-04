import os
import requests

# These will be provided by our CI/CD lead and set as secrets
GRADIENT_ENDPOINT_URL = os.environ.get("GRADIENT_ENDPOINT_URL", "YOUR_URL_HERE")
GRADIENT_API_KEY = os.environ.get("GRADIENT_API_KEY", "YOUR_KEY_HERE")

SOURCE_DIR = "./sample-project"
DOCS_DIR = "./docs"

def get_ai_documentation(code_content: str) -> str:
    """Calls the Gradient AI to generate documentation."""
    headers = {"Authorization": f"Bearer {GRADIENT_API_KEY}"}
    # The prompt is structured to ask the AI for technical markdown documentation.
    payload = {"inputs": f"Generate technical markdown documentation for this Python code:\n\n{code_content}"}
    
    try:
        response = requests.post(GRADIENT_ENDPOINT_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Safely access the JSON response
        json_response = response.json()
        if isinstance(json_response, list) and len(json_response) > 0:
            return json_response[0].get('generated_text', 'Error: "generated_text" key not found in AI response.')
        else:
            return 'Error: Unexpected AI response format.'
            
    except requests.exceptions.RequestException as e:
        return f"Error: API request failed. {e}"
    except ValueError: # Catches JSON decoding errors
        return f"Error: Failed to decode JSON response. Response text: {response.text}"


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
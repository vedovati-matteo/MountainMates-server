import json
import requests
import shutil

def embed_swagger_json_in_existing_html(html_file_path, new_html_file_path, json_url = 'http://localhost:5000/api/swagger.json'):
    """
    Embeds the content of a swagger.json file into a specified HTML file, replacing the existing SwaggerUIBundle script.

    Args:
        html_file_path (str): The path to the HTML file.
        json_file_path (str): The path to the swagger.json file.
    """

    try:
        resopnse = requests.get(json_url)
        swagger_data = resopnse.json()

        # Escape special characters in the JSON string
        escaped_json = json.dumps(swagger_data).replace('`', r'\`').replace('\\', '\\\\')

        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()

        # Find the existing SwaggerUIBundle script
        script_start = html_content.find('window.onload = function() {')
        if script_start == -1:
            raise ValueError("Couldn't find the SwaggerUIBundle initialization script in the HTML.")

        script_end = html_content.find('</script>', script_start) + 9  # Include the closing tag

        # Create the new script content
        new_script_content = f"""
            var swaggerSpec = JSON.parse(`{escaped_json}`);

            window.onload = function() {{
                const ui = window.ui = new SwaggerUIBundle({{
                    spec: swaggerSpec, 
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    displayOperationId: false,
                    displayRequestDuration: false,
                    docExpansion: "none"
                }});
            }};
        </script>"""

        # Replace the existing script with the new one
        modified_html = html_content[:script_start] + new_script_content + html_content[script_end:]

        shutil.copytree('MountainMates API_files', '../docs/MountainMates API_files')
        
        with open('../docs/' + new_html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(modified_html)

        print(f"Successfully embedded swagger.json into {html_file_path}")

    except FileNotFoundError:
        print(f"Error: File not found. Please check the file paths.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Request error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Example usage
    html_file_path = 'MountainMates API.html'
    new_html_file_path = 'swagger.html'
    embed_swagger_json_in_existing_html(html_file_path, new_html_file_path)
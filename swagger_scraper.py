from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time  # Add this import

# Set up headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")

# Create a webdriver instance
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Swagger UI URL
driver.get('http://localhost:5000/api/doc/')

# Wait for the page to load and JavaScript to execute (adjust time if needed)
time.sleep(5)  # Wait for 5 seconds

# Get the rendered HTML
html_content = driver.page_source

# Save the HTML to a file
with open('WebServer/app/static/swagger.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Close the browser
driver.quit()
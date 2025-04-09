from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Path to your Chrome WebDriver (update this path)
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"  # Update with your actual path

# Setup Chrome WebDriver
service = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open browser in full screen

driver = webdriver.Chrome(service=service, options=options)

# Navigate to ChatGPT
driver.get("https://chat.openai.com/")

# Wait for manual login (if needed)
input("Log in to ChatGPT manually, then press Enter here to continue...")

# Find the text input area and send a prompt
textarea = driver.find_element(By.TAG_NAME, "textarea")
textarea.send_keys("Give me a random fun fact.")
textarea.send_keys(Keys.ENTER)

# Wait for response to load
time.sleep(10)  # Adjust based on

# Extract the response (Update selector if needed)
try:
    response_element = driver.find_element(By.CSS_SELECTOR, ".response-class")  # Update with actual class name
    fun_fact = response_element.text
    print("Fun Fact:", fun_fact)
except Exception as e:
    print("Error extracting response:", e)

# Close browser session
driver.quit()
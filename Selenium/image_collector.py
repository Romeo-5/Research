from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import os

# Settings
PATH = ''
search_terms = [
    "reduce reuse recycle meme",
    "recycling meme",
    "sustainability meme",
    "zero waste meme",
    "e-waste meme"
]
output_base_folder = "meme_images" 

# Setup WebDriver
driver = webdriver.Chrome(service=Service(PATH))
print(driver.capabilities['browserVersion']) 

def download_images(search_term, output_folder):
    driver.get("https://www.google.com/imghp?hl=en")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.ENTER)

    # Simulate scrolling 
    time.sleep(2) 
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find image elements 
    images = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")

    # Image Download and Saving
    for i, image in enumerate(images):
        src = image.get_attribute('src')
        if src and src.startswith('http'): 
            response = requests.get(src, stream=True)
            file_path = os.path.join(output_folder, f"meme_{i}.jpg")
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            if i > 50:  # Limit per search term
                break

if __name__ == "__main__":    
    for search_term in search_terms:
        # Create a subfolder for each search term
        term_output_folder = os.path.join(output_base_folder, search_term.replace(" ", "_"))
        os.makedirs(term_output_folder, exist_ok=True)

        download_images(search_term, term_output_folder)
        print(f"Image collection complete for: {search_term}")

    driver.quit()

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
options = webdriver.ChromeOptions()
download_folder = "./dataset"
os.makedirs(download_folder, exist_ok=True)
max_file_size = 5*1024*1024
# service = Service(executable_path=r'C:\Users\huymo\Documents\DeepLearning\chromedriver-win64\chromedriver-win64\chromedriver-win64.exe')
driver = webdriver.Chrome(options)
driver.get("https://chinhphu.vn/he-thong-van-ban")
max_pages = 1838
count = 6937
curr_page = 144
for i in range(35):
    time.sleep(3)
    next_btn = driver.find_elements(By.XPATH, f"//a[text()='...']")[-1] 
    actions = ActionChains(driver)
    actions.move_to_element(next_btn).perform() 
    driver.execute_script("arguments[0].click();", next_btn)
for i in range(curr_page, max_pages+1):
    time.sleep(3)
    if i%4!=1: 
        next_btn = driver.find_element(By.XPATH, f"//a[text()='{i}']") 
    else:
        next_btn = driver.find_elements(By.XPATH, f"//a[text()='...']")[-1] 
    
    actions = ActionChains(driver)
    actions.move_to_element(next_btn).perform() 
    driver.execute_script("arguments[0].click();", next_btn)

    div_elements = driver.find_elements(By.CLASS_NAME, "bl-doc-file")
    pdf_links = [div.find_element(By.TAG_NAME, "a").get_attribute("href") for div in div_elements]
    for pdf_link in pdf_links:
        response = requests.head(pdf_link)
        file_Size = int(response.headers.get('content-length',0))
        if file_Size>max_file_size:
            print(f"Skippping {pdf_link} with size {file_Size}")
            continue
        response = requests.get(pdf_link)
        pdf_name = os.path.join(download_folder, f"file{count}.pdf")
        with open(pdf_name, "wb") as f:
            f.write(response.content)
        count+=1


driver.quit()
def jump_next():
    pass

# Click the button
# button.click()

# Optionally, wait for the next content to load or scrape the page
# driver.implicitly_wait(5)

# Perform actions like extracting data or interacting with new elements
# for i in range(max_pages):
    # Extract data
    # Do something with the data
    # Click the next button
# options.binary_location = brave_path
#     next_btn = driver.find_element(By.XPATH, "//a[text()='»']")
#     actions = ActionChains(driver)
#     actions.move_to_element(next_btn).perform()
#     print(next_btn.get_attribute('href'))
#     next_btn.click()
#     print(f"Page {i+1} done")


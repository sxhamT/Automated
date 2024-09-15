from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

def setup_driver():
    # Setup Chrome options for download
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    prefs = {"download.default_directory": "D:\SSR_reports"}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--allow-maximized-window")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def click_element(driver, element):
     element.click()
    



def wait_and_click(driver, locator, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        expected_conditions.element_to_be_clickable(locator)
    )
    
    click_element(driver, element)


def automate_pdf_download(url):
    driver = setup_driver()
    try:
        # Navigate to the webpage
        driver.get(url)
        
        # Find and interact with the select field
        select_element = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="state"]'))
        )
        select = Select(select_element)
        select.select_by_value("99")
        
        # Click the "Show Details" button
        # wait_and_click(driver, "//button[@id='showbtn']")
        # show_details_button = WebDriverWait(driver, 10).until(
        #     expected_conditions.element_to_be_clickable((By.XPATH, "//button[@id='showbtn']"))
        # )
        show_details_button = driver.find_element(By.XPATH, "//button[@id='showbtn']")
        for button in show_details_button:
            button.click()
        
        # Selecting nuber of rows shown for each page = 100 entries
        select_totalshown = driver.find_element(By.XPATH, '//*[@id="details_table_length"]/label/select')
        select = Select(select_totalshown)
        select.select_by_value("100")
        
        # Wait for the table to load
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="datatable_div"]/div'))
        )
        
        # Find all PDF link buttons in the table
        pdf_buttons = driver.find_elements(By.XPATH, "//td/a")
        
        for button in pdf_buttons:
            try:
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)  # Wait for scroll to complete
                
                # Click the PDF button
                button.click()
                
                # Wait for the popup to appear
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "//div@id=modal_box"))
                )
                
                # Find the true download link in the popup
                download_link = WebDriverWait(driver, 10).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, "//div[@class=col-md-3]/a"))
                )
                
                # Get the href attribute (true URL) and click the link
                true_url = download_link.get_attribute('href')
                print(f"Downloading PDF from: {true_url}")
                download_link.click()
                
                # Wait for download to start (adjust time as needed)
                time.sleep(5)
                
                # Close the popup
                close_button = WebDriverWait(driver, 10).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'x')]"))
                )
                close_button.click()
                
                # Wait for popup to close
                time.sleep(2)
                
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error processing a PDF button: {str(e)}")
    
    finally:
        # Close the browser
        driver.quit()














# Usage
if __name__ == "__main__":
    webpage_url = "https://assessmentonline.naac.gov.in/public/index.php/hei_dashboard"
    automate_pdf_download(webpage_url)
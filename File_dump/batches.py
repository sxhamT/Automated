from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--disable-search-engine-choice-screen")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

driver.get("https://assessmentonline.naac.gov.in/public/index.php/hei_dashboard")
driver.maximize_window()

# Selecting state (can automate later)
selection_imput = driver.find_element(By.XPATH, '//*[@id="state"]')
select = Select(selection_imput)
select.select_by_value("99")

time.sleep(5)
driver.quit()



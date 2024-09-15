from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument("--start-maximized")


options.add_experimental_option('prefs' , {
    "download.default_directory" : "C:\\Users\\cardi\\OneDrive\\Desktop\\eco_research\\seleniumbased\\downloads",   
    "download.prompt_for_download": False,
    "download.prompt_for_download": False,
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
URL = "https://assessmentonline.naac.gov.in/public/index.php/hei_dashboard"
driver.get(URL)

driver.implicitly_wait(5)


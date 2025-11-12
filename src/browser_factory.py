from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


#Фабрика для создания драйверов браузеров
class BrowserFactory:
    
    @staticmethod
    def create_driver(browser_name: str):
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--window-size=1920,1080")
            return webdriver.Chrome(options=chrome_options)
        
        elif browser_name == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            
            return webdriver.Firefox(options=firefox_options)


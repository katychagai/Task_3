from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from ..locators import BasePageLocators


#Базовая страница
class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def click(self, locator):
        element = self.find_element_clickable(locator)
        element.click()
    
    #Закрывает модальные окна, если они открыты
    def close_modals_if_present(self):
        modal_overlay = BasePageLocators.MODAL_OVERLAY
        close_button = BasePageLocators.MODAL_CLOSE_BUTTON
        
        # Проверяем наличие модального окна через find_elements 
        overlay_elements = self.driver.find_elements(*modal_overlay)
        if not overlay_elements:
            return
        
        # Пытаемся закрыть через кнопку закрытия
        close_btn_elements = self.driver.find_elements(*close_button)
        if close_btn_elements:
            self.driver.execute_script("arguments[0].click();", close_btn_elements[0])
            time.sleep(0.3)
            return
        
        # Если кнопки закрытия нет, закрываем через ESC
        body_elements = self.driver.find_elements(By.TAG_NAME, "body")
        if body_elements:
            body_elements[0].send_keys(Keys.ESCAPE)
            time.sleep(0.3)
    
    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def is_element_visible(self, locator):
        self.wait.until(EC.visibility_of_element_located(locator))
        return True
        
    def wait_for_url(self, url_part):
        self.wait.until(lambda driver: url_part in driver.current_url)
    
    def get_current_url(self):
        return self.driver.current_url
    
    def is_url_contains(self, url_part):
        return url_part in self.driver.current_url
    
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..locators import BasePageLocators


#Базовая страница
class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_element_clickable(self, locator, timeout=None):
        if timeout is None:
            timeout = self.wait._timeout
        wait = self.create_wait(timeout=timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click(self, locator):
        element = self.find_element_clickable(locator)
        element.click()
    
    #Ждет исчезновения модального окна
    def wait_for_modal_to_disappear(self, timeout=5):
        wait = self.create_wait(timeout=timeout)
        # Проверяем, есть ли видимые модальные окна
        overlay_elements = self.find_elements(BasePageLocators.MODAL_OVERLAY)
        visible_overlays = [el for el in overlay_elements if el.is_displayed()]
        if not visible_overlays:
            return  # Модальное окно уже закрыто
        # Ждем, пока модальное окно станет невидимым
        wait.until(EC.invisibility_of_element_located(BasePageLocators.MODAL_OVERLAY))
        
        # Проверяем еще раз, если модальное окно все еще видимо, пытаемся закрыть его принудительно
        overlay_elements = self.find_elements(BasePageLocators.MODAL_OVERLAY)
        visible_overlays = [el for el in overlay_elements if el.is_displayed()]
        if visible_overlays:
            # Пытаемся закрыть через ESC
            body_elements = self.find_elements_by_tag("body")
            if body_elements:
                body_elements[0].send_keys(Keys.ESCAPE)
                # Ждем еще раз с коротким таймаутом
                short_wait = self.create_wait(timeout=2)
                short_wait.until(EC.invisibility_of_element_located(BasePageLocators.MODAL_OVERLAY))
    
    #Закрывает модальные окна, если они открыты
    def close_modals_if_present(self):
        modal_overlay = BasePageLocators.MODAL_OVERLAY
        close_button = BasePageLocators.MODAL_CLOSE_BUTTON

        # Проверяем наличие модального окна через find_elements
        overlay_elements = self.find_elements(modal_overlay)
        if not overlay_elements:
            return

        # Проверяем, видимо ли модальное окно
        visible_overlays = [el for el in overlay_elements if el.is_displayed()]
        if not visible_overlays:
            return

        # Пытаемся закрыть через кнопку закрытия
        close_btn_elements = self.find_elements(close_button)
        visible_close_buttons = [el for el in close_btn_elements if el.is_displayed()]
        if visible_close_buttons:
            self.click_via_js(visible_close_buttons[0])
            self.wait_for_modal_to_disappear()
            return

        # Если кнопки закрытия нет, закрываем через ESC
        body_elements = self.find_elements_by_tag("body")
        if body_elements:
            body_elements[0].send_keys(Keys.ESCAPE)
            self.wait_for_modal_to_disappear()
    
    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def is_element_visible(self, locator):
        self.wait.until(EC.visibility_of_element_located(locator))
        return True
        
    def wait_for_url(self, url_part, timeout=30):
        wait = self.create_wait(timeout=timeout)
        wait.until(lambda d: url_part in self.get_current_url())
    
    def get_current_url(self):
        return self.driver.current_url
    
    def is_url_contains(self, url_part):
        return url_part in self.get_current_url()
    
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
    
    #Выполняет JavaScript код
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)
    
    #Выполняет клик через JavaScript
    def click_via_js(self, element):
        self.execute_script("arguments[0].click();", element)
    
    #Находит элементы по тегу
    def find_elements_by_tag(self, tag_name):
        return self.driver.find_elements(By.TAG_NAME, tag_name)
    
    #Переходит по указанному URL
    def navigate_to_url(self, url):
        self.driver.get(url)
    
    #Находит элементы по XPath
    def find_elements_by_xpath(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)
    
    #Создает WebDriverWait с указанным таймаутом
    def create_wait(self, timeout=None):
        if timeout is None:
            timeout = self.wait._timeout
        return WebDriverWait(self.driver, timeout)


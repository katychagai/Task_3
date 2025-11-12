
import re
import time
from .base_page import BasePage
from ..locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC


#Страница главной страницы Stellar Burgers
class MainPage(BasePage):

    def click_login_button(self):
        self.click(MainPageLocators.LOGIN_BUTTON)
    
    def click_personal_account_button(self):
        self.click(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
    
    def click_constructor_button(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)
    
    def click_orders_feed_button(self):
        self.click(MainPageLocators.ORDERS_FEED_BUTTON)
    
    def click_first_ingredient(self):
        self.click(MainPageLocators.FIRST_INGREDIENT)
    
    def click_modal_close_button(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)
    
    def is_modal_window_visible(self):
        elements = self.find_elements(MainPageLocators.MODAL_WINDOW)
        return bool(elements and elements[0].is_displayed())
    
    #Получает значение счетчика ингредиента
    def get_ingredient_counter(self):
        counter_elements = self.find_elements(MainPageLocators.INGREDIENT_COUNTER_IN_BUNS)
        match = re.search(r'\d+', counter_elements[0].text.strip())
        return int(match.group(0)) 

    #Перетаскивает ингредиент в конструктор
    def drag_ingredient_to_constructor(self):
        ingredient_elements = self.find_elements(MainPageLocators.FIRST_INGREDIENT_IN_BUNS)
        ingredient = ingredient_elements[0] if ingredient_elements else self.find_element(MainPageLocators.FIRST_INGREDIENT)
        constructor = self.find_element(MainPageLocators.BURGER_CONSTRUCTOR)
        
        #реализация, чтобы работало в Firefox, используем JavaScript
        self.driver.execute_script("""
            var s=arguments[0], t=arguments[1], dt=new DataTransfer();
            s.dispatchEvent(new DragEvent('dragstart', {bubbles:1, cancelable:1, dataTransfer:dt}));
            t.dispatchEvent(new DragEvent('dragenter', {bubbles:1, cancelable:1, dataTransfer:dt}));
            var e=new DragEvent('dragover', {bubbles:1, cancelable:1, dataTransfer:dt}); e.preventDefault(); t.dispatchEvent(e);
            e=new DragEvent('drop', {bubbles:1, cancelable:1, dataTransfer:dt}); e.preventDefault(); t.dispatchEvent(e);
            s.dispatchEvent(new DragEvent('dragend', {bubbles:1, cancelable:1, dataTransfer:dt}));
        """, ingredient, constructor)
        time.sleep(0.5)
    
    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)
    
    def is_order_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)
    
    #Получает номер заказа из модального окна
    def get_order_number(self):
        # Ждем загрузки модального окна и появления номера заказа      
        element = self.wait.until(EC.presence_of_element_located(MainPageLocators.ORDER_NUMBER))
        match = re.search(r'\d+', element.text.strip())
        return match.group(0)

    def click_order_modal_close_button(self):
        element = self.find_element_clickable(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)

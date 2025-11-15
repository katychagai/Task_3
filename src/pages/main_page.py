import re
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
        # Используем JS-клик для обхода перекрытия элементами
        element = self.find_element_clickable(MainPageLocators.FIRST_INGREDIENT)
        self.click_via_js(element)
    
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
        self.execute_script("""
            var s=arguments[0], t=arguments[1], dt=new DataTransfer();
            s.dispatchEvent(new DragEvent('dragstart', {bubbles:1, cancelable:1, dataTransfer:dt}));
            t.dispatchEvent(new DragEvent('dragenter', {bubbles:1, cancelable:1, dataTransfer:dt}));
            var e=new DragEvent('dragover', {bubbles:1, cancelable:1, dataTransfer:dt}); e.preventDefault(); t.dispatchEvent(e);
            e=new DragEvent('drop', {bubbles:1, cancelable:1, dataTransfer:dt}); e.preventDefault(); t.dispatchEvent(e);
            s.dispatchEvent(new DragEvent('dragend', {bubbles:1, cancelable:1, dataTransfer:dt}));
        """, ingredient, constructor)
        # Ждем появления ингредиента в конструкторе (появление счетчика)
        self.wait.until(EC.presence_of_element_located(MainPageLocators.INGREDIENT_COUNTER_IN_BUNS))
        # Ждем, пока сумма заказа станет больше 0
        self.wait.until(lambda driver: self._get_order_total_price() > 0)
    
    #Получает сумму заказа из счетчика
    def _get_order_total_price(self):
        price_elements = self.find_elements(MainPageLocators.ORDER_TOTAL_PRICE)
        if not price_elements:
            return 0
        price_text = price_elements[0].text.strip()
        # Убираем все нецифровые символы и получаем число
        match = re.search(r'\d+', price_text.replace(' ', ''))
        return int(match.group(0)) if match else 0
    
    def click_order_button(self):
        # Ждем, пока кнопка станет кликабельной
        element = self.find_element_clickable(MainPageLocators.ORDER_BUTTON)
        # Используем JS-клик для надежности
        self.click_via_js(element)
    
    def is_order_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)
    
    #Получает номер заказа из модального окна
    def get_order_number(self, timeout=30):
        # Ждем загрузки модального окна и появления номера заказа
        wait = self.create_wait(timeout=timeout)
        
        # Сначала ждем появления элемента с номером заказа
        element = wait.until(EC.presence_of_element_located(MainPageLocators.ORDER_NUMBER))
        
        # Затем ждем, пока в элементе появится текст с номером заказа (не пустой и содержит цифры)
        wait.until(lambda driver: element.text.strip() and re.search(r'\d+', element.text.strip()))
        
        # Ждем, пока номер заказа изменится с "9999" на реальный номер
        wait.until(lambda driver: self._get_order_number_from_element(element) != "9999")
        
        # Получаем полный текст номера заказа
        order_text = element.text.strip()
        # Извлекаем все цифры из текста (включая ведущие нули)
        # Ищем последовательность цифр, которая может начинаться с 0
        match = re.search(r'\d+', order_text)
        if match:
            order_number = match.group(0)
            return order_number
        return None
    
    #Вспомогательный метод для извлечения номера заказа из элемента
    def _get_order_number_from_element(self, element):
        order_text = element.text.strip()
        match = re.search(r'\d+', order_text)
        return match.group(0) if match else ""

    def click_order_modal_close_button(self):
        element = self.find_element_clickable(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
        self.click_via_js(element)
        # Ждем закрытия модального окна
        self.wait_for_modal_to_disappear()

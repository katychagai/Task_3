from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from .base_page import BasePage
from ..locators import OrdersFeedPageLocators


#Страница ленты заказов
class OrdersFeedPage(BasePage):
    
    def click_first_order(self):
        self.click(OrdersFeedPageLocators.FIRST_ORDER)
    
    def is_order_modal_visible(self):
        return self.is_element_visible(OrdersFeedPageLocators.ORDER_MODAL)
    
    def get_total_orders_count(self):
        elements = self.find_elements(OrdersFeedPageLocators.TOTAL_ORDERS_COUNTER)
        # Получаем текст из элемента p с классом OrderFeed_number
        order_number_element = elements[0].find_element(*OrdersFeedPageLocators.ORDER_NUMBER_ELEMENT)
        order_text = order_number_element.text.strip()
        match = re.search(r'\d+', order_text)
        return match.group(0) 
    
    def get_today_orders_count(self):
        elements = self.find_elements(OrdersFeedPageLocators.TODAY_ORDERS_COUNTER)
        # Получаем текст из элемента p с классом OrderFeed_number
        order_number_element = elements[0].find_element(*OrdersFeedPageLocators.ORDER_NUMBER_ELEMENT)
        order_text = order_number_element.text.strip()
        match = re.search(r'\d+', order_text)
        return match.group(0) 
    
    def get_order_number_from_in_progress(self, order_number):
        # Используем _is_order_in_progress для проверки наличия заказа
        if self._is_order_in_progress(order_number):
            return order_number
        return None
    
    def find_order_by_number(self, order_number):
        locator = (By.XPATH, OrdersFeedPageLocators.ORDER_BY_NUMBER_PATTERN.format(order_number))
        # Ждем появления заказа с повторными попытками
        wait = self.create_wait(timeout=15)
        wait.until(lambda d: len(self.find_elements(locator)) > 0)
        return self.find_elements(locator)
    
    #Ждет появления первого заказа в ленте
    def wait_for_orders_to_load(self):
        self.wait.until(EC.presence_of_element_located(OrdersFeedPageLocators.FIRST_ORDER))
    
    #Ждет появления счетчиков заказов
    def wait_for_counters_to_load(self, timeout=15):
        wait = self.create_wait(timeout=timeout)
        # Ждем появления обоих счетчиков
        wait.until(EC.presence_of_element_located(OrdersFeedPageLocators.TOTAL_ORDERS_COUNTER))
        wait.until(EC.presence_of_element_located(OrdersFeedPageLocators.TODAY_ORDERS_COUNTER))
    
    #Ждет появления модального окна заказа
    def wait_for_order_modal(self):
        self.wait.until(EC.visibility_of_element_located(OrdersFeedPageLocators.ORDER_MODAL))
    
    #Ждет обновления счетчика (проверяет, что значение изменилось)
    def wait_for_counter_update(self, initial_value, get_counter_func, timeout=20):
        wait = self.create_wait(timeout=timeout)
        wait.until(lambda driver: int(get_counter_func()) > int(initial_value))
    
    #Ждет появления заказа в разделе "В работе"
    def wait_for_order_in_progress(self, order_number, timeout=60):
        wait = self.create_wait(timeout=timeout)
        # Ждем появления раздела "В работе" сначала
        wait.until(EC.presence_of_element_located(OrdersFeedPageLocators.IN_PROGRESS_ORDER_LIST))
        
        # Затем ждем появления конкретного заказа по номеру (номер может начинаться с 0)
        wait.until(lambda driver: self._is_order_in_progress(order_number))
    
    #Проверяет, что заказ появился в разделе "В работе" 
    def _is_order_in_progress(self, order_number):
        ul_elements = self.find_elements(OrdersFeedPageLocators.IN_PROGRESS_ORDER_LIST)
        if not ul_elements:
            return False
        li_elements = ul_elements[0].find_elements(By.TAG_NAME, "li")
        for li in li_elements:
            li_text = li.text.strip()
            # Пропускаем элемент с текстом "Все текущие заказы готовы!"
            if "Все текущие заказы готовы" in li_text:
                continue
            # Проверяем, содержит ли текст номер заказа
            if order_number in li_text or (not order_number.startswith('0') and f"0{order_number}" in li_text):
                return True
        return False


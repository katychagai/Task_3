from selenium.webdriver.common.by import By
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
        # Сначала проверяем наличие списка "В работе"
        elements = self.find_elements(OrdersFeedPageLocators.IN_PROGRESS_ORDER_LIST)
        # Ищем заказ по номеру внутри списка "В работе"
        ul_element = elements[0]
        # Ищем все li элементы внутри ul
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        for li_element in li_elements:
            li_text = li_element.text.strip()
            # Извлекаем номер из текста и сравниваем как числа
            match = re.search(r'\d+', li_text)
            if match and int(match.group(0)) == int(order_number):
                return order_number
    
    def find_order_by_number(self, order_number):
        locator = (By.XPATH, OrdersFeedPageLocators.ORDER_BY_NUMBER_PATTERN.format(order_number))
        return self.find_elements(locator)


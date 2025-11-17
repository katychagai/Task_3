from .base_page import BasePage
from ..locators import ProfilePageLocators


#Страница профиля пользователя
class ProfilePage(BasePage):
    
    def click_logout_button(self):
        self.close_modals_if_present()
        self.wait_for_modal_to_disappear()
        element = self.find_element_clickable(ProfilePageLocators.LOGOUT_BUTTON)
        self.click_via_js(element)
    
    def click_orders_history_link(self):
        # Закрываем модальные окна, если они открыты
        self.close_modals_if_present()
        self.wait_for_modal_to_disappear()
        element = self.find_element_clickable(ProfilePageLocators.ORDERS_HISTORY_LINK)
        self.click_via_js(element)
    
    #Ждет перехода на страницу истории заказов
    def wait_for_orders_history_page(self, timeout=20):
        wait = self.create_wait(timeout=timeout)
        # Проверяем, что URL содержит "orders" или "order-history"
        wait.until(lambda d: "orders" in self.get_current_url() or "order-history" in self.get_current_url())
    
    def logout(self):
        self.click_logout_button()


from .base_page import BasePage
from ..locators import ProfilePageLocators


#Страница профиля пользователя
class ProfilePage(BasePage):
    
    def click_logout_button(self):
        self.click(ProfilePageLocators.LOGOUT_BUTTON)
    
    def click_orders_history_link(self):
        # Закрываем модальные окна, если они открыты
        self.close_modals_if_present()
        element = self.find_element_clickable(ProfilePageLocators.ORDERS_HISTORY_LINK)
        self.driver.execute_script("arguments[0].click();", element)
    
    def logout(self):
        self.click_logout_button()


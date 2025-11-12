
from .base_page import BasePage
from ..locators import ResetPasswordPageLocators


#Страница сброса пароля
class ResetPasswordPage(BasePage):

    def enter_password(self, password):
        self.send_keys(ResetPasswordPageLocators.NEW_PASSWORD_INPUT, password)
    
    def click_show_password_button(self):
        self.click(ResetPasswordPageLocators.SHOW_PASSWORD_BUTTON)
    
    def is_password_input_active(self):
        parent_with_active = self.find_elements(ResetPasswordPageLocators.ACTIVE_PASSWORD_FIELD_PARENT)
        return bool(parent_with_active)


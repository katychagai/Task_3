from .base_page import BasePage
from ..locators import ForgotPasswordPageLocators, BasePageLocators

#Страница восстановления пароля
class ForgotPasswordPage(BasePage):

    def enter_email(self, email):
        self.send_keys(BasePageLocators.EMAIL_INPUT, email)
    
    def click_restore_button(self):
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)
    


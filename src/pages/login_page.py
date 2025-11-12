from .base_page import BasePage
from ..locators import LoginPageLocators, BasePageLocators


#Страница входа в аккаунт
class LoginPage(BasePage):

    def enter_email(self, email):
        self.send_keys(BasePageLocators.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        self.send_keys(BasePageLocators.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        self.click(LoginPageLocators.LOGIN_BUTTON)
    
    def click_forgot_password_link(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)
    
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()


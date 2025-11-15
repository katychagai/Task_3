from .base_page import BasePage
from ..locators import LoginPageLocators, BasePageLocators
from ..urls import MAIN_PAGE


#Страница входа в аккаунт
class LoginPage(BasePage):

    def enter_email(self, email):
        self.send_keys(BasePageLocators.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        self.send_keys(BasePageLocators.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        self.click(LoginPageLocators.LOGIN_BUTTON)
    
    def click_forgot_password_link(self):
        self.close_modals_if_present()
        self.wait_for_modal_to_disappear()
        # Ждем, пока ссылка станет кликабельной
        element = self.find_element_clickable(LoginPageLocators.FORGOT_PASSWORD_LINK)
        href = element.get_attribute("href")
        if href:
            self.navigate_to_url(href)
        else:
            self.click_via_js(element)
    
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        self.wait_for_url(MAIN_PAGE, timeout=30)


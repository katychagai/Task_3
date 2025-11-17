from .base_page import BasePage
from ..locators import ForgotPasswordPageLocators, BasePageLocators

#Страница восстановления пароля
class ForgotPasswordPage(BasePage):

    def enter_email(self, email):
        self.send_keys(BasePageLocators.EMAIL_INPUT, email)
    
    def click_restore_button(self):
        self.close_modals_if_present()
        self.wait_for_modal_to_disappear()
        # Используем JS-клик для обхода перекрытия модальными окнами
        element = self.find_element_clickable(ForgotPasswordPageLocators.RESTORE_BUTTON)
        self.click_via_js(element)
    


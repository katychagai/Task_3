import allure
from src.pages.main_page import MainPage
from src.pages.login_page import LoginPage
from src.pages.forgot_password_page import ForgotPasswordPage
from src.pages.reset_password_page import ResetPasswordPage
from src.helpers import generate_user_data
from src.locators import ResetPasswordPageLocators, LoginPageLocators, ForgotPasswordPageLocators
from src.urls import LOGIN_PAGE, FORGOT_PASSWORD_PAGE, RESET_PASSWORD_PAGE


@allure.epic("Stellar Burgers UI")
@allure.feature("Восстановление пароля")
class TestForgotPassword:
    
    @allure.story("Восстановление пароля")
    @allure.title("Переход на страницу восстановления пароля по кнопке 'Восстановить пароль'")
    def test_go_to_forgot_password_page(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        forgot_password_page = ForgotPasswordPage(driver)
        
        with allure.step("Кликаем на кнопку 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Дождаться перехода на страницу /login"):
            login_page.wait_for_url(LOGIN_PAGE)
            # Ждем загрузки элементов страницы входа
            login_page.wait.until(lambda d: login_page.find_elements(LoginPageLocators.FORGOT_PASSWORD_LINK))
        
        with allure.step("Кликаем на кнопку 'Восстановить пароль'"):
            login_page.click_forgot_password_link()
        
        with allure.step("Дождаться страницы /forgot-password"):
            forgot_password_page.wait_for_url(FORGOT_PASSWORD_PAGE)
        
        with allure.step("Проверяем, что перешли на страницу восстановления пароля"):
            assert forgot_password_page.is_url_contains(FORGOT_PASSWORD_PAGE)
    
    @allure.story("Восстановление пароля")
    @allure.title("Ввод почты и клик по кнопке 'Восстановить'")
    def test_restore_password_with_email(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        forgot_password_page = ForgotPasswordPage(driver)
        reset_password_page = ResetPasswordPage(driver)
        user_data = generate_user_data()
        
        with allure.step("Кликаем на кнопку 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Дождаться перехода на страницу /login"):
            login_page.wait_for_url(LOGIN_PAGE)
            # Ждем загрузки элементов страницы входа
            login_page.wait.until(lambda d: login_page.find_elements(LoginPageLocators.FORGOT_PASSWORD_LINK))
        
        with allure.step("Кликаем на кнопку 'Восстановить пароль'"):
            login_page.click_forgot_password_link()
        
        with allure.step("Дождаться страницы /forgot-password"):
            forgot_password_page.wait_for_url(FORGOT_PASSWORD_PAGE)
            # Ждем загрузки элементов страницы восстановления пароля
            forgot_password_page.wait.until(lambda d: forgot_password_page.find_elements(ForgotPasswordPageLocators.RESTORE_BUTTON))
        
        with allure.step("Ввести любой email в поле email"):
            forgot_password_page.enter_email(user_data["email"])
        
        with allure.step("Нажать кнопку 'Восстановить'"):
            forgot_password_page.click_restore_button()
        
        with allure.step("Дождаться страницы /reset-password"):
            reset_password_page.wait_for_url(RESET_PASSWORD_PAGE)
            # Ждем загрузки элементов страницы сброса пароля
            reset_password_page.wait.until(lambda d: reset_password_page.find_elements(ResetPasswordPageLocators.NEW_PASSWORD_INPUT))
        
        with allure.step("Проверяем, что перешли на страницу сброса пароля"):
            assert reset_password_page.is_url_contains(RESET_PASSWORD_PAGE)
    
    @allure.story("Восстановление пароля")
    @allure.title("Клик по кнопке показать/скрыть пароль делает поле активным")
    def test_show_password_button_activates_field(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        forgot_password_page = ForgotPasswordPage(driver)
        reset_password_page = ResetPasswordPage(driver)
        user_data = generate_user_data()
        
        with allure.step("Кликаем на кнопку 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Дождаться перехода на страницу /login"):
            login_page.wait_for_url(LOGIN_PAGE)
            # Ждем загрузки элементов страницы входа
            login_page.wait.until(lambda d: login_page.find_elements(LoginPageLocators.FORGOT_PASSWORD_LINK))
        
        with allure.step("Кликаем на кнопку 'Восстановить пароль'"):
            login_page.click_forgot_password_link()
        
        with allure.step("Дождаться страницы /forgot-password"):
            forgot_password_page.wait_for_url(FORGOT_PASSWORD_PAGE)
            # Ждем загрузки элементов страницы восстановления пароля
            forgot_password_page.wait.until(lambda d: forgot_password_page.find_elements(ForgotPasswordPageLocators.RESTORE_BUTTON))
        
        with allure.step("Ввести любой email в поле email"):
            forgot_password_page.enter_email(user_data["email"])
        
        with allure.step("Нажать кнопку 'Восстановить'"):
            forgot_password_page.click_restore_button()
        
        with allure.step("Дождаться страницы /reset-password"):
            reset_password_page.wait_for_url(RESET_PASSWORD_PAGE)
            # Ждем загрузки элементов страницы сброса пароля
            reset_password_page.wait.until(lambda d: reset_password_page.find_elements(ResetPasswordPageLocators.NEW_PASSWORD_INPUT))
        
        with allure.step("Ввести пароль в поле пароль"):
            reset_password_page.enter_password(user_data["password"])
        
        with allure.step("Кликаем на поле пароля, чтобы оно получило фокус"):
            reset_password_page.close_modals_if_present()
            password_input = reset_password_page.find_element_clickable(ResetPasswordPageLocators.NEW_PASSWORD_INPUT)
            reset_password_page.click_via_js(password_input)
        
        with allure.step("Кликаем на кнопку показать/скрыть пароль"):
            reset_password_page.click_show_password_button()
            # Ждем активации поля пароля
            reset_password_page.wait.until(lambda d: reset_password_page.is_password_input_active())  
        
        with allure.step("Проверяем, что поле пароля стало активным (подсвечено)"):
            is_active = reset_password_page.is_password_input_active()
            assert is_active


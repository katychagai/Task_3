import allure
from src.pages.profile_page import ProfilePage
from src.locators import ProfilePageLocators
from src.urls import PROFILE_PAGE, LOGIN_PAGE


@allure.epic("Stellar Burgers UI")
@allure.feature("Профиль пользователя")
class TestProfile:
    
    @allure.story("Личный кабинет")
    @allure.title("Переход по клику на 'Личный кабинет'")
    def test_go_to_personal_account(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем на 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Проверяем переход в личный кабинет"):
            profile_page.wait_for_url(PROFILE_PAGE)
            assert profile_page.is_url_contains(PROFILE_PAGE)
    
    @allure.story("Личный кабинет")
    @allure.title("Переход в раздел 'История заказов'")
    def test_go_to_orders_history(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        profile_page = ProfilePage(driver)
        
        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account_button()
            profile_page.wait_for_url(PROFILE_PAGE)
            # Ждем загрузки страницы профиля
            profile_page.wait.until(lambda d: profile_page.find_elements(ProfilePageLocators.ORDERS_HISTORY_LINK))
        
        with allure.step("Кликаем на раздел 'История заказов'"):
            profile_page.click_orders_history_link()
            profile_page.wait_for_orders_history_page(timeout=20)
        
        with allure.step("Проверяем переход в раздел истории заказов"):
            current_url = profile_page.get_current_url()
            assert "order-history" in current_url
    
    @allure.story("Личный кабинет")
    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        login_page = authenticated_user["login_page"]
        profile_page = ProfilePage(driver)
        
        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account_button()
            profile_page.wait_for_url(PROFILE_PAGE)
            # Ждем загрузки страницы профиля
            profile_page.wait.until(lambda d: profile_page.find_elements(ProfilePageLocators.LOGOUT_BUTTON))
        
        with allure.step("Выполняем выход из аккаунта"):
            profile_page.logout()
        
        with allure.step("Проверяем переход на страницу входа"):
            login_page.wait_for_url(LOGIN_PAGE)
            assert login_page.is_url_contains(LOGIN_PAGE)


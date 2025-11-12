import allure
import time
from src.pages.main_page import MainPage
from src.pages.login_page import LoginPage
from src.urls import MAIN_PAGE, LOGIN_PAGE, ORDERS_FEED_PAGE


@allure.epic("Stellar Burgers UI")
@allure.feature("Основной функционал")
class TestMainFunctionality:
    
    @allure.story("Навигация")
    @allure.title("Переход по клику на 'Конструктор'")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        
        with allure.step("Переходим в другое место (например, в личный кабинет)"):
            main_page.click_personal_account_button()
            login_page.wait_for_url(LOGIN_PAGE)
        
        with allure.step("Кликаем на кнопку 'Конструктор'"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем переход на главную страницу (конструктор)"):
            main_page.wait_for_url(MAIN_PAGE)
    
    @allure.story("Навигация")
    @allure.title("Переход по клику на 'Лента заказов'")
    def test_go_to_orders_feed(self, driver):
        main_page = MainPage(driver)
        
        with allure.step("Кликаем на кнопку 'Лента заказов'"):
            main_page.click_orders_feed_button()
        
        with allure.step("Проверяем переход на страницу ленты заказов"):
            main_page.wait_for_url(ORDERS_FEED_PAGE)
    
    @allure.story("Ингредиенты")
    @allure.title("При клике на ингредиент появляется всплывающее окно с деталями")
    def test_ingredient_click_shows_modal(self, driver):
        main_page = MainPage(driver)
        
        with allure.step("Кликаем на первый ингредиент"):
            main_page.click_first_ingredient()
        
        with allure.step("Проверяем появление модального окна с деталями"):
            assert main_page.is_modal_window_visible(), "Модальное окно должно появиться после клика на ингредиент"
    
    @allure.story("Ингредиенты")
    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_modal_closes_on_close_button(self, driver):
        main_page = MainPage(driver)
        
        with allure.step("Открываем модальное окно, кликая на ингредиент"):
            main_page.click_first_ingredient()
        
        with allure.step("Кликаем на кнопку закрытия (крестик)"):
            main_page.click_modal_close_button()
        
        with allure.step("Проверяем, что модальное окно закрылось"):
            time.sleep(0.5)
            assert not main_page.is_modal_window_visible(), "Модальное окно должно закрыться"
    
    @allure.story("Конструктор")
    @allure.title("При добавлении ингредиента в заказ увеличивается каунтер")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        
        with allure.step("Прокручиваем в самый верх страницы (секция 'Булки' должна быть видна)"):
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.3)
        
        with allure.step("Получаем начальное значение счетчика первого ингредиента из секции 'Булки'"):
            initial_counter = main_page.get_ingredient_counter()
            time.sleep(1)  # Задержка для получения счетчика ингредиента в секции "Булки"
        
        with allure.step("Добавляем ингредиент в конструктор (перетаскиваем)"):
            main_page.drag_ingredient_to_constructor()
            time.sleep(3)  # Ждем обновления счетчика
        
        with allure.step("Проверяем, что счетчик увеличился"):
            # Пробуем получить счетчик несколько раз с задержкой
            new_counter = initial_counter
            for _ in range(5):
                new_counter = main_page.get_ingredient_counter()
                if new_counter > initial_counter:
                    break
                time.sleep(0.5)
            
            assert new_counter > initial_counter
    
    @allure.story("Заказ")
    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_logged_in_user_can_create_order(self, authenticated_user):
        main_page = authenticated_user["main_page"]
        
        with allure.step("Добавляем ингредиенты в конструктор"):
            main_page.drag_ingredient_to_constructor()
            time.sleep(1)
            main_page.drag_ingredient_to_constructor()
            time.sleep(1)
        
        with allure.step("Кликаем на кнопку 'Оформить заказ'"):
            main_page.click_order_button()
        
        with allure.step("Проверяем появление модального окна с номером заказа"):
            time.sleep(5)
            assert main_page.is_order_modal_visible()
            
            order_number = None
            for _ in range(10):
                order_number = main_page.get_order_number()
                if order_number:
                    break
                time.sleep(0.5)
            
            assert order_number is not None

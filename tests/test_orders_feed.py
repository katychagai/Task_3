import allure
import time
from src.pages.main_page import MainPage
from src.pages.orders_feed_page import OrdersFeedPage
from src.pages.profile_page import ProfilePage
from src.urls import ORDERS_FEED_PAGE, PROFILE_PAGE, MAIN_PAGE


@allure.epic("Stellar Burgers UI")
@allure.feature("Лента заказов")
class TestOrdersFeed:

    @allure.story("Лента заказов")
    @allure.title("При клике на заказ открывается всплывающее окно с деталями")
    def test_order_click_shows_modal(self, driver):
        main_page = MainPage(driver)
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Переходим на страницу ленты заказов"):
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(5)  # Ждем загрузки заказов

        with allure.step("Кликаем на первый заказ"):
            orders_feed_page.click_first_order()
            time.sleep(3)
        
        with allure.step("Проверяем появление модального окна с деталями заказа"):
            time.sleep(0.5)
            assert orders_feed_page.is_order_modal_visible()

    @allure.story("Лента заказов")
    @allure.title("Заказы пользователя из раздела 'История заказов' отображаются на странице 'Лента заказов'")
    def test_user_orders_displayed_in_feed(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        profile_page = ProfilePage(driver)
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Создаем заказ и получаем его номер"):
            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)
            
            # Оформляем заказ
            main_page.click_order_button()
            time.sleep(4)  
            
            # Получаем номер заказа
            order_number = main_page.get_order_number()
            time.sleep(2)
            
            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()
            time.sleep(1)  

        with allure.step("Переходим в раздел 'История заказов'"):
            main_page.click_personal_account_button()
            profile_page.wait_for_url(PROFILE_PAGE)
            profile_page.click_orders_history_link()
            time.sleep(2)

        with allure.step("Переходим на страницу 'Лента заказов' и проверяем наличие заказа"):
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(5)  
            
            # Ждем появления заказа в ленте с повторными попытками
            order_in_feed = []
            order_in_feed = orders_feed_page.find_order_by_number(order_number)
            time.sleep(2)  
            
            assert order_in_feed

    @allure.story("Лента заказов")
    @allure.title("При создании нового заказа счётчик 'Выполнено за всё время' увеличивается")
    def test_total_orders_counter_increases(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Переходим на страницу ленты заказов и запоминаем начальное значение счетчика"):
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(3)  # Ждем загрузки счетчиков
            initial_total_count = orders_feed_page.get_total_orders_count()

        with allure.step("Возвращаемся на главную и создаем заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_url(MAIN_PAGE)

            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)

            # Оформляем заказ
            main_page.click_order_button()
            time.sleep(3)  # Ждем обработки заказа (модальное окно)

            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()

        with allure.step("Переходим обратно на ленту заказов и проверяем счетчик"):
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(3)

            new_total_count = orders_feed_page.get_total_orders_count()
            time.sleep(2)
            
            assert int(new_total_count) > int(initial_total_count)

    @allure.story("Лента заказов")
    @allure.title("При создании нового заказа счётчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_counter_increases(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Переходим на страницу ленты заказов и запоминаем начальное значение счетчика"):                                                       
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(7)  # Ждем загрузки счетчиков
            initial_today_count = orders_feed_page.get_today_orders_count()

        with allure.step("Возвращаемся на главную и создаем заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_url(MAIN_PAGE)

            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)

            # Оформляем заказ
            main_page.click_order_button()
            time.sleep(5)  # Ждем обработки заказа (модальное окно)

            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()
            time.sleep(2)

        with allure.step("Переходим обратно на ленту заказов и проверяем счетчик"):                                                                             
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(8)  # Ждем обновления счетчика

            new_today_count = orders_feed_page.get_today_orders_count()
            time.sleep(2)
            
            assert int(new_today_count) > int(initial_today_count)

    @allure.story("Лента заказов")
    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    def test_order_appears_in_progress(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Создаем заказ и получаем его номер"):
            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)
            main_page.drag_ingredient_to_constructor()
            time.sleep(0.5)

            # Оформляем заказ
            main_page.click_order_button()
            time.sleep(3)
            
            # Получаем номер заказа из модального окна
            order_number = main_page.get_order_number()
            
            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()

        with allure.step("Переходим на страницу 'Лента заказов' и проверяем номер заказа в разделе 'В работе'"):
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            time.sleep(3)

            # Ищем заказ по номеру в разделе "В работе"
            in_progress_order_number = orders_feed_page.get_order_number_from_in_progress(order_number)
            time.sleep(1)
            
            assert in_progress_order_number == order_number

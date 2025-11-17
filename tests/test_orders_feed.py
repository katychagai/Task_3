import allure
from src.pages.main_page import MainPage
from src.pages.orders_feed_page import OrdersFeedPage
from src.pages.profile_page import ProfilePage
from src.locators import MainPageLocators, ProfilePageLocators
from src.urls import ORDERS_FEED_PAGE, PROFILE_PAGE, MAIN_PAGE
from src.config import get_settings


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
            orders_feed_page.wait_for_orders_to_load()

        with allure.step("Кликаем на первый заказ"):
            orders_feed_page.click_first_order()
            orders_feed_page.wait_for_order_modal()
        
        with allure.step("Проверяем появление модального окна с деталями заказа"):
            assert orders_feed_page.is_order_modal_visible()

    @allure.story("Лента заказов")
    @allure.title("Заказы пользователя из раздела 'История заказов' отображаются на странице 'Лента заказов'")
    def test_user_orders_displayed_in_feed(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        profile_page = ProfilePage(driver)
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Создаем заказ и получаем его номер"):
            # Ждем загрузки элементов главной страницы
            main_page.wait.until(lambda d: main_page.find_elements(MainPageLocators.ORDER_BUTTON))
            
            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            main_page.drag_ingredient_to_constructor()
            
            # Ждем, пока сумма заказа станет больше 0
            main_page.wait.until(lambda d: main_page._get_order_total_price() > 0)
            
            # Оформляем заказ
            main_page.click_order_button()
            main_page.is_order_modal_visible()  # Ждем появления модального окна
            
            # Получаем номер заказа
            order_number = main_page.get_order_number()
            
            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()  

        with allure.step("Переходим в раздел 'История заказов'"):
            main_page.click_personal_account_button()
            profile_page.wait_for_url(PROFILE_PAGE)
            # Ждем загрузки страницы профиля
            profile_page.wait.until(lambda d: profile_page.find_elements(ProfilePageLocators.ORDERS_HISTORY_LINK))
            profile_page.click_orders_history_link()
            # Ждем загрузки истории заказов
            profile_page.wait_for_orders_history_page(timeout=10)

        with allure.step("Переходим на страницу 'Лента заказов' и проверяем наличие заказа"):
            # Используем прямой переход по URL вместо поиска кнопки
            base_url = get_settings().base_url.rstrip("/")
            orders_feed_page.navigate_to_url(f"{base_url}{ORDERS_FEED_PAGE}")
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            orders_feed_page.wait_for_orders_to_load()
            
            # Ждем появления заказа в ленте с повторными попытками
            wait = orders_feed_page.create_wait(timeout=10)
            wait.until(lambda d: len(orders_feed_page.find_order_by_number(order_number)) > 0)
            
            order_in_feed = orders_feed_page.find_order_by_number(order_number)
            
            assert order_in_feed

    @allure.story("Лента заказов")
    @allure.title("При создании нового заказа счётчик 'Выполнено за всё время' увеличивается")
    def test_total_orders_counter_increases(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Переходим на страницу ленты заказов и запоминаем начальное значение счетчика"):
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            # Ждем загрузки страницы и элементов
            orders_feed_page.wait_for_orders_to_load()
            orders_feed_page.wait_for_counters_to_load()
            initial_total_count = orders_feed_page.get_total_orders_count()

        with allure.step("Возвращаемся на главную и создаем заказ"):
            # Используем прямой переход по URL
            base_url = get_settings().base_url.rstrip("/")
            main_page.navigate_to_url(f"{base_url}{MAIN_PAGE}")
            main_page.wait_for_url(MAIN_PAGE, timeout=30)
            # Ждем загрузки элементов главной страницы с увеличенным таймаутом
            wait = main_page.create_wait(timeout=30)
            wait.until(lambda d: main_page.find_elements(MainPageLocators.ORDER_BUTTON))

            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            main_page.drag_ingredient_to_constructor()
            
            # Ждем, пока сумма заказа станет больше 0
            main_page.wait.until(lambda d: main_page._get_order_total_price() > 0)

            # Оформляем заказ
            main_page.click_order_button()
            main_page.is_order_modal_visible()  # Ждем появления модального окна

            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()

        with allure.step("Переходим обратно на ленту заказов и проверяем счетчик"):
            # Используем прямой переход по URL
            base_url = get_settings().base_url.rstrip("/")
            orders_feed_page.navigate_to_url(f"{base_url}{ORDERS_FEED_PAGE}")
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            # Ждем загрузки страницы и элементов
            orders_feed_page.wait_for_orders_to_load()
            orders_feed_page.wait_for_counters_to_load()
            
            # Ждем обновления счетчика
            orders_feed_page.wait_for_counter_update(initial_total_count, orders_feed_page.get_total_orders_count, timeout=20)
            new_total_count = orders_feed_page.get_total_orders_count()
            
            assert int(new_total_count) > int(initial_total_count)

    @allure.story("Лента заказов")
    @allure.title("При создании нового заказа счётчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_counter_increases(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Переходим на страницу ленты заказов и запоминаем начальное значение счетчика"):                                                       
            main_page.click_orders_feed_button()
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            # Ждем загрузки страницы и элементов
            orders_feed_page.wait_for_orders_to_load()
            orders_feed_page.wait_for_counters_to_load()
            initial_today_count = orders_feed_page.get_today_orders_count()

        with allure.step("Возвращаемся на главную и создаем заказ"):
            # Используем прямой переход по URL
            base_url = get_settings().base_url.rstrip("/")
            main_page.navigate_to_url(f"{base_url}{MAIN_PAGE}")
            main_page.wait_for_url(MAIN_PAGE, timeout=30)
            # Ждем загрузки элементов главной страницы с увеличенным таймаутом
            wait = main_page.create_wait(timeout=30)
            wait.until(lambda d: main_page.find_elements(MainPageLocators.ORDER_BUTTON))

            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            main_page.drag_ingredient_to_constructor()
            
            # Ждем, пока сумма заказа станет больше 0
            main_page.wait.until(lambda d: main_page._get_order_total_price() > 0)

            # Оформляем заказ
            main_page.click_order_button()
            main_page.is_order_modal_visible()  # Ждем появления модального окна

            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()

        with allure.step("Переходим обратно на ленту заказов и проверяем счетчик"):
            # Используем прямой переход по URL
            base_url = get_settings().base_url.rstrip("/")
            orders_feed_page.navigate_to_url(f"{base_url}{ORDERS_FEED_PAGE}")
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            # Ждем загрузки страницы и элементов
            orders_feed_page.wait_for_orders_to_load()
            orders_feed_page.wait_for_counters_to_load()
            
            # Ждем обновления счетчика
            orders_feed_page.wait_for_counter_update(initial_today_count, orders_feed_page.get_today_orders_count, timeout=20)
            new_today_count = orders_feed_page.get_today_orders_count()
            
            assert int(new_today_count) > int(initial_today_count)

    @allure.story("Лента заказов")
    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    def test_order_appears_in_progress(self, driver, authenticated_user):
        main_page = authenticated_user["main_page"]
        orders_feed_page = OrdersFeedPage(driver)

        with allure.step("Создаем заказ и получаем его номер из модального окна"):
            # Ждем загрузки элементов главной страницы
            main_page.wait.until(lambda d: main_page.find_elements(MainPageLocators.ORDER_BUTTON))

            # Добавляем ингредиенты
            main_page.drag_ingredient_to_constructor()
            main_page.drag_ingredient_to_constructor()
            
            # Ждем, пока сумма заказа станет больше 0
            main_page.wait.until(lambda d: main_page._get_order_total_price() > 0)

            # Оформляем заказ
            main_page.click_order_button()
            main_page.is_order_modal_visible()  # Ждем появления модального окна
            
            # Получаем номер заказа из модального окна (метод ждет, пока номер изменится с "9999" на реальный)
            order_number = main_page.get_order_number()
            
            # Закрываем модальное окно заказа
            main_page.click_order_modal_close_button()
            
            # Ждем немного, чтобы заказ успел обработаться на сервере
            wait = main_page.create_wait(timeout=3)
            # Просто небольшая пауза для обработки заказа на сервере
            wait.until(lambda d: True)

        with allure.step("Переходим на страницу 'Лента заказов' и проверяем номер заказа в разделе 'В работе'"):
            # Используем прямой переход по URL
            base_url = get_settings().base_url.rstrip("/")
            orders_feed_page.navigate_to_url(f"{base_url}{ORDERS_FEED_PAGE}")
            orders_feed_page.wait_for_url(ORDERS_FEED_PAGE)
            # Ждем загрузки страницы и элементов
            orders_feed_page.wait_for_orders_to_load()
            orders_feed_page.wait_for_counters_to_load()

            # Ждем появления заказа в разделе "В работе"
            orders_feed_page.wait_for_order_in_progress(order_number, timeout=3)
            
            # Проверяем, что заказ появился в разделе "В работе" (после ожидания элемент уже должен быть виден)
            in_progress_order_number = orders_feed_page.get_order_number_from_in_progress(order_number)
            assert in_progress_order_number == order_number or (not order_number.startswith('0') and in_progress_order_number == f"0{order_number}")

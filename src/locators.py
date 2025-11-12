
from selenium.webdriver.common.by import By


#Локаторы главной страницы
class MainPageLocators:
    
    # Навигация
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[contains(@href, '/account')]")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDERS_FEED_BUTTON = (By.XPATH, "//a[contains(@href, '/feed')]")
    
    # Ингредиенты
    FIRST_INGREDIENT = (By.XPATH, "(//div[contains(@class, 'BurgerIngredient_ingredient')])[1]")
    FIRST_INGREDIENT_IN_BUNS = (By.XPATH, "//h2[contains(text(),'Булки')]/following-sibling::div[1]//div[contains(@class, 'BurgerIngredient_ingredient')][1] | //h2[contains(text(),'Булки')]/../following-sibling::div//div[contains(@class, 'BurgerIngredient_ingredient')][1]")
    INGREDIENT_COUNTER_IN_BUNS = (By.XPATH, "//section[contains(@class, 'BurgerIngredients')]//ul[contains(@class, 'ingredients__list')]//div[contains(@class, 'counter_counter')]")
    
    # Модальное окно с деталями ингредиента
    MODAL_WINDOW = (By.XPATH, "//h2[contains(@class, 'Modal_modal') and text()='Детали ингредиента']")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    
    # Конструктор бургера
    BURGER_CONSTRUCTOR = (By.XPATH, "//section[contains(@class, 'BurgerConstructor')]")
    
    # Кнопка заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    
    # Модальное окно заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow')]")
    ORDER_MODAL_CLOSE_BUTTON = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//button[@type='button']")


#Локаторы страницы входа
class LoginPageLocators:
    
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, '/forgot-password')]")


#Локаторы страницы профиля
class ProfilePageLocators:
    
    ORDERS_HISTORY_LINK = (By.XPATH, "//a[contains(@href, '/profile/orders')] | //a[contains(@href, '/account/orders')] | //a[contains(text(), 'История заказов')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")


#Локаторы страницы восстановления пароля
class ForgotPasswordPageLocators:
    
    RESTORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")


#Локаторы страницы сброса пароля
class ResetPasswordPageLocators:
    
    NEW_PASSWORD_INPUT = (By.XPATH, "//input[@name='Введите новый пароль']")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[@class='input__icon input__icon-action']")
    ACTIVE_PASSWORD_FIELD_PARENT = (By.XPATH, "//input[@name='Введите новый пароль']/ancestor::div[contains(@class, 'input') and contains(@class, 'input_status_active')]")

#Локаторы страницы ленты заказов"""
class OrdersFeedPageLocators:
    
    # Локаторы заказов
    FIRST_ORDER = (By.XPATH, "//main[contains(@class, 'componentContainer')]//li[1]//a[1]")
    
    # Модальное окно с деталями заказа
    ORDER_MODAL = (By.CSS_SELECTOR, "div[class*='Modal_orderBox']")
    
    # Счетчики
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//div[contains(@class, 'undefined') and .//p[contains(@class, 'OrderFeed_number')]]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//div[p[text()='Выполнено за сегодня:'] and p[contains(@class, 'OrderFeed_number')]]")
    ORDER_NUMBER_ELEMENT = (By.XPATH, ".//p[contains(@class, 'OrderFeed_number')]")
    
    # Раздел "В работе"
    IN_PROGRESS_ORDER_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]")
    
    # Заказы пользователя
    USER_ORDERS = (By.XPATH, "//div[contains(@class, 'OrderItem') and contains(@class, 'OrderItem_own')]")
    
    # Шаблон для поиска заказа по номеру
    ORDER_BY_NUMBER_PATTERN = "//*[contains(text(), '{}')]"


#Общие локаторы для базовой страницы
class BasePageLocators:
  
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")


import pytest
from src.browser_factory import BrowserFactory
from src.config import get_settings
from src.pages.main_page import MainPage
from src.pages.login_page import LoginPage
from src.api_client import register_user, delete_user
from src.helpers import generate_user_data
from src.urls import LOGIN_PAGE
from src.locators import LoginPageLocators, MainPageLocators


#Универсальная фикстура для создания драйвера браузера
@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    
    # Используем фабрику для создания драйвера
    driver = BrowserFactory.create_driver(request.param)
    
    settings = get_settings()
    driver.get(settings.base_url)
    
    yield driver
    
    driver.quit()


#Фикстура для создания авторизованного пользователя
#Создает пользователя через API, выполняет вход через UI
@pytest.fixture(scope="function")
def authenticated_user(driver):
    
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    
    # Создаем пользователя через API с повторными попытками, возникают случаи когда пользователь уже существует 
    max_attempts = 5
    register_response = None
    user_data = None
    
    for attempt in range(max_attempts):
        user_data = generate_user_data()
        register_response = register_user(user_data)
        
        if register_response.status_code in [200, 201]:
            break
        
        if register_response.status_code != 403:
            pytest.fail(f"Не удалось создать пользователя через API. Статус: {register_response.status_code}")
    
    # Получаем токен из ответа
    response_data = register_response.json()
    access_token = response_data.get("accessToken", "")
    
    # Выполняем вход через UI
    main_page.click_login_button()
    login_page.wait_for_url(LOGIN_PAGE, timeout=30)
    # Ждем загрузки элементов страницы входа
    login_page.wait.until(lambda d: login_page.find_elements(LoginPageLocators.LOGIN_BUTTON))
    login_page.login(user_data["email"], user_data["password"])
    # Ждем загрузки элементов главной страницы после входа
    main_page.wait.until(lambda d: main_page.find_elements(MainPageLocators.ORDER_BUTTON))
    
    yield {
        "user_data": user_data,
        "main_page": main_page,
        "login_page": login_page,
        "access_token": access_token,
    }
    
    # Удаляем пользователя после теста через API
    if access_token:
        delete_user(access_token)


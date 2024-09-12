from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import logging
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO)
@pytest.fixture
def setup():

    # Настройка веб-драйвера
    driver = webdriver.Chrome()  # Замените на ваш драйвер
    driver.get("https://makarovartem.github.io/frontend-avito-tech-test-assignment/")
    yield driver
    driver.quit()


def testcases_select_shooter_category(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    # открыть выпадающий список "Filter by category"
    filter_by_category = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[3]/div/div[2]/div[2]/div/span[2]")))
    filter_by_category.click()

    # найти и выбрать категорию "shooter"
    shooter_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and text()='shooter']")))
    shooter_option.click()

    # проверка, что элементы были отфильтрованы
    filtered_items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-typography css-17a39f8' and  text()='Genre: ' and text()='Shooter']")))
    assert len(filtered_items) > 0, "Фильтр не применился или не найдено элементов"

    # проверить, что все элементы соответствуют категории "shooter"
    for item in filtered_items:
        category = item.find_element(By.XPATH, "//div[@class='ant-typography css-17a39f8' and  text()='Genre: ' and text()='Shooter']").text
        assert category == "Genre: Shooter", f"Найден элемент другой категории: {category}"


def testcases_back_to_main(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)
    driver.get("https://makarovartem.github.io/frontend-avito-tech-test-assignment/")

    # нажать на карточку первой игры
    game_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='ant-list-item'][1]")))
    game_card.click()

    wait = WebDriverWait(driver, 10)
    back_to_main_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Back to Main']")))

    # прокрутить страницу вниз к кнопке "Back to Main"
    actions = ActionChains(driver)
    actions.move_to_element(back_to_main_button).perform()

    # нажать кнопку
    back_to_main_button.click()
    print(driver.current_url)

    # проверить, что после клика вернулись на главную страницу
    assert driver.current_url == "https://makarovartem.github.io/frontend-avito-tech-test-assignment"

def testcases_pagination(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)
    driver.get("https://makarovartem.github.io/frontend-avito-tech-test-assignment/")

    # последняя страница
    last_page = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//a[text()='40'])[2]"))).text)

    # переход по страницам
    for _ in range(last_page):
        next_page = driver.find_element(By.XPATH, "(//button[@class='ant-pagination-item-link'])[4]")
        next_page.click()

    # проверить, что последняя страница достигнута
    next_page_button = driver.find_element(By.XPATH, "(//button[@class='ant-pagination-item-link'])[4]")
    assert next_page_button.get_attribute("disabled") is not None


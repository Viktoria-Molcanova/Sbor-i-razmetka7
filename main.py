from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import json

# Настройка опций для браузера
options = Options()
options.add_argument('start-maximized')

try:
    driver = webdriver.Chrome(options=options)

    # Переход на сайт Aliexpress
    driver.get("https://aliexpress.ru")

    # Поиск элемента ввода и отправка запроса
    input_element = driver.find_element(By.ID, 'SearchText')
    input_element.send_keys("платье")
    input_element.send_keys(Keys.ENTER)

    # Инициализация переменной для хранения количества карточек
    count = 0
    products = []

    while True:
        wait = WebDriverWait(driver, 10)
        # Находим все карточки товаров
        cards = driver.find_elements(By.XPATH, "//div[@data-product-id]")
        new_count = len(cards)

        # Прокручиваем страницу вниз
        driver.execute_script("window.scrollBy(0,2000)")

        # Проверяем, изменилось ли количество карточек
        if new_count == count:
            break
        count = new_count

    # Извлечение информации о товарах
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for card in soup.find_all('div', {'data-product-id': True}):
        title = card.find('div', class_='product-snippet_ProductSnippet__block__1mogfw').text if card.find('div', class_='product-snippet_ProductSnippet__block__1mogfw') else 'Нет названия'
        price = card.find('div', class_='snow-price_SnowPrice__mainM__uw8t09').text if card.find('div', class_='snow-price_SnowPrice__mainM__uw8t09') else 'Нет цены'
        products.append({'title': title, 'price': price})

    # Сохранение результатов в файл JSON
    with open('products.json', 'w', encoding='utf-8') as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

    # Вывод результатов
    print(f"Общее количество карточек: {count}")
    for product in products:
        print(product)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()
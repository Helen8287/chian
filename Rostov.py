from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Firefox()
driver.get("https://rostov.cian.ru/snyat-kvartiru/")

wait = WebDriverWait(driver, 15)

# --- функция автоскролла ---
def scroll_page(driver, pause=1.0):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # скроллим до конца
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # дошли до конца
        last_height = new_height

# Делаем полный скролл страницы
scroll_page(driver, pause=2)

# Теперь ищем карточки
cards = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, 'article[data-name="CardComponent"]')
))

ads = []
for card in cards:
    # Цена
    try:
        price = card.find_element(By.CSS_SELECTOR, 'span[data-mark="MainPrice"]').text
    except:
        price = None

    # Адрес
    address = None
    try:
        # Вариант 1: GeoLabel
        address = card.find_element(By.CSS_SELECTOR, 'div[data-name="GeoLabel"]').text.strip()
    except:
        pass

    if not address:
        try:
            # Вариант 2: OfferSubtitle (берем все span и склеиваем)
            parts = card.find_elements(By.CSS_SELECTOR, 'div[data-mark="OfferSubtitle"] span')
            address = ", ".join([el.text for el in parts if el.text.strip()])
        except:
            address = None

    # Комнаты / описание
    try:
        rooms = card.find_element(By.CSS_SELECTOR, 'span[data-mark="OfferTitle"]').text
    except:
        rooms = None

    ads.append({
        "price": price,
        "address": address,
        "rooms": rooms
    })

print("Найдено объявлений:", len(ads))
for ad in ads[:5]:  # выводим только первые 5 для проверки
    print(ad)

# Сохраняем в CSV
with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price', 'Address', 'Rooms'])
    for ad in ads:
        writer.writerow([ad['price'], ad['address'], ad['rooms']])

driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Firefox()

url = "https://rostov.cian.ru/snyat-kvartiru/"
driver.get(url)
time.sleep(3)

    # Сбор карточек
cards = driver.find_elements(By.CSS_SELECTOR, 'article[data-name="CardComponent"]')

ads = []
for card in cards:
        try:
            price = card.find_element(By.CSS_SELECTOR, 'span[data-mark="MainPrice"]').text
        except:
            price = None

        try:  # Адрес (чаще всего в OfferSubtitle или GeoLabel)
            address = card.find_element(By.CSS_SELECTOR, 'div[data-name="GeoLabel"]').text
        except:
            try:
                address = card.find_element(By.CSS_SELECTOR, 'div[data-mark="OfferSubtitle"]').text
            except:
                address = None


        try:    # Комнаты / описание
            rooms = card.find_element(By.CSS_SELECTOR, 'span[data-mark="OfferTitle"]').text
        except:
            try:
                rooms = card.find_element(By.CSS_SELECTOR, 'span[data-mark="OfferSubtitle"]').text
            except:
                rooms = None



        ads.append({
            "price": price,
            "address": address,
            "rooms": rooms
        })

print("Найдено объявлений:", len(ads))

for ad in ads:
        print(ad)

# Открытие CSV файла для записи
with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price', 'Address', 'Rooms'])    # Записываем заголовок столбца

    for ad in ads:  # Записываем цены в CSV файл
        writer.writerow([ad['price'], ad['address'], ad['rooms']])

driver.quit()
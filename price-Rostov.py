import csv
import re

input_file = 'prices.csv'
output_file = 'prices_clean_Rostov.csv'

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # оставляем только один заголовок
    writer.writerow(['Price'])

    for row in reader:
        price_text = row['Price']  # берем колонку Price
        # Убираем всё кроме цифр
        price_digits = re.sub(r'\D', '', price_text)
        if price_digits:  # если получилось число
            writer.writerow([price_digits])
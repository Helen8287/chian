import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные из файла
df = pd.read_csv("prices_clean_Rostov.csv")

# Предположим, что в файле есть колонка 'price'
# Если она называется иначе, замените 'price' на реальное имя столбца
prices = df['Price']

# Строим гистограмму
plt.figure(figsize=(10, 6))
plt.hist(prices, bins=30, edgecolor='black')

# Добавляем подписи
plt.title("Гистограмма цен")
plt.xlabel("Цена")
plt.ylabel("Как часто сдают по такой цене")

# Отображаем график
plt.show()
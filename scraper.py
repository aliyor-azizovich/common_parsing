import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы
url = "https://www.olx.uz/nedvizhimost/doma/prodazha/ferganskaya-oblast/?currency=UZS"

# Выполнение запроса
response = requests.get(url)

# Проверка статуса ответа
if response.status_code == 200:
    # Разбор HTML-кода страницы
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Найти все объявления по классу
    ads = soup.find_all('div', class_='css-1sw7q4x')

    # Сбор данных
    data = []
    for ad in ads:
        # Извлечение заголовка
        title_tag = ad.find('h6', class_='css-1wxaaza')
        title = title_tag.text.strip() if title_tag else 'Без заголовка'
        
        # Извлечение цены
        price_tag = ad.find('p', class_='css-13afqrm')
        price = price_tag.text.strip() if price_tag else 'Цена не указана'
        
        # Извлечение адреса
        address_tag = ad.find('p', class_='css-1mwdrlh')
        address = address_tag.text.strip() if address_tag else 'Адрес не указан'
        
        # Извлечение площади
        area_tag = ad.find('span', class_='css-643j0o')
        area = area_tag.text.strip() if area_tag else 'Площадь не указана'
        
        # Извлечение ссылки на объявление
        link_tag = ad.find('a', class_='css-z3gu2d')
        link = link_tag['href'] if link_tag else 'Ссылка не найдена'
        full_url = f'https://www.olx.uz{link}' if link != 'Ссылка не найдена' else 'Ссылка не найдена'
        
        data.append({
            'Title': title,
            'Price': price,
            'Area': area,
            'Address': address,
            'URL': full_url
        })

    # Преобразование данных в DataFrame
    df = pd.DataFrame(data)

    # Сохранение в Excel файл
    df.to_excel('olx_commercial_real_estate_2.xlsx', index=False)

    print("Парсинг завершен. Данные сохранены в olx_commercial_real_estate.xlsx.")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")

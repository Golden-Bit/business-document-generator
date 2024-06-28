import requests
from bs4 import BeautifulSoup
import json


def estrai_informazioni_prodotto(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('h1', {'data-hook': 'product-title'}).get_text(strip=True)
        product_code = soup.find('div', {'data-hook': 'sku'}).get_text(strip=True).replace('SKU: ', '')
        product_price = soup.find('span', {'data-hook': 'formatted-primary-price'}).get_text(strip=True)
        product_price = product_price.replace('.', '').replace(',', '.').replace('€', '').strip()
        product_price = float(product_price)
        main_image_wrapper = soup.find('div', {'data-hook': 'main-media-image-wrapper'})
        image_info = main_image_wrapper.find('wow-image')['data-image-info'] if main_image_wrapper else None
        if image_info:
            image_data = json.loads(image_info)
            high_res_image = f"https://static.wixstatic.com/media/{image_data['imageData']['uri']}"
        else:
            high_res_image = 'Immagine non trovata'
        return {
            "name": product_name,
            "code": product_code,
            "unit_price": product_price,
            "quantity": 1,  # Default quantity
            "image": high_res_image,
            "total_price": 0  # Default total price
        }
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None

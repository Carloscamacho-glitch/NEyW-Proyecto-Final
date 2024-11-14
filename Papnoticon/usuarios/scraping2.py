# usuarios/scraping.py
import requests
from bs4 import BeautifulSoup

def obtener_precios_externos2(nombre_producto):
    precios = []
    url = "https://www.apple.com/mx/apple-one/"  # Cambia la URL según la página que desees analizar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Encuentra los planes de precios
        planes = soup.find_all("div", class_="plan-tile")
        for plan in planes:
            # Extraer el título del plan
            titulo_tag = plan.find("h3", class_="typography-plan-headline")
            titulo = titulo_tag.text.strip() if titulo_tag else ""
            
            # Verificar si el título coincide con el nombre del producto
            if nombre_producto.lower() in titulo.lower():
                # Extraer el precio del plan
                precio_tag = plan.find("p", class_="typography-plan-subhead")
                precio = precio_tag.text.strip() if precio_tag else "Precio no disponible"
                
                # Añadir el enlace actual como referencia
                enlace_completo = url

                # Añadir detalles al diccionario de precios
                precios.append({
                    "titulo": titulo,
                    "precio": precio,
                    "enlace": enlace_completo
                })
    return precios

# Ejemplo de ejecución directa
if __name__ == "__main__":
    precios = obtener_precios_externos2("Individual")
    print(precios)  # Esto debería mostrar solo los planes que coinciden con el nombre proporcionado

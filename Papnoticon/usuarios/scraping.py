# usuarios/scraping.py
import requests
from bs4 import BeautifulSoup

def obtener_precios_externos(nombre_producto):
    precios = []
    url = f"https://freedom.to/plans"  # Cambia la URL según la página que desees analizar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Encuentra los planes de precios (ajusta los selectores según el HTML)
        planes = soup.find_all("div", class_="plan-box")
        for plan in planes:
            # Título del plan
            titulo = plan.find("div", class_="plan-name").text.strip()
            
            # Precio del plan
            precio = plan.find("div", class_="regular-price").text.strip()
            
            # Enlace para iniciar la prueba gratuita
            enlace = plan.find("a", class_="plan-button")["href"]
            enlace_completo = f"https://freedom.to/plans{enlace}" if enlace.startswith("/") else enlace

            # Descripción adicional (opcional)
            descripcion = plan.find("p", class_="plan-description").text.strip()

            # Añade los detalles al diccionario de precios
            precios.append({
                "titulo": titulo,
                "precio": precio,
                "enlace": enlace_completo,
                "descripcion": descripcion
            })
    return precios

# Ejemplo de ejecución directa
if __name__ == "__main__":
    precios = obtener_precios_externos("Monthly Premium")
    print(precios)  # Esto debería mostrar los planes obtenidos de la página

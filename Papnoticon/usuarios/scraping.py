# usuarios/scraping.py
import requests
from bs4 import BeautifulSoup

def obtener_precios_externos(nombre_plan):
    precios = []
    url = f"https://www.spotify.com/mx/premium/?ref=jam"  # Cambia la URL según la página que desees analizar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Encuentra los planes de precios y filtra por el nombre del plan (ajusta los selectores según el HTML)
        planes = soup.find_all("div", {"data-component-type": "product"})
        for plan in planes:
            titulo = plan.get("data-event-plan-name", "").strip()
            
            # Verificar si el título coincide con el nombre del plan
            if nombre_plan.lower() in titulo.lower():
                # Precio del plan
                precio_tag = plan.find("p", class_="sc-71cce616-5")
                precio = precio_tag.text.strip() if precio_tag else "Precio no disponible"
                
                # Enlace para el plan (opcional)
                enlace_completo = url  # Usa la URL actual si no hay un enlace específico en el plan
                
                precios.append({
                    "titulo": titulo,
                    "precio": precio,
                    "enlace": enlace_completo
                })
    return precios

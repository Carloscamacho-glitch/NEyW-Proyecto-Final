import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.shortcuts import render

def scrape_plan_and_price_from_site(url, price_xpath, plan_xpath):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica

    # Configuración automática del ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    try:
        # Espera explícita para asegurarse de que los precios y los nombres de los planes estén cargados
        price_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, price_xpath))  # Obtener todos los precios
        )
        plan_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, plan_xpath))  # Obtener los nombres de los planes
        )

        # Extraer el texto de los precios y nombres de los planes
        prices = [price.text.strip() for price in price_elements]
        plans = [plan.text.strip() for plan in plan_elements]

    except Exception as e:
        prices = ["Error: " + str(e)]
        plans = ["Error: " + str(e)]
    finally:
        driver.quit()

    return plans, prices

def compare_prices():
    # Lista de URLs de sitios con el mismo producto y los XPATHs para los precios y los nombres de los planes
    urls = [
        ("https://www.focusatwill.com/app/pages/pricing", 
         "//div[contains(@class, '_2R15z9BByczF5NhFPDdz-v')]//h4/span[1]",  # XPATH para los precios en Focus@Will
         "//h3/span"),  # XPATH para los nombres de los planes en Focus@Will
        ("https://freedom.to/upgrade", 
         "//div[@class='regular-price']",  # XPATH para los precios en Freedom.to
         "//div[@class='plan-name']")  # XPATH para los nombres de los planes en Freedom.to
    ]
    
    # Obtener los precios y nombres de los planes de cada sitio
    all_prices_and_plans = {}
    for url, price_xpath, plan_xpath in urls:
        plans, prices = scrape_plan_and_price_from_site(url, price_xpath, plan_xpath)
        all_prices_and_plans[url] = list(zip(plans, prices))  # Emparejamos el nombre del plan con el precio

        for plan, price in zip(plans, prices):
            print(f"Plan: {plan}, Precio: {price} en {url}")  # Mostrar los planes y precios en consola
    
    # Guardar en un archivo JSON
    archivo_json = "precios_planes.json"  # Nombre del archivo
    with open(archivo_json, 'w', encoding='utf-8') as archivo:
        json.dump(all_prices_and_plans, archivo, ensure_ascii=False, indent=4)

    return all_prices_and_plans  # Retornar el diccionario con los precios y planes

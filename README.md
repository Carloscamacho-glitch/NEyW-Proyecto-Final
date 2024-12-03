# NEyW-Proyecto-Final

## SEMESTRE 2025-1

## Integrantes:

  - Arellano Hernández Israel . 318251020
  
  - Badillo Aguilar Diego. 318095909 
  
  - Camacho Martínez Juan Carlos . 318035530
  
  - Constantino Cruz Pablo Giovanni . 318073538
  
  - Juarez Paniagua Cristopher Israel . 318175890
  
  - Salgado Valdés Andrés . 318146094

--- 

# Guía Instalación

Una vez que hayas descargado y descomprimido el Zip. En una ventana del CMD de tu PC.

1. Verifica la instalación de `pip`, el gestor de paquetes oficial de Python:
   ```
   pip --version
   ```

2. Instala `virtualenv` para crear un entorno virtual:
   ```
   pip install virtualenv
   ```

3. Crea un nuevo entorno virtual:
   ```
   python -m venv venv
   ```

4. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```

## Instalación de Dependencias

Con el entorno virtual activado, instala las librerías necesarias mediante `pip`:

```
pip install django
```
```
pip install pillow
```
```
pip install beautifulsoup4
```
```
pip install requests
```
```
pip install tweepy
```
```
pip install stripe
```

### Descripción de las Librerías

- **Django**: Framework para desarrollo web que simplifica tareas comunes.
- **Pillow**: Biblioteca para manipulación de imágenes.
- **BeautifulSoup4**: Herramienta para analizar y extraer datos de documentos HTML/XML.
- **Requests**: Librería para realizar solicitudes HTTP.
- **Tweepy**: Interfaz para interactuar con la API de Twitter.
- **Stripe**: Plataforma para gestionar pagos en línea.

## Ejecución de la Aplicación Web

1. Navega al directorio donde se encuentra el archivo `manage.py`:
   ```bash
   cd Panopticon
   ```
2. Crea las migraciones iniciales para la base de datos:
   ```bash
   python manage.py makemigrations
   ```
3. Aplica las migraciones a la base de datos:
   ```bash
   python manage.py migrate
   ```
4. Crea un superusuario para acceder al panel de administración de Django:
   ```bash
   python manage.py createsuperuser
   ```
5. Opcional: Accede a la base de datos desde la línea de comandos (si es necesario):
   ```bash
   python manage.py dbshell
   ```
6. Inicia el servidor de desarrollo local:
   ```bash
   python manage.py runserver
   ```

7. Accede a la aplicación en tu navegador:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   
   También puedes acceder al panel de administración:
   [http://127.0.0.1:8000/admin/]
---
---






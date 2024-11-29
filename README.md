# NEyW-Proyecto-Final

Integrantes:
  Arellano Hernández Israel . 318251020
  Badillo Aguilar Diego. 318095909 
  Camacho Martínez Juan Carlos . 318035530
  Constantino Cruz Pablo Giovanni . 318073538
  Juarez Paniagua Cristopher Israel . 318175890
  Salgado Valdés Andrés . 318146094

SEMESTRE 2025-1

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
pip install django pillow beautifulsoup4 requests tweepy stripe
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

2. Inicia el servidor de desarrollo local:
   ```bash
   python manage.py runserver
   ```

3. Abre un navegador y accede a la URL proporcionada por la consola, generalmente:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

¡Y eso es todo! Ahora deberías poder visualizar y trabajar con tu aplicación web.
``` 

Este texto es más conciso y profesional, ideal para un repositorio en GitHub. 😊






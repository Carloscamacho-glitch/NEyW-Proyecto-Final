import scrapy

class BuscarPlanSpider(scrapy.Spider):
    name = "buscar_plan"
    
    # URL de la página donde se hará el scraping
    start_urls = ["https://www.spotify.com/mx/premium/?ref=jam"]

    # Palabra que estamos buscando en las etiquetas
    palabra_clave = "Individual"  # Cambia por la palabra que estás buscando

    def parse(self, response):
        # Recorre todas las etiquetas <h3>, <span>, <p>, y otras que puedan contener el texto
        for etiqueta in response.xpath("//h3 | //span | //p | //div"):
            texto = etiqueta.xpath("text()").get()  # Extrae el texto de la etiqueta

            # Si el texto contiene la palabra clave, lo almacenamos
            if texto and self.palabra_clave.lower() in texto.lower():
                # Extraer información relevante: tipo de etiqueta, texto y URL
                item = {
                    "etiqueta": etiqueta.root.tag,  # Tipo de etiqueta (ejemplo: div, h3, etc.)
                    "texto": texto.strip(),         # Texto de la etiqueta
                    "url": response.url,            # URL de la página
                }

                yield item  # Devolvemos el item con la información encontrada

            # También buscar en atributos específicos (por ejemplo, 'data-*', 'title', 'alt', etc.)
            for atributo in etiqueta.xpath("@*").getall():
                if self.palabra_clave.lower() in atributo.lower():
                    item = {
                        "etiqueta": etiqueta.root.tag,  # Tipo de etiqueta (ejemplo: div, h3, etc.)
                        "atributo": atributo,            # Atributo donde se encontró la palabra clave
                        "url": response.url,            # URL de la página
                    }
                    yield item

# WebScrapping ChilePropiedades

## General

Este repositorio es un webscraping del portal ChilePropiedades, la cual contiene información de departamentos y casas en arriendo y venta en Chile. Se puede extraer la información completa de las propiedades, desde el precio hasta su latitud y longitud.

WebScrapping URL: https://chilepropiedades.cl/

## ¿Qué se requiere?

Para poder ejecutar este repositorio, se necesita tener instalado Docker en el computador.

Si no tienes instalado Docker, por favor, descárgalo en el siguiente enlace:

https://www.docker.com/products/docker-desktop/


## ¿Qué contiene el Docker?

El Docker contiene una API con un endpoint en en la ruta "/webscrapping", que permite extraer la información de la página web. Este endpoint recibe 5 variables de entrada:

- **region**: Es la ubicación de la cual se quiere extraer la información. Si se quiere extraer la información por region, sus posibles valores son:
```bash
    Region Metropolitana: Santiago
    Región de Arica y Parinacota: Arica
    Región de Tarapacá: i-region-de-tarapaca
    Región de Atacama: iii-region-de-atacama
    Región de Coquimbo: iv-region-de-coquimbo
    Región de Valparaíso: v-region-de-valparaiso  
    Región del Maule:vii-region-del-maule
    Región del Ñuble: xvi-region-de-nuble
    Región del Biobío:viii-region-del-biobio
    Región de La Araucanía:ix-region-de-la-araucania
    Región de Los Ríos:xiv-region-de-los-rios
    Región de Los Lagos:x-region-de-los-lagos
```

- **type_searching**: Esta variable indica el tipo de búsqueda para extraer la información. Los posibles valores son:
```bash
    Arrendar: arriendo-mensual
    Comprar: venta
    Arriendo Diario: arriendo-diario
```

- **type_house**: Esta variable indica el tipo de propiedad de la consulta. Los posibles valores son:
```bash
    Bodega: Bodega
    Casa: casa
    Departamento: departamento
    Estacionamiento: estacionamiento
    Estudio: estudio
    Hotel: hotel
    Local Comercial: local-comercial
    Loft: loft
    Lote de Cementerio: lote-de-cementerio
    Oficina: oficina
    Parcela: parcela
    Sitio: sitio
    Terreno : terreno
    Terreno Agricola: terreno-agricola
    Terreno Forestal: terreno-forestal
    Terreno Industrial: terreno-industrial
```

- **min_publish_date**: Esta variable indica la fecha mínima de publicación de las propiedades. Su formato es YYYY-MM-DD.
- **max_publish_date**: Esta variable indica la fecha máxima de publicación de las propiedades. Su formato es YYYY-MM-DD.

## ¿Cómo empezar?

Si quiere ejecutar el codigo debe seguir los siguientes pasos:

**Clonar el repositorio**

```bash
git clone https://github.com/Foco22/X-Academy-Project.git
```

**Empezar el Docker**

Para ejecutar el contenedor se debe construir su imagen usando:

```bash
sudo docker build -t my-flask-app .
```

Luego, se debe ejecutar usando:

```bash
sudo docker run -d -p 8000:8000 my-flask-app
```

**¿Cómo ejecutarlo?**

Si se requiere tener acceso al endpoint, se puede utilizar la librería requests en Python, mediante el siguiente código:

```bash
import requests

url = "http://localhost:8000/webscrapping"
data = {
    "region": "santiago",
    "type_searching": "arriendo-mensual",
    "type_house": "departamento",
    "min_publish_date": "2024-05-23",
    "max_publish_date": "2024-05-24"
}
response_body = requests.post(url, json=data)
response_json = response_body.json()
```

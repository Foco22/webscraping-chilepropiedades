import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
import pandas as pd

class GetDataChilePropiedades:

    def __init__(self, region, type_searching, type_house, min_publish_date, max_publish_date):
        self.region = region
        self.type_searching = type_searching
        self.type_house = type_house
        self.min_publish_date = min_publish_date
        self.max_publish_date = max_publish_date

    def getdata(self):

        extracted_data = []
        url = 'https://chilepropiedades.cl/propiedades/{}/{}/{}/0'.format(self.type_searching, self.type_house,self.region)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        element_page = soup.find_all('div', class_='clp-results-text-container d-none d-sm-block col-sm-6 text-right')
        max_count_page = element_page[0].text
        pattern = r"Total de páginas:\s+(\d+)"
        match = re.search(pattern, max_count_page)
        if match:
            total_pages = match.group(1)
        else:
            return {
                'response': extracted_data,
                'status': True
            }

        table_count_page = [i for i in range(int(total_pages))]
        
        for page in table_count_page:
            try:    
                url =   

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                element_page = soup.find_all('p', class_='mt-3 p-3 clp-highlighted-container text-center')
                time.sleep(3)

                if element_page != []:
                    continue

                # Find all the publication elements
                elements = soup.find_all('div', class_='clp-publication-list')
                list_element_public = elements[0].find_all('div', class_='clp-publication-element clp-highlighted-container')


                # Iterate over each publication element
                for element in list_element_public:
                    
                    try:
                        date_publish = element.find('div', class_='text-center clp-publication-date').text.strip()
                        date_publish_datetime = datetime.strptime(date_publish, "%d/%m/%Y")                        
                        date_publish_datetime = str(date_publish_datetime)[:10]
                    except:
                        date_publish_datetime = '1990-01-01'
                    
                    ## Filter by date
                    if (date_publish_datetime >= self.min_publish_date) and (date_publish_datetime <= self.max_publish_date):

                        # Images 
                        try:
                            img_publish_list = element.find('a', class_='clp-listing-image-link')
                            img_element = img_publish_list.find('picture').find('img')['src']
                        except:
                            img_element = ''

                        # Extract rooms
                        try:
                            rooms_span = element.find('span', title='Habitaciones')
                            rooms = rooms_span.find('span', class_='clp-feature-value').text if rooms_span else None
                        except:
                            rooms = 0

                        # Extract bathrooms
                        try:
                            bathrooms_span = element.find('span', title='Baños')
                            bathrooms = bathrooms_span.find('span', class_='clp-feature-value').text if bathrooms_span else None
                        except:
                            bathrooms = 0

                        # Extract value price
                        try:
                            value_spans = element.find_all('span', class_='clp-value-container', attrs={'valueunit': '1'})
                            value_price_clp = value_spans[1].text.strip() if len(value_spans) > 1 else None
                        except:
                            value_price_clp = 0

                        # Extract value currency
                        try:
                            value_spans = element.find_all('span', class_='clp-value-container', attrs={'valueunit': '1'})
                            value_price_currency_clp = value_spans[0].text.strip() if len(value_spans) > 1 else None
                        except:
                            value_price_currency_clp = 0

                        # Extract value price
                        try:
                            value_spans = element.find_all('span', class_='clp-value-container', attrs={'valueunit': '3'})
                            value_price_uf = value_spans[1].text.strip() if len(value_spans) > 1 else None
                        except:
                            value_price_uf = 0

                        # Extract value currency
                        try:
                            value_spans = element.find_all('span', class_='clp-value-container', attrs={'valueunit': '3'})
                            value_price_currency_uf = value_spans[0].text.strip() if len(value_spans) > 1 else None
                        except:
                            value_price_currency_uf = 0

                        # Extract parking lots
                        try:
                            parking_span = element.find('span', title='Estacionamientos')
                            parking = parking_span.find('span', class_='clp-feature-value').text if parking_span else None
                        except:
                            parking = 0  

                        try:
                            h2_element = element.find('h2', class_='publication-title-list')
                            a_tag = h2_element.find('a') if h2_element else None
                            href = a_tag['href'] if a_tag else None
                            url_element = 'https://chilepropiedades.cl' + href
                        except: 
                            url_element = ''      

                        try:
                            data_element = element.find('div', class_='d-md-flex mt-2 align-items-center')
                            data_element = data_element.find('h3', class_='sub-codigo-data').text.split('/')
                            type_action = data_element[0].strip()
                            type_property = data_element[1].strip()
                            type_province = data_element[2].strip()
                        except:
                            type_action = ''
                            type_property = ''
                            type_province = ''

                        # code publication
                        try: 
                            code_publication = element.find('div', class_='d-md-flex mt-2 align-items-center')
                            code_publication = code_publication.find('span', class_='light-bold').next_sibling.strip()
                        except:
                            code_publication = ''

                        # get latitude and longitude
                        response = requests.get(url_element, headers=headers)
                        time.sleep(3)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        script_element = soup.find_all('script')

                        for i in range(len(script_element)):
                            location_pattern = r'var publicationLocation = \[\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\s*\];'
                            matches = re.findall(location_pattern, str(script_element[i]))
                            if matches:
                                latitude, longitude = matches[0] 
                                break
                            else:
                                latitude = None
                                longitude = None

                            # Add to the list
                        extracted_data.append({
                            'rooms': rooms,
                            'bathrooms': bathrooms,
                            'value_price_clp': value_price_clp,
                            'value_price_currency_clp': value_price_currency_clp,
                            'value_price_uf': value_price_uf,
                            'value_price_currency_uf': value_price_currency_uf,
                            'parking': parking,
                            'url': url_element,
                            'type_action': type_action,
                            'type_property': type_property,
                            'type_province': type_province,
                            'latitude': latitude,
                            'longitude': longitude,
                            'page': page,
                            'region': self.region,
                            'type_searching': self.type_searching,
                            'type_house': self.type_house,
                            'date_publish': date_publish,
                            'code_publication': code_publication,
                            'image_picture': img_element,
                            'web': 'chilepropiedades',
                        })
                    elif (date_publish_datetime < self.min_publish_date):
                        return {
                            'response': extracted_data,
                            'status': True
                        }
            except:
                pass
        return {
            'response': extracted_data,
            'status': True
        }



from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse
import services
import requests

app = Flask(__name__)
api = Api(app, version='1.0', title='Web Scraping API', description='A simple Web Scraping API')

# Define the request parser
parser = reqparse.RequestParser()
parser.add_argument('region', type=str, required=True, help='The region to search')
parser.add_argument('type_searching', type=str, required=True, help='The type of search')
parser.add_argument('type_house', type=str, required=True, help='The type of house')
parser.add_argument('min_publish_date', type=str, required=True, help='The minimum publish date')
parser.add_argument('max_publish_date', type=str, required=True, help='The maximum publish date')

def validate_input(data):
    required_fields = ['region', 'type_searching', 'type_house', 'min_publish_date', 'max_publish_date']
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, None

@api.route('/webscrapping')
class WebScrapping(Resource):
    @api.expect(parser)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.response(500, 'Internal Server Error')
    def post(self):
        try:
            data = request.get_json()


            # Validate the input data
            is_valid, error_message = validate_input(data)
            if not is_valid:
                return {'error': error_message}, 400

            region = data.get('region')
            type_searching = data.get('type_searching')
            type_house = data.get('type_house')
            min_publish_date = data.get('min_publish_date')
            max_publish_date = data.get('max_publish_date')

            # Create an instance of GetDataChilePropiedades
            get_data_instance = services.GetDataChilePropiedades(
                region=region,
                type_searching=type_searching,
                type_house=type_house,
                min_publish_date=min_publish_date,
                max_publish_date=max_publish_date
            )

            # Call the method to get data
            response = get_data_instance.getdata()
            if response['status'] == True:
                return response, 200
            else:
                return {'error': 'Error fetching data'}, 500

        except KeyError as e:
            return {'error': f'Missing key: {str(e)}'}, 400

        except Exception as e:
            return {'error': f'Missing key: {str(e)}'}, 400
        

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)


from flask import Flask, request, jsonify

from geo import get_nearby_hotels
from profile import *
from rate import get_rates


app = Flask(__name__)


@app.route('/hotels', methods=['GET'])
def get_hotels():
    # Parse the HTTP request
    in_date = request.args.get('inDate')
    out_date = request.args.get('outDate')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    # Call the geo function
    hotel_ids = get_nearby_hotels(lat, lon)

    # Fetch rate information
    rate_results = get_rates(hotel_ids, in_date, out_date)

    # Using only the hotel IDs for the profile service
    rate_hotel_ids = [ratePlan.hotelId for ratePlan in rate_results.ratePlans]

    # Call the profile function
    profile_results = get_hotel_profiles(rate_hotel_ids)

    # Convert the REST API response to a desired JSON format
    hotels = [{
        'id': hotel['id'],
        'coordinates': {'lat': hotel['address']['lat'], 'lon': hotel['address']['lon']},
        'properties': {'name': hotel['name'], 'phone_number': hotel['phoneNumber']}
    } for hotel in profile_results]

    return jsonify(hotels)


if __name__ == "__main__":
    app.run(port=5000)
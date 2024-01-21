import googlemaps
from datetime import datetime
import random

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

def get_directions(origin, destination):
    # Get directions from the origin to the destination
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())
    return directions_result

def calculate_energy_consumption(distance_km, efficiency_kwh_per_km):
    # Calculate energy consumption based on distance and vehicle efficiency
    energy_consumption_kwh = distance_km * efficiency_kwh_per_km
    return energy_consumption_kwh

def main():
    # Auckland city coordinates (you can adjust these coordinates)
    auckland_coordinates = (-36.8485, 174.7633)

    # Define the electric vehicle's efficiency (kWh per km)
    efficiency_kwh_per_km = 0.2  # Adjust this based on the vehicle's specifications

    # Number of random directions to generate
    num_directions = 5

    for _ in range(num_directions):
        # Generate random destination coordinates within Auckland city
        dest_latitude = auckland_coordinates[0] + random.uniform(-0.1, 0.1)
        dest_longitude = auckland_coordinates[1] + random.uniform(-0.1, 0.1)

        destination = (dest_latitude, dest_longitude)

        # Get directions from the current location to the destination
        directions_result = get_directions(auckland_coordinates, destination)

        # Extract distance and duration from the directions result
        distance_km = directions_result[0]['legs'][0]['distance']['value'] / 1000.0
        duration_seconds = directions_result[0]['legs'][0]['duration']['value']

        # Calculate energy consumption for the trip
        energy_consumption = calculate_energy_consumption(distance_km, efficiency_kwh_per_km)

        print(f"Destination: {destination}")
        print(f"Distance: {distance_km:.2f} km")
        print(f"Duration: {duration_seconds // 60} minutes")
        print(f"Energy Consumption: {energy_consumption:.2f} kWh\n")

if __name__ == "__main__":
    main()

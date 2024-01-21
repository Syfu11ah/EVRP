import googlemaps
from datetime import datetime

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
api_key = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=api_key)

def get_directions(origin, destination):
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())
    return directions_result[0]['legs'][0]['steps']

def calculate_energy_consumption(distance):
    # Replace this with your own energy consumption model
    # Example: 0.2 kWh per mile
    energy_consumption_per_mile = 0.2
    return distance * energy_consumption_per_mile

def main():
    # List of destinations (latitude, longitude)
    destinations = [
        (37.7749, -122.4194),  # San Francisco, CA
        (34.0522, -118.2437),  # Los Angeles, CA
        # Add more destinations as needed
    ]

    total_energy_consumption = 0.0

    for i in range(len(destinations) - 1):
        origin = destinations[i]
        destination = destinations[i + 1]

        # Get directions between two points
        steps = get_directions(origin, destination)

        # Calculate total distance for the route
        total_distance = sum(step['distance']['value'] for step in steps) / 1000.0  # Convert meters to kilometers

        # Calculate energy consumption for the route
        energy_consumption = calculate_energy_consumption(total_distance)
        total_energy_consumption += energy_consumption

        print(f"Route {i+1}:")
        print(f"  Distance: {total_distance:.2f} km")
        print(f"  Energy Consumption: {energy_consumption:.2f} kWh")
        print()

    print(f"Total Energy Consumption for all routes: {total_energy_consumption:.2f} kWh")

if __name__ == "__main__":
    main()

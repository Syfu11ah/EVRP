import googlemaps
from geopy.distance import geodesic

# Set your Google Maps API key
API_KEY = 'your_api_key'
gmaps = googlemaps.Client(key=API_KEY)

def calculate_distance(origin, destination):
    return geodesic(origin, destination).km

def calculate_energy_consumption(distance):
    # Your energy consumption calculation logic goes here
    # This could involve the specific characteristics of your electric vehicle
    # For simplicity, let's assume a constant energy consumption rate for now
    energy_consumption_rate = 0.2  # kWh per km
    return distance * energy_consumption_rate

def main():
    # Specify the list of destinations
    destinations = [
        "Auckland, New Zealand",
        "Destination 1, Auckland",
        "Destination 2, Auckland",
        # Add more destinations as needed
    ]

    # Get the coordinates for each destination
    coordinates = [gmaps.geocode(dest)[0]['geometry']['location'] for dest in destinations]

    total_energy_consumed = 0.0

    # Iterate through each destination
    for i in range(len(coordinates) - 1):
        origin = coordinates[i]
        destination = coordinates[i + 1]

        # Calculate distance between current and next destination
        distance = calculate_distance((origin['lat'], origin['lng']), (destination['lat'], destination['lng']))

        # Calculate energy consumption for the segment
        energy_consumption = calculate_energy_consumption(distance)

        print(f"Segment {i+1}: Distance - {distance:.2f} km, Energy Consumption - {energy_consumption:.2f} kWh")

        # Accumulate total energy consumption
        total_energy_consumed += energy_consumption

    print(f"Total Energy Consumption: {total_energy_consumed:.2f} kWh")

if __name__ == "__main__":
    main()

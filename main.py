import googlemaps
from datetime import datetime

def get_directions(api_key, origin, destinations):
    gmaps = googlemaps.Client(key=api_key)

    directions_result = gmaps.directions(
        origin,
        destinations,
        mode="driving",
        departure_time=datetime.now()
    )

    return directions_result

def calculate_energy_consumption(distance_km, efficiency_kWh_per_km):
    energy_consumption_kWh = distance_km * efficiency_kWh_per_km
    return energy_consumption_kWh

def main():
    # Replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual API key
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    
    # Example destinations
    origin = "Start Location"
    destinations = ["Destination 1", "Destination 2", "Destination 3"]

    # Example electric vehicle energy consumption model
    efficiency_kWh_per_km = 0.2  # Adjust this based on your electric vehicle's specifications

    # Get directions
    directions_result = get_directions(api_key, origin, destinations)

    total_distance_km = 0

    # Calculate energy consumption for each leg of the journey
    for leg in directions_result[0]['legs']:
        distance_km = leg['distance']['value'] / 1000.0
        total_distance_km += distance_km

        energy_consumption_kWh = calculate_energy_consumption(distance_km, efficiency_kWh_per_km)

        print(f"Leg: {leg['start_address']} to {leg['end_address']}")
        print(f"Distance: {distance_km:.2f} km")
        print(f"Energy Consumption: {energy_consumption_kWh:.2f} kWh")
        print("-----------------------------")

    print(f"Total Distance: {total_distance_km:.2f} km")

if __name__ == "__main__":
    main()

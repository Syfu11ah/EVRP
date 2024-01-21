import googlemaps
from datetime import datetime

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

def calculate_energy_consumption(start_location, waypoints, vehicle_efficiency):
    total_energy_consumption = 0.0

    for i in range(len(waypoints) - 1):
        # Get directions between waypoints
        directions_result = gmaps.directions(
            waypoints[i],
            waypoints[i + 1],
            mode="driving",
            departure_time=datetime.now(),
            avoid="ferries",
        )

        # Extract distance in meters from the directions result
        distance_in_meters = directions_result[0]['legs'][0]['distance']['value']

        # Convert distance from meters to kilometers
        distance_in_kilometers = distance_in_meters / 1000.0

        # Calculate energy consumption using the formula: Energy = Distance * Efficiency
        energy_consumption = distance_in_kilometers * vehicle_efficiency
        total_energy_consumption += energy_consumption

    return total_energy_consumption

if __name__ == "__main__":
    # Define the starting location and waypoints
    start_location = "-36.8536054,174.7616096"
    waypoints = [
        "destination_lat1,destination_long1",
        "destination_lat2,destination_long2",
        # Add more waypoints as needed
    ]

    # Vehicle efficiency in kWh per kilometer
    vehicle_efficiency = 0.2  # Change this value based on your specific vehicle

    # Calculate total energy consumption
    total_energy = calculate_energy_consumption(start_location, waypoints, vehicle_efficiency)

    print(f"Total energy consumption: {total_energy:.2f} kWh")

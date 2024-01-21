import googlemaps
from datetime import datetime

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

def calculate_energy_consumption(start_location, waypoints, vehicle_efficiency, motor_efficiency, battery_capacity):
    total_energy_consumption = 0.0
    remaining_battery_capacity = battery_capacity

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

        # Adjust energy consumption for electric motor efficiency
        energy_consumption /= motor_efficiency

        # Check if there is enough battery capacity for the trip
        if remaining_battery_capacity >= energy_consumption:
            remaining_battery_capacity -= energy_consumption
        else:
            print("Insufficient battery capacity for the trip.")
            return None

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

    # Electric vehicle parameters
    vehicle_efficiency = 0.2  # kWh per kilometer
    motor_efficiency = 0.9  # Electric motor efficiency
    battery_capacity = 60.0  # kWh, replace with your vehicle's actual battery capacity

    # Calculate total energy consumption
    total_energy = calculate_energy_consumption(start_location, waypoints, vehicle_efficiency, motor_efficiency, battery_capacity)

    if total_energy is not None:
        print(f"Total energy consumption: {total_energy:.2f} kWh")

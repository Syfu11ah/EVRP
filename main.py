import googlemaps
from datetime import datetime

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

def get_elevation(location):
    # Get elevation from Google Maps Elevation API
    elevation_result = gmaps.elevation((location['lat'], location['lng']))
    return elevation_result[0]['elevation']

def calculate_energy_consumption(start_location, waypoints, motor_efficiency, battery_capacity):
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

        # Estimate road inclination using start and end location elevations
        start_location_dict = directions_result[0]['legs'][0]['start_location']
        end_location_dict = directions_result[0]['legs'][0]['end_location']
        
        start_elevation = get_elevation(start_location_dict)
        end_elevation = get_elevation(end_location_dict)
        road_inclination = (end_elevation - start_elevation) / distance_in_kilometers

        # Adjust energy consumption for motor efficiency, battery capacity, and road inclination
        energy_consumption = (distance_in_kilometers / motor_efficiency) * battery_capacity * (1 + road_inclination)

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
    start_location = {"lat": -36.8536054, "lng": 174.7616096}
    waypoints = [
        {"lat": destination_lat1, "lng": destination_long1},
        {"lat": destination_lat2, "lng": destination_long2},
        # Add more waypoints as needed
    ]

    # Electric vehicle motor and battery parameters
    motor_efficiency = 0.9  # Electric motor efficiency
    battery_capacity = 60.0  # kWh, replace with your vehicle's actual battery capacity

    # Calculate total energy consumption
    total_energy = calculate_energy_consumption(start_location, waypoints, motor_efficiency, battery_capacity)

    if total_energy is not None:
        print(f"Total energy consumption: {total_energy:.2f} kWh")

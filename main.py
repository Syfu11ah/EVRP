import googlemaps
from datetime import datetime
import random

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

def get_directions(origin, destination):
    # Get directions from the origin to the destination with the "shortest" option
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now(), optimize_waypoints=True)
    return directions_result

def calculate_energy_consumption(distance_km, motor_efficiency, battery_efficiency):
    # Assuming a linear relationship between distance and energy consumption
    motor_energy_consumption_kwh = distance_km / motor_efficiency
    battery_energy_consumption_kwh = motor_energy_consumption_kwh / battery_efficiency

    return motor_energy_consumption_kwh, battery_energy_consumption_kwh

def main():
    # Auckland city coordinates (you can adjust these coordinates)
    auckland_coordinates = (-36.8485, 174.7633)

    # Define the electric vehicle's parameters
    motor_efficiency = 0.2  # Efficiency of the electric motor (kWh per km)
    battery_efficiency = 0.9  # Efficiency of the battery (percentage)

    # Battery capacity in kWh
    battery_capacity_kwh = 100.0  # Adjust this based on the vehicle's battery capacity

    # Initialize the starting point as Auckland coordinates
    current_location = auckland_coordinates

    # Initialize the initial battery level to 100%
    current_battery_level = battery_capacity_kwh

    # Continue driving until the battery drops below 20%
    while current_battery_level > 20:
        # Generate random destination coordinates within Auckland city
        dest_latitude = current_location[0] + random.uniform(-0.1, 0.1)
        dest_longitude = current_location[1] + random.uniform(-0.1, 0.1)

        destination = (dest_latitude, dest_longitude)

        # Get directions from the current location to the destination
        directions_result = get_directions(current_location, destination)

        # Extract distance and duration from the directions result
        distance_km = directions_result[0]['legs'][0]['distance']['value'] / 1000.0
        duration_seconds = directions_result[0]['legs'][0]['duration']['value']

        # Calculate energy consumption for the trip
        motor_energy_consumption, battery_energy_consumption = calculate_energy_consumption(
            distance_km, motor_efficiency, battery_efficiency
        )

        # Update the battery level
        current_battery_level -= battery_energy_consumption

        print(f"Start Location: {current_location}")
        print(f"Destination: {destination}")
        print(f"Distance: {distance_km:.2f} km")
        print(f"Duration: {duration_seconds // 60} minutes")
        print(f"Motor Energy Consumption: {motor_energy_consumption:.2f} kWh")
        print(f"Battery Energy Consumption: {battery_energy_consumption:.2f} kWh")
        print(f"Battery Level: {current_battery_level:.2f} kWh\n")

        # Update the current location for the next iteration
        current_location = destination

if __name__ == "__main__":
    main()

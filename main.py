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

def calculate_energy_consumption(vehicle_mass, acceleration, road_angle, distance, wind_speed=0.0, front_area=2.5, rolling_resistance=0.01, air_density=1.225, drag_coefficient=0.3):
    # Constants
    gravity = 9.8

    # Convert velocity from km/h to m/s
    velocity = distance / 1000.0  # Assuming constant speed

    # Change in height considering road angle
    height_change = distance * road_angle

    # Rolling resistance force
    rolling_resistance_force = vehicle_mass * gravity * rolling_resistance

    # Aerodynamic drag force
    drag_force = 0.5 * air_density * drag_coefficient * front_area * velocity**2

    # Total force
    total_force = rolling_resistance_force + drag_force

    # Energy consumption (in joules)
    energy_consumption_joules = 0.5 * vehicle_mass * velocity**2 + vehicle_mass * gravity * height_change + total_force * distance

    # Convert energy consumption to kilowatt-hours
    energy_consumption_kwh = energy_consumption_joules / 3600000.0

    return energy_consumption_kwh

def main():
    # Auckland city coordinates (you can adjust these coordinates)
    auckland_coordinates = (-36.8485, 174.7633)

    # Electric vehicle parameters
    vehicle_mass = 1500  # in kg
    acceleration = 0.1  # in m/s^2
    road_angle = 0.05  # 5% road incline

    # Battery capacity in kilowatt-hours
    battery_capacity_kwh = 100.0  # Adjust this based on the vehicle's battery capacity

    # Initialize the starting point as Auckland coordinates
    current_location = auckland_coordinates

    # Initialize the initial battery level to 100%
    current_battery_level_kwh = battery_capacity_kwh

    # Continue driving until the battery drops below 20%
    while current_battery_level_kwh > 0.2 * battery_capacity_kwh:
        # Generate random destination coordinates within Auckland city
        dest_latitude = current_location[0] + random.uniform(-0.1, 0.1)
        dest_longitude = current_location[1] + random.uniform(-0.1, 0.1)

        destination = (dest_latitude, dest_longitude)

        # Get directions from the current location to the destination
        directions_result = get_directions(current_location, destination)

        # Extract distance and duration from the directions result
        distance_km = directions_result[0]['legs'][0]['distance']['value'] / 1000.0

        # Calculate energy consumption for the trip
        energy_consumption_kwh = calculate_energy_consumption(
            vehicle_mass, acceleration, road_angle, distance_km
        )

        # Update the battery level
        current_battery_level_kwh -= energy_consumption_kwh

        print(f"Start Location: {current_location}")
        print(f"Destination: {destination}")
        print(f"Distance: {distance_km:.2f} km")
        print(f"Energy Consumption: {energy_consumption_kwh:.2f} kWh")
        print(f"Battery Level: {current_battery_level_kwh:.2f} kWh\n")

        # Update the current location for the next iteration
        current_location = destination

if __name__ == "__main__":
    main()

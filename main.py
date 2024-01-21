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

def calculate_energy_consumption(
    distance_km,
    efficiency_kwh_per_km,
    vehicle_mass_kg,
    mass_factor,
    acceleration,
    coefficient_of_rolling,
    air_density,
    front_area,
    aerodynamic_drag,
    wind_speed,
    road_angle,
):
    # Constants
    gravity = 9.81  # m/s^2, acceleration due to gravity

    # Convert distance to meters
    distance_meters = distance_km * 1000.0

    # Calculate energy consumption based on various factors
    energy_consumption_kwh = (
        efficiency_kwh_per_km
        + (0.5 * vehicle_mass_kg * acceleration**2) / mass_factor
        + vehicle_mass_kg * gravity * distance_meters * coefficient_of_rolling
        + 0.5 * air_density * front_area * aerodynamic_drag * wind_speed**2 * distance_meters
        + vehicle_mass_kg * gravity * distance_meters * road_angle
    )

    return energy_consumption_kwh
# Adjust these values based on the vehicle's specifications
vehicle_mass_kg = 1500.0
mass_factor = 1.2
acceleration = 0.5  # m/s^2
coefficient_of_rolling = 0.01
air_density = 1.225  # kg/m^3
front_area = 2.0  # m^2
aerodynamic_drag = 0.3
wind_speed = 0.0  # m/s (assuming no wind for simplicity)
road_angle = 0.0  # degrees (assuming flat road for simplicity)

# Calculate energy consumption for the trip
energy_consumption = calculate_energy_consumption(
    distance_km,
    efficiency_kwh_per_km,
    vehicle_mass_kg,
    mass_factor,
    acceleration,
    coefficient_of_rolling,
    air_density,
    front_area,
    aerodynamic_drag,
    wind_speed,
    road_angle,
)

def main():
    # Auckland city coordinates (you can adjust these coordinates)
    auckland_coordinates = (-36.8485, 174.7633)

    # Define the electric vehicle's efficiency (kWh per km)
    efficiency_kwh_per_km = 0.2  # Adjust this based on the vehicle's specifications

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
        energy_consumption = calculate_energy_consumption(distance_km, efficiency_kwh_per_km)

        # Update the battery level
        current_battery_level -= energy_consumption

        print(f"Start Location: {current_location}")
        print(f"Destination: {destination}")
        print(f"Distance: {distance_km:.2f} km")
        print(f"Duration: {duration_seconds // 60} minutes")
        print(f"Energy Consumption: {energy_consumption:.2f} kWh")
        print(f"Battery Level: {current_battery_level:.2f} kWh\n")

        # Update the current location for the next iteration
        current_location = destination

if __name__ == "__main__":
    main()

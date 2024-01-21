import googlemaps
import csv
from datetime import datetime
import random

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
api_key = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=api_key)

class BatteryModule:
    def __init__(self, capacity, initial_soc):
        self.capacity = capacity  # kWh
        self.soc = initial_soc  # Initial state of charge in percentage

    def charge(self, energy):
        # Charge the battery
        self.soc = min(100, self.soc + (energy / self.capacity) * 100)

    def discharge(self, energy):
        # Discharge the battery
        self.soc = max(0, self.soc - (energy / self.capacity) * 100)

class ElectricMotor:
    def __init__(self, efficiency):
        self.efficiency = efficiency  # Efficiency of the electric motor

    def consume_energy(self, energy):
        # Consume energy from the battery
        return energy / self.efficiency

def get_directions(origin, destination):
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())
    return directions_result[0]['legs'][0]['steps']

def get_elevation(profile):
    elevation_result = gmaps.elevation(profile)
    return elevation_result[0]['elevation']

def get_energy_consumption_data(origin, destination):
    # This is a placeholder function; replace it with a call to your energy consumption data source
    # For example, you might use an electric vehicle API, database, or model
    # Return the energy consumption data in kWh
    # Example: return 30.0
    return 30.0

def calculate_energy_consumption(distance, motor, energy_consumption_data, battery_module, inclination_factor):
    # Calculate energy consumption for the route considering inclination
    energy_consumption = distance * (1 + inclination_factor) * energy_consumption_data

    # Discharge the battery after adjusting for motor efficiency
    energy_consumed_by_motor = motor.consume_energy(energy_consumption)
    battery_module.discharge(energy_consumed_by_motor)

    return energy_consumption, energy_consumed_by_motor

def generate_random_destination():
    # Generate random latitude and longitude for a destination
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    return latitude, longitude

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Route', 'Distance (km)', 'Energy Consumption (kWh)', 'Energy Consumed by Motor (kWh)', 'Remaining Battery Capacity (%)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    # Starting location point
    starting_location = (-36.8536054, 174.7616096)

    # Electric vehicle specifications
    motor_efficiency = 0.9  # Example: 90%
    battery_capacity = 60.0  # Example: 60 kWh
    initial_soc = 100.0  # Initial state of charge in percentage

    motor = ElectricMotor(motor_efficiency)
    battery_module = BatteryModule(battery_capacity, initial_soc)

    battery_threshold = 20.0  # Battery threshold to stop driving (percentage)

    data = []

    while battery_module.soc > battery_threshold:
        # Generate a random destination
        destination = generate_random_destination()

        # Get directions between the current location and the random destination
        steps = get_directions(starting_location, destination)

        inclination_factor = 0.0

        for step in steps:
            # Calculate inclination factor for each step
            profile = [(step['start_location']['lat'], step['start_location']['lng']),
                       (step['end_location']['lat'], step['end_location']['lng'])]
            elevation_start = get_elevation(profile[:1])
            elevation_end = get_elevation(profile[1:])
            inclination_factor += max(0, (elevation_end - elevation_start) / (step['distance']['value'] / 1000.0))

        inclination_factor /= len(steps)

        # Calculate total distance for the route
        total_distance = sum(step['distance']['value'] for step in steps) / 1000.0  # Convert meters to kilometers

        # Retrieve energy consumption data from an external source
        energy_consumption_data = get_energy_consumption_data(starting_location, destination)

        # Calculate energy consumption for the route considering inclination
        energy_consumption, energy_consumed_by_motor = calculate_energy_consumption(
            total_distance, motor, energy_consumption_data, battery_module, inclination_factor
        )

        route_data = {
            'Route': len(data) + 1,
            'Distance (km)': total_distance,
            'Energy Consumption (kWh)': energy_consumption,
            'Energy Consumed by Motor (kWh)': energy_consumed_by_motor,
            'Remaining Battery Capacity (%)': battery_module.soc
        }

        data.append(route_data)

        print(f"Route {len(data)}:")
        print(f"  Distance: {total_distance:.2f} km")
        print(f"  Energy Consumption: {energy_consumption:.2f} kWh")
        print(f"  Energy Consumed by Motor: {energy_consumed_by_motor:.2f} kWh")
        print(f"  Remaining Battery Capacity: {battery_module.soc:.2f}%")
        print()

    print(f"Total Energy Consumption for all routes: {sum(route['Energy Consumption (kWh)'] for route in data):.2f} kWh")

    # Save data to CSV file
    save_to_csv(data, 'energy_consumption_data.csv')

if __name__ == "__main__":
    main()

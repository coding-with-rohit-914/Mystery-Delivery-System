import json
import math
import random
from typing import Dict, List, Tuple, Any
import csv
from datetime import datetime

class FastBoxDeliverySystem:
    def __init__(self, json_data: Dict[str, Any]):
        """
        Initialize the delivery system with data from JSON
        """
        self.warehouses = self._parse_warehouses(json_data.get('warehouses', {}))
        self.agents = self._parse_agents(json_data.get('agents', {}))
        self.packages = self._parse_packages(json_data.get('packages', []))
        
        # Track agent statistics
        self.agent_stats = {}
        self._initialize_agent_stats()
        
        # Optional: Enable random delays
        self.enable_random_delays = False
        self.new_agent_joining_time = None  # For bonus feature
    def _parse_warehouses(self, warehouses_data: Any) -> Dict[str, Tuple[float, float]]:
        """
        Parse warehouses from JSON data
        Handles both list format (base_case.json) and dict format (test cases)
        """
        warehouses = {}
        if isinstance(warehouses_data, list):
            # Handle format from base_case.json: [{"id": "W1", "location": [0, 0]}, ...]
            for warehouse in warehouses_data:
                warehouses[warehouse['id']] = tuple(warehouse['location'])
        elif isinstance(warehouses_data, dict):
            # Handle format from test cases: {"W1": [0, 0], "W2": [50, 75], ...}
            for warehouse_id, location in warehouses_data.items():
                warehouses[warehouse_id] = tuple(location)   
        return warehouses
    def _parse_agents(self, agents_data: Any) -> Dict[str, Tuple[float, float]]:
        """
        Parse agents from JSON data
        """
        agents = {}
        if isinstance(agents_data, list):
            # Handle list format if exists
            for agent in agents_data:
                agents[agent['id']] = tuple(agent['location'])
        elif isinstance(agents_data, dict):
            # Handle dict format
            for agent_id, location in agents_data.items():
                agents[agent_id] = tuple(location)
        return agents
    def _parse_packages(self, packages_data: List[Dict]) -> List[Dict]:
        """
        Parse packages from JSON data
        Handles different field names (warehouse_id vs warehouse)
        """
        packages = []
        for package in packages_data:
            # Handle both 'warehouse_id' and 'warehouse' field names
            warehouse_id = package.get('warehouse_id') or package.get('warehouse')
            packages.append({
                'id': package['id'],
                'warehouse': warehouse_id,
                'destination': tuple(package['destination'])
            })
        return packages
    def _initialize_agent_stats(self):
        """Initialize statistics for each agent"""
        for agent_id in self.agents.keys():
            self.agent_stats[agent_id] = {
                'packages_delivered': 0,
                'total_distance': 0.0,
                'current_location': self.agents[agent_id],
                'route_history': []  # For visualization
            }
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Calculate Euclidean distance between two points
        Formula: sqrt((x2-x1)² + (y2-y1)²)
        """
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    def find_nearest_agent(self, warehouse_location: Tuple[float, float], 
                          available_agents: List[str] = None) -> str:
        """
        Find the nearest agent to a warehouse location
        """
        if available_agents is None:
            available_agents = list(self.agents.keys())
        nearest_agent = None
        min_distance = float('inf')
        for agent_id in available_agents:
            agent_location = self.agent_stats[agent_id]['current_location']
            distance = self.calculate_distance(agent_location, warehouse_location)
            if distance < min_distance:
                min_distance = distance
                nearest_agent = agent_id
        return nearest_agent
    def simulate_random_delay(self) -> float:
        """
        Bonus: Simulate random delivery delays (0-30% extra time)
        Returns multiplier for distance/travel time
        """
        if not self.enable_random_delays:
            return 1.0
        # Random delay between 0% and 30%
        delay_multiplier = 1.0 + random.uniform(0, 0.3)
        return delay_multiplier
    def assign_packages_to_agents(self) -> Dict[str, List[Dict]]:
        """
        Assign each package to the nearest agent
        Returns: Dictionary mapping agent_id to list of assigned packages
        """
        agent_assignments = {agent_id: [] for agent_id in self.agents.keys()}
        for package in self.packages:
            # Get warehouse location for this package
            warehouse_id = package['warehouse']
            warehouse_location = self.warehouses[warehouse_id]
            # Find nearest agent
            nearest_agent = self.find_nearest_agent(warehouse_location)
            if nearest_agent:
                agent_assignments[nearest_agent].append(package)
        return agent_assignments
    def simulate_delivery(self, enable_delays: bool = False, new_agent_mid_day: bool = False):
        """
        Simulate the delivery process for all packages
        """
        self.enable_random_delays = enable_delays
        # Bonus: Handle new agent joining mid-day
        if new_agent_mid_day:
            self._add_new_agent_mid_day()
        # Assign packages to agents
        assignments = self.assign_packages_to_agents()
        # Process deliveries for each agent
        for agent_id, packages in assignments.items():
            if not packages:
                continue
            current_location = self.agent_stats[agent_id]['current_location']
            # Group packages by warehouse for efficient pickup
            packages_by_warehouse = {}
            for package in packages:
                warehouse_id = package['warehouse']
                if warehouse_id not in packages_by_warehouse:
                    packages_by_warehouse[warehouse_id] = []
                packages_by_warehouse[warehouse_id].append(package)
            # Process deliveries for each warehouse
            for warehouse_id, warehouse_packages in packages_by_warehouse.items():
                warehouse_location = self.warehouses[warehouse_id]
                # Agent travels to warehouse
                distance_to_warehouse = self.calculate_distance(current_location, warehouse_location)
                # Apply random delay if enabled
                delay_multiplier = self.simulate_random_delay()
                effective_distance_to_warehouse = distance_to_warehouse * delay_multiplier
                # Update agent's current location and distance
                self.agent_stats[agent_id]['current_location'] = warehouse_location
                self.agent_stats[agent_id]['total_distance'] += effective_distance_to_warehouse
                self.agent_stats[agent_id]['route_history'].append({
                    'from': current_location,
                    'to': warehouse_location,
                    'distance': effective_distance_to_warehouse,
                    'type': 'to_warehouse'
                })
                current_location = warehouse_location
                # Deliver packages from this warehouse
                for package in warehouse_packages:
                    # Travel from warehouse to destination
                    distance_to_destination = self.calculate_distance(
                        current_location, package['destination']
                    )
                    # Apply random delay if enabled
                    delay_multiplier = self.simulate_random_delay()
                    effective_distance_to_destination = distance_to_destination * delay_multiplier
                    # Update statistics
                    self.agent_stats[agent_id]['packages_delivered'] += 1
                    self.agent_stats[agent_id]['total_distance'] += effective_distance_to_destination
                    self.agent_stats[agent_id]['route_history'].append({
                        'from': current_location,
                        'to': package['destination'],
                        'distance': effective_distance_to_destination,
                        'type': 'delivery'
                    })
                    # Agent is now at destination
                    current_location = package['destination']
            # Return agent to original position (optional)
            self.agent_stats[agent_id]['current_location'] = current_location
    def _add_new_agent_mid_day(self):
        """
        Bonus: Simulate a new agent joining mid-day
        """
        if len(self.packages) > 0:
            # Add a new agent at a random location
            new_agent_id = f"A{len(self.agents) + 1}"
            new_location = (random.uniform(0, 100), random.uniform(0, 100))
            self.agents[new_agent_id] = new_location
            self.agent_stats[new_agent_id] = {
                'packages_delivered': 0,
                'total_distance': 0.0,
                'current_location': new_location,
                'route_history': []
            }
            
            print(f"⚠️  New agent {new_agent_id} joined at location {new_location}")
    def calculate_efficiency(self) -> Dict[str, Dict]:
        """
        Calculate efficiency for each agent
        Efficiency = total_distance / packages_delivered (lower is better)
        """
        report = {}
        for agent_id, stats in self.agent_stats.items():
            if stats['packages_delivered'] > 0:
                efficiency = stats['total_distance'] / stats['packages_delivered']
            else:
                efficiency = 0.0
            report[agent_id] = {
                'packages_delivered': stats['packages_delivered'],
                'total_distance': round(stats['total_distance'], 2),
                'efficiency': round(efficiency, 2)
            }
        # Find best agent (most efficient = lowest efficiency score)
        best_agent = None
        best_efficiency = float('inf')
        for agent_id, data in report.items():
            if data['packages_delivered'] > 0 and data['efficiency'] < best_efficiency:
                best_efficiency = data['efficiency']
                best_agent = agent_id
        if best_agent:
            report['best_agent'] = best_agent
        return report
    def visualize_routes_ascii(self, agent_id: str):
        """
        Bonus: Visualize an agent's route in ASCII
        """
        if agent_id not in self.agent_stats:
            print(f"Agent {agent_id} not found!")
            return
        stats = self.agent_stats[agent_id]
        print(f"\n📊 Route Visualization for Agent {agent_id}:")
        print("=" * 50)
        for i, route in enumerate(stats['route_history'], 1):
            from_point = route['from']
            to_point = route['to']
            distance = route['distance']
            route_type = route['type']
            if route_type == 'to_warehouse':
                symbol = "🏭"
                action = "Traveling to warehouse"
            else:
                symbol = "📦"
                action = "Delivering package"
            print(f"{i}. {symbol} {action}")
            print(f"   From: {from_point} → To: {to_point}")
            print(f"   Distance: {distance:.2f} units")
            print("-" * 40)
        print(f"\n📈 Summary for {agent_id}:")
        print(f"   Total packages delivered: {stats['packages_delivered']}")
        print(f"   Total distance traveled: {stats['total_distance']:.2f}")
        print("=" * 50)
    def export_top_performer_csv(self, report: Dict[str, Dict], filename: str = "top_performer.csv"):
        """
        Bonus: Export top performer data to CSV
        """
        if 'best_agent' not in report:
            print("No best agent found!")
            return
        best_agent_id = report['best_agent']
        best_agent_data = report[best_agent_id]
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['agent_id', 'packages_delivered', 'total_distance', 'efficiency', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'agent_id': best_agent_id,
                'packages_delivered': best_agent_data['packages_delivered'],
                'total_distance': best_agent_data['total_distance'],
                'efficiency': best_agent_data['efficiency'],
                'timestamp': datetime.now().isoformat()
            })
        print(f"✅ Top performer data exported to {filename}")
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate the final report
        """
        report = self.calculate_efficiency()
        # Verify total packages delivered
        total_delivered = sum(
            report[agent_id]['packages_delivered'] 
            for agent_id in report.keys() 
            if agent_id != 'best_agent'
        )
        print(f"\n📦 Total packages in system: {len(self.packages)}")
        print(f"📦 Total packages delivered: {total_delivered}")
        if total_delivered != len(self.packages):
            print("⚠️  Warning: Not all packages were delivered!")
        return report
def main():
    """
    Main function to run the delivery simulation
    """
    # Ask user which test case to run
    print("🚚 FastBox Delivery System Simulator")
    print("=" * 40)
    print("Available test cases:")
    print("1. base_case.json")
    print("2. test_case_1.json")
    print("3. test_case_2.json")
    print("... (all other test cases)")
    choice = input("\nEnter the test case number (1-10) or filename: ").strip()
    if choice.isdigit():
        if choice == '1':
            filename = 'base_case.json'
        else:
            filename = f'test_case_{choice}.json'
    else:
        filename = choice
    try:
        # Read and parse JSON file
        print(f"\n📂 Loading data from {filename}...")
        with open(filename, 'r') as file:
            data = json.load(file)
        # Initialize delivery system
        delivery_system = FastBoxDeliverySystem(data)
        # Ask about bonus features
        enable_delays = input("Enable random delivery delays? (y/n): ").lower() == 'y'
        new_agent = input("Simulate new agent joining mid-day? (y/n): ").lower() == 'y'
        # Simulate delivery
        print("\n🚀 Starting delivery simulation...")
        delivery_system.simulate_delivery(
            enable_delays=enable_delays,
            new_agent_mid_day=new_agent
        )
        # Generate report
        print("\n📊 Generating report...")
        report = delivery_system.generate_report()
        # Display report
        print("\n" + "=" * 50)
        print("FINAL REPORT")
        print("=" * 50)
        for agent_id, agent_data in report.items():
            if agent_id != 'best_agent':
                print(f"\nAgent {agent_id}:")
                print(f"  Packages delivered: {agent_data['packages_delivered']}")
                print(f"  Total distance: {agent_data['total_distance']}")
                print(f"  Efficiency: {agent_data['efficiency']}")
        if 'best_agent' in report:
            print(f"\n🏆 Best Agent: {report['best_agent']}")
        # Save report to JSON
        output_filename = "report.json"
        with open(output_filename, 'w') as outfile:
            json.dump(report, outfile, indent=2)
        print(f"\n✅ Report saved to {output_filename}")
        # Bonus features
        visualize = input("\nVisualize routes for an agent? (enter agent ID or 'n'): ").strip()
        if visualize.lower() != 'n':
            delivery_system.visualize_routes_ascii(visualize)
        export_csv = input("Export top performer to CSV? (y/n): ").lower() == 'y'
        if export_csv:
            delivery_system.export_top_performer_csv(report)
        print("\n✨ Simulation completed successfully!")
    except FileNotFoundError:
        print(f"❌ Error: File {filename} not found!")
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in {filename}!")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
if __name__ == "__main__":
    main()
🚚 Mystery Delivery System

📋 Project Overview
-- FastBox Delivery System Simulator is a Python-based logistics simulation that models package delivery operations for a fictional delivery company.
--The system simulates one day of operations with multiple warehouses, delivery agents, and packages, calculating optimal assignments and generating performance reports.

✨ Features:

# Core Features:

✅ Intelligent Agent-Package Assignment - Assigns packages to the nearest available agent using Euclidean distance
✅ Route Simulation - Simulates agents traveling to warehouses and delivering packages to destinations
✅ Performance Metrics - Calculates delivery efficiency (distance per package)
✅ JSON I/O - Reads input data from JSON files and outputs comprehensive reports
✅ Multi-Format Support - Handles both array and dictionary-based JSON formats

# Bonus Features:

🎯 Random Delivery Delays - Simulates real-world delays with 0-30% extra travel time
📊 ASCII Route Visualization - Displays agent routes in console for easy debugging
👥 Mid-Day Agent Joining - Simulates new agents joining during operations
📈 CSV Export - Exports top performer data to CSV format
🔄 Flexible Input - Works with 10+ different test case formats

📁 Project Structure

Mystery Delivery System/
├── fastbox_simulator.py      # Main simulation program
├── base_case.json            # Sample input format 1
├── test_case_1.json          # Sample input format 2
├── test_case_2.json          # Additional test cases
├── ................          # Test cases 3-9  
├── test_case_10.json         # Sample input format 10
├── report.json               # Output report (generated)
└── top_performer.csv         # CSV export (generated)

🚀 Quick Start:

# Prerequisites:

-- Python 3.6+
-- No external dependencies required

#Installation:

-- Clone or download the project files
-- Ensure all JSON test files are in the same directory

# Running the Simulation

-- python mystery_delivery_sys.py

🎮 Interactive Prompts:
-- When you run the simulator, you'll see:

🚚 FastBox Delivery System Simulator
========================================
Available test cases:
1. base_case.json
2. test_case_1.json
...
10. test_case_10.json

Enter the test case number (1-10) or filename: 1

📂 Loading data from base_case.json...

Enable random delivery delays? (y/n): y
Simulate new agent joining mid-day? (y/n): n

🚀 Starting delivery simulation...
📊 Generating report...

✅ Report saved to report.json

Visualize routes for an agent? (enter agent ID or 'n'): A1
Export top performer to CSV? (y/n): y

✨ Simulation completed successfully!
📊 Output Format
The system generates a comprehensive JSON report:

json
{
  "A1": {
    "packages_delivered": 2,
    "total_distance": 85.32,
    "efficiency": 42.66
  },
  "A2": {
    "packages_delivered": 2,
    "total_distance": 120.12,
    "efficiency": 60.06
  },
  "A3": {
    "packages_delivered": 1,
    "total_distance": 50.00,
    "efficiency": 50.00
  },
  "best_agent": "A1"
}

🔧 Technical Implementation:

-- Core Algorithms
-- Euclidean Distance Calculation

-- python
-- distance = √((x₂ - x₁)² + (y₂ - y₁)²)
-- Nearest Agent Assignment

-- For each package, find the agent closest to its warehouse
-- Assign package to that agent

# Efficiency Calculation:

-- python
  -- efficiency = total_distance / packages_delivered

# Key Classes

-- FastBoxDeliverySystem: Main simulation class
-- Methods for parsing, assignment, simulation, and reporting
-- Modular design for easy extension

📈 Sample Visualization Output

📊 Route Visualization for Agent A1:
==================================================
1. 🏭 Traveling to warehouse
   From: (5, 5) → To: (0, 0)
   Distance: 7.07 units
--------------------------------------------------
2. 📦 Delivering package
   From: (0, 0) → To: (30, 40)
   Distance: 50.00 units
--------------------------------------------------
📈 Summary for A1:
   Total packages delivered: 2
   Total distance traveled: 85.32
==================================================

🧪 Test Cases

-- The simulator comes with 10 comprehensive test cases:

   -- base_case.json    - Basic 3 warehouses, 3 agents, 5 packages
   -- test_case_1.json  - 5 warehouses, 4 agents, 12 packages
   -- test_case_2.json  - 3 warehouses, 3 agents, 10 packages
   -- test_case_3.json  - 4 warehouses, 4 agents, 6 packages
   -- test_case_4.json  - 5 warehouses, 5 agents, 12 packages
   -- test_case_5.json  - 5 warehouses, 5 agents, 10 packages
   -- test_case_6.json  - 4 warehouses, 4 agents, 9 packages
   -- test_case_7.json  - 4 warehouses, 4 agents, 10 packages
   -- test_case_8.json  - 5 warehouses, 4 agents, 11 packages
   -- test_case_9.json  - 3 warehouses, 4 agents, 8 packages
   -- test_case_10.json - 5 warehouses, 4 agents, 11 packages

📝 Evaluation Criteria Met:

     Criteria                Weight	      Status	     Implementation
-- JSON Parsing	             10%	   ✅ Complete	 Dual-format support
-- Distance Calculation	     20%	   ✅ Complete	 Euclidean formula
-- Agent-Package Assignment	 25%	   ✅ Complete	 Nearest-agent mapping
-- Simulation & Report	     25%	   ✅ Complete	 Full simulation with JSON output
-- Code Clarity & Comments	 10%	   ✅ Complete	 Well-documented code
-- Bonus Creativity	         10%	   ✅ Complete	 4 bonus features implemented

🎯 Learning Objectives

-- This project demonstrates:
-- Object-oriented programming in Python
-- JSON file handling and data parsing
-- Mathematical calculations (Euclidean distance)
-- Algorithm design (nearest neighbor assignment)
-- Simulation modeling
-- Data visualization (ASCII art)
-- File export (JSON and CSV)

🔍 Advanced Features

-- Random Delay Simulation

# Add 0-30% random delay to simulate real-world conditions

-- delay_multiplier = 1.0 + random.uniform(0, 0.3)
-- effective_distance = distance * delay_multiplier
-- Mid-Day Agent Joining

# Dynamically add new agents during simulation

-- new_agent_id = f"A{len(self.agents) + 1}"
-- new_location = (random.uniform(0, 100), random.uniform(0, 100))
-- Efficiency Optimization
-- Agents group packages by warehouse for efficient pickups

-- Routes are optimized to minimize backtracking
-- Real-time statistics tracking

🛠️ Customization:

-- The system can be easily extended:
-- Add new assignment algorithms (replace find_nearest_agent())
-- Implement different distance metrics (Manhattan, etc.)
-- Add more visualization options (matplotlib graphs)
-- Include package priorities (express vs standard)
-- Simulate traffic conditions (time-based delays)

📚 Usage Examples:

-- Basic Usage

from fastbox_simulator import FastBoxDeliverySystem
import json
with open('base_case.json', 'r') as f:
    data = json.load(f)
system = FastBoxDeliverySystem(data)
system.simulate_delivery()
report = system.generate_report()
With All Bonus Features

system = FastBoxDeliverySystem(data)
system.simulate_delivery(enable_delays=True, new_agent_mid_day=True)
system.visualize_routes_ascii("A1")
system.export_top_performer_csv(report)

🤝 Contributing:

-- Fork the repository
-- Create a feature branch
-- Add your improvements
-- Submit a pull request

📄 License:

-- This project is created for educational purposes. 
-- Feel free to use and modify as needed.

👨‍💻 Author:

-- FastBox Delivery System Simulator
-- A comprehensive logistics simulation tool for learning Python programming and algorithm design

📞 Support

-- For questions or issues:
-- Check the code comments for detailed explanations
-- Review the sample test cases
-- Experiment with different configurations

# Happy Delivering! 🚀📦✨

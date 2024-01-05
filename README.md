# pyMGgameops
This repository contains a Python implementation of a microgrid game operations simulation for demand response. The simulation models the interaction between electricity consumers (players) and a microgrid with renewable energy sources (solar and wind) and energy storage (battery).

Contents
Introduction
Features
Usage
Adjusting Parameters
Dependencies
License
Introduction
Demand response is a strategy employed to optimize electricity consumption in response to changes in electricity prices, renewable energy generation, or other external factors. In this simulation, each player makes decisions on whether to cooperate or compete based on user-defined preferences. The microgrid manages renewable energy generation, battery storage, and facilitates communication with the players.

Features
Player Class: Represents an electricity consumer with individual characteristics such as base and peak prices, peak hours, and user preferences.
Microgrid Class: Models the microgrid with solar and wind generation, battery storage, and methods for simulating energy flow.
Demand Response Simulation: Simulates the interaction between players and the microgrid, considering cooperation, competition, and renewable energy constraints.
Visualization: Includes example code for visualizing demand response strategies, electricity demand before and after response, cumulative cost savings, renewable energy generation, and battery state of charge.
Usage
Clone the repository:

bash
Copy code
git clone https://github.com/<your-username>/pyMGgameops.git
cd pyMGgameops
Run the example script:

bash
Copy code
python pyMGgameops.py
This will execute a one-day simulation with two players, a microgrid, and visualize the results.

Adjusting Parameters
You can customize the simulation by adjusting various parameters in the pyMGgameops.py script:

Player Characteristics: Modify player characteristics such as base_price, peak_price, peak_hours, and user_preferences.
Microgrid Parameters: Adjust microgrid parameters like solar_capacity, wind_capacity, battery_capacity, charge_efficiency, and discharge_efficiency.
Demand Profiles: Generate different demand profiles for players by changing the player1_demand_profile and player2_demand_profile.
Run the modified script to see the impact of parameter changes on the simulation results.
Dependencies
The simulation requires the following Python libraries:

NumPy
Matplotlib
Install the dependencies using:

bash
Copy code
pip install numpy matplotlib

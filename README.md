# pyMGgameops V1.0

## Overview

Microgrid Game Operations is a Python implementation of a microgrid game operations simulation for demand response. The simulation models the interaction between electricity consumers (players) and a microgrid with renewable energy sources (solar and wind) and energy storage (battery).

## Features

- **Player Class**: Represents an electricity consumer with individual characteristics such as base and peak prices, peak hours, and user preferences.
- **Microgrid Class**: Models the microgrid with solar and wind generation, battery storage, and methods for simulating energy flow.
- **Demand Response Simulation**: Simulates the interaction between players and the microgrid, considering cooperation, competition, and renewable energy constraints.
- **Visualization**: Includes example code for visualizing demand response strategies, electricity demand before and after response, cumulative cost savings, renewable energy generation, and battery state of charge.

## Script Components

The primary components of the simulation script (`pyMGgameops.py`) include:

- **Player Characteristics Configuration**: Modify player characteristics such as `base_price`, `peak_price`, `peak_hours`, and `user_preferences`.
- **Microgrid Parameters Configuration**: Adjust microgrid parameters like `solar_capacity`, `wind_capacity`, `battery_capacity`, `charge_efficiency`, and `discharge_efficiency`.
- **Demand Profile Generation**: Generate different demand profiles for players by changing the `player1_demand_profile` and `player2_demand_profile`.
- **Simulation Execution**: Run the simulation script to observe one-day simulation results with two players, a microgrid, and visualization of key metrics.


## How to Use

1. **Requirements:**
   - Python (3.x recommended)

2. **Run the Simulation:**
   - Modify the script parameters as needed.
   - Run the script:
     ```bash
     pyMGgameops.py
     ```

## Adjusting Parameters

Customize the simulation by adjusting various parameters in the pyMGgameops.py script:

Player Characteristics: Modify player characteristics such as base_price, peak_price, peak_hours, and user_preferences.
Microgrid Parameters: Adjust microgrid parameters like solar_capacity, wind_capacity, battery_capacity, charge_efficiency, and discharge_efficiency.
Demand Profiles: Generate different demand profiles for players by changing the player1_demand_profile and player2_demand_profile.

## Results

Review the generated plots to understand the demand response strategies, electricity demand variations, cost savings, renewable energy generation, and battery state of charge.

## Dependencies

- `matplotlib`
- `numpy`

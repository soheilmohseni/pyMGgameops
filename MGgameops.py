"""
@author: Dr Soheil Mohseni

"""

import numpy as np
import matplotlib.pyplot as plt

class Player:
    def __init__(self, id, base_price, peak_price, peak_hours, user_preferences):
        self.id = id
        self.base_price = base_price
        self.peak_price = peak_price
        self.peak_hours = peak_hours
        self.user_preferences = user_preferences
        self.original_demand = None

    def get_hourly_price(self, hour):
        return self.peak_price if hour in self.peak_hours else self.base_price

    def decide_strategy(self, hour):
        cooperation_threshold = self.user_preferences.get("cooperation_probability", 0.5)
        return "cooperate" if np.random.rand() < cooperation_threshold else "compete"

    def simulate_demand_response(self, demand, hour, opponent_demand, renewable_generation, battery_soc):
        price = self.get_hourly_price(hour)
        strategy = self.decide_strategy(hour)

        if strategy == "cooperate":
            new_demand = self.calculate_cooperative_demand(demand, opponent_demand, renewable_generation, battery_soc)
        else:
            new_demand = self.calculate_competitive_demand(demand, renewable_generation, battery_soc)

        cost_savings = (demand - new_demand) * price
        return new_demand, cost_savings, strategy

    def calculate_cooperative_demand(self, demand, opponent_demand, renewable_generation, battery_soc):
        reduction_factor = self.user_preferences.get("cooperative_reduction_factor", 0.3)
        max_cooperative_demand = min(demand, opponent_demand, renewable_generation + battery_soc)
        reduced_demand = max(0, max_cooperative_demand - int(max_cooperative_demand * reduction_factor))
        return min(demand, reduced_demand)

    def calculate_competitive_demand(self, demand, renewable_generation, battery_soc):
        reduction_factor = self.user_preferences.get("competitive_reduction_factor", 0.2)
        max_competitive_demand = min(demand, renewable_generation + battery_soc)
        reduced_demand = max(0, max_competitive_demand - int(max_competitive_demand * reduction_factor))
        return min(demand, reduced_demand)

class Microgrid:
    def __init__(self, solar_capacity, wind_capacity, battery_capacity, charge_efficiency, discharge_efficiency):
        self.solar_capacity = solar_capacity
        self.wind_capacity = wind_capacity
        self.battery_capacity = battery_capacity
        self.charge_efficiency = charge_efficiency
        self.discharge_efficiency = discharge_efficiency
        self.solar_generation = np.zeros(24)
        self.wind_generation = np.random.uniform(0, self.wind_capacity, 24)
        self.battery_soc = 0

    def generate_energy(self):
        # Simulate solar generation with a typical daily profile
        solar_profile = 0.5 * np.sin((np.arange(24) - 6) * np.pi / 12) + 0.5
        self.solar_generation = solar_profile * self.solar_capacity

    def simulate_one_hour(self, total_demand, players, hour):
        self.generate_energy()

        renewable_generation = self.solar_generation[hour] + self.wind_generation[hour]

        max_charge_capacity = min(self.battery_capacity - self.battery_soc, renewable_generation)
        charging_power = max_charge_capacity * self.charge_efficiency
        self.battery_soc = min(self.battery_capacity, self.battery_soc + charging_power)

        total_cost_savings = 0

        for player in players:
            player_demand, cost_savings, strategy = player.simulate_demand_response(player.original_demand[hour], hour, total_demand // len(players), renewable_generation, self.battery_soc)
            total_cost_savings += cost_savings

            print(f"Hour {hour + 1} - Player {player.id}: Demand (kWh) = {player_demand:.2f}, Cost Savings ($) = {cost_savings:.2f}, Strategy = {strategy}")

            # Update player's original demand with the new demand for future calculations
            player.original_demand[hour] = player_demand

        demand_exceeds_renewable = total_demand > renewable_generation

        if demand_exceeds_renewable:
            max_discharge_capacity = min(self.battery_soc, total_demand - renewable_generation)
            discharging_power = max_discharge_capacity * self.discharge_efficiency
            self.battery_soc = max(0, self.battery_soc - discharging_power)

        print(f"Hour {hour + 1} - Renewable Generation: Solar (kWh) = {self.solar_generation[hour]:.2f}, Wind (kWh) = {self.wind_generation[hour]:.2f}")
        print(f"Hour {hour + 1} - Battery State of Charge (kWh): {self.battery_soc:.2f}")
        print(f"Hour {hour + 1} - Total Cost Savings ($): {total_cost_savings:.2f}")

# Example usage with a microgrid, players, solar PV, wind, and a battery
solar_capacity = 50
wind_capacity = 30
battery_capacity = 100
charge_efficiency = 0.9
discharge_efficiency = 0.9

# Generate random demand profiles for players 1 and 2
player1_demand_profile = np.random.uniform(20, 50, 24)
player2_demand_profile = np.random.uniform(20, 50, 24)

player1_preferences = {"cooperation_probability": 0.6, "cooperative_reduction_factor": 0.3, "competitive_reduction_factor": 0.2}
player2_preferences = {"cooperation_probability": 0.5, "cooperative_reduction_factor": 0.2, "competitive_reduction_factor": 0.3}

player1 = Player(id=1, base_price=0.1, peak_price=0.2, peak_hours=[16, 17, 18], user_preferences=player1_preferences)
player1.original_demand = player1_demand_profile.copy()

player2 = Player(id=2, base_price=0.1, peak_price=0.2, peak_hours=[16, 17, 18], user_preferences=player2_preferences)
player2.original_demand = player2_demand_profile.copy()

microgrid = Microgrid(solar_capacity, wind_capacity, battery_capacity, charge_efficiency, discharge_efficiency)

# Simulate demand response for one day
total_demand = np.sum(player1_demand_profile) + np.sum(player2_demand_profile)
players = [player1, player2]

time_steps = list(range(24))
strategy_data = [[] for _ in players]
before_dr_demand_data = [[] for _ in players]
after_dr_demand_data = [[] for _ in players]
cost_savings_data = [[] for _ in players]
cumulative_cost_savings_data = [[] for _ in players]
solar_generation_data = []
wind_generation_data = []
battery_soc_data = []

for hour in range(24):
    microgrid.simulate_one_hour(total_demand, players, hour)

    # Store data for plotting
    solar_generation_data.append(microgrid.solar_generation[hour])
    wind_generation_data.append(microgrid.wind_generation[hour])
    battery_soc_data.append(microgrid.battery_soc)

    for i, player in enumerate(players):
        after_dr_demand, cost_savings, _ = player.simulate_demand_response(player.original_demand[hour], hour, total_demand // len(players), microgrid.solar_generation[hour] + microgrid.wind_generation[hour], microgrid.battery_soc)
        strategy_data[i].append(1 if player.decide_strategy(hour) == "cooperate" else 0)
        before_dr_demand_data[i].append(player.original_demand[hour])
        after_dr_demand_data[i].append(after_dr_demand)
        cost_savings_data[i].append(cost_savings)
        cumulative_cost_savings_data[i].append(cumulative_cost_savings_data[i][-1] + cost_savings if cumulative_cost_savings_data[i] else cost_savings)

# Plotting
plt.figure(figsize=(12, 16))

# Plot 1: Demand Response Strategies Over Time
plt.subplot(4, 2, 1)
for i, player in enumerate(players):
    plt.plot(time_steps, strategy_data[i], label=f'Player {player.id}')
plt.title('Demand Response Strategies Over Time')
plt.xlabel('Hour')
plt.ylabel('Cooperate (1) / Compete (0)')
plt.legend()

# Plot 2: Player 1 Electricity Demand Before Demand Response
plt.subplot(4, 2, 2)
plt.plot(time_steps, before_dr_demand_data[0], label=f'Player 1 - Before DR')
plt.plot(time_steps, after_dr_demand_data[0], linestyle='--', label='Player 1 - After DR')
plt.title('Player 1 Electricity Demand Before and After Demand Response')
plt.xlabel('Hour')
plt.ylabel('Demand (kWh)')
plt.legend()

# Plot 3: Player 2 Electricity Demand Before Demand Response
plt.subplot(4, 2, 3)
plt.plot(time_steps, before_dr_demand_data[1], label=f'Player 2 - Before DR')
plt.plot(time_steps, after_dr_demand_data[1], linestyle='--', label='Player 2 - After DR')
plt.title('Player 2 Electricity Demand Before and After Demand Response')
plt.xlabel('Hour')
plt.ylabel('Demand (kWh)')
plt.legend()

# Plot 4: Cumulative Cost Savings Over Time
plt.subplot(4, 2, 4)

# Calculate the total cost savings for both players
grand_total_cost_savings = np.sum(cumulative_cost_savings_data, axis=0)

# Plot the grand total cost savings with a dashed line
plt.plot(time_steps, grand_total_cost_savings, label='Grand Total')

plt.title('Cumulative Cost Savings Over Time')
plt.xlabel('Hour')
plt.ylabel('Cumulative Cost Savings ($)')
plt.legend()

# Plot 5: Renewable Energy Generation Over Time
plt.subplot(4, 2, 5)
plt.plot(time_steps, solar_generation_data, label='Solar')
plt.plot(time_steps, wind_generation_data, label='Wind')
plt.title('Renewable Energy Generation Over Time')
plt.xlabel('Hour')
plt.ylabel('Generation (kWh)')
plt.legend()

# Plot 6: Battery State of Charge Over Time
plt.subplot(4, 2, 6)
plt.plot(time_steps, battery_soc_data)
plt.title('Battery State of Charge Over Time')
plt.xlabel('Hour')
plt.ylabel('State of Charge (kWh)')

plt.tight_layout()

# Uncomment the line below if you are using an IDE that doesn't automatically show plots
# plt.show()



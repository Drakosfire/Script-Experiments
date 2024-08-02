import numpy as np
import matplotlib.pyplot as plt

# Initial parameters
initial_population = 1000
years = 207

# Growth rates and mortality rates per phase
phases = {
    "Phase 1": {"start": 0, "end": 50, "growth_rate": 0.02, "mortality_rate": 0.05},
    "Phase 2": {"start": 50, "end": 100, "growth_rate": 0.03, "mortality_rate": 0.02},
    "Phase 3": {"start": 100, "end": 150, "growth_rate": 0.05, "mortality_rate": 0.01},
    "Phase 4": {"start": 150, "end": 200, "growth_rate": 0.03, "mortality_rate": 0.01},
    "Phase 5": {"start": 200, "end": 207, "growth_rate": 0.03, "mortality_rate": 0.01},
}

# Population array to store population for each year
population = np.zeros(years)
population[0] = initial_population

# Function to calculate population growth
def calculate_population_growth(population, growth_rate, mortality_rate, migration=0):
    return population * (1 + growth_rate - mortality_rate) + migration

# Simulate population growth
for year in range(1, years):
    for phase, details in phases.items():
        if details["start"] <= year < details["end"]:
            # Adjust migration for specific years (internal migration)
            migration = 0
            if year == 125:  # Arboreal Titan migration
                population[year - 1] *= 0.95  # 5% population reduction due to disruption
            # Adjust population growth due to significant events
            if year == 75:  # Plague year
                population[year - 1] *= 0.8  # 20% population reduction
            population[year] = calculate_population_growth(population[year - 1], details["growth_rate"], details["mortality_rate"], migration)
            break

# Extracting the population for the year 207
population_207 = population[206]

# Output the population in the year 207
print(f"Population in the year 207: {population_207}")

# Plotting the population growth curve
plt.figure(figsize=(10, 6))
plt.plot(range(years), population, label="Population Growth", color="b")
plt.title("Population Growth of Mirathorn Over 207 Years")
plt.xlabel("Years")
plt.ylabel("Population")
plt.grid(True)
plt.legend()
plt.show()

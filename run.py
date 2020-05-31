from person import Person
from model import *


scale_factor = 0.001
area = 242495  # km2 uk
side = int(math.sqrt(area)) # 492

def lockdown_policy(infected, deaths, population_size):
    """Given infected and deaths over time (lists)
    determine for how long we should declare a national lockdown.
    0 means we don't declare lockdown.
    """
    if (max(infected[-20:]) / population_size) > 0.2:
        return 21 * 12
    return 0

sim_params = {
    'grid_x': side,
    'grid_y': side,
    'density': 259 * scale_factor, # population density uk,
    'initial_infected': 0.05,
    'infect_rate': 0.1,
    'recovery_period': 14 * 12,
    'critical_rate': 0.15,
    'hospital_capacity_rate': .02,
    'active_ratio': 8 / 24.0,
    'immunity_chance': 1.0,
    'quarantine_rate': 0.6,
    'lockdown_policy': lockdown_policy,
    'cycles': 200 * 12,
    'hospital_period': 21 * 12,
}

model = Simulation(sim_params)
cycles_to_run = sim_params.get('cycles')
print(sim_params)
for current_cycle in range(cycles_to_run):
    model.step()
    if (current_cycle % 10) == 0:
        live_plot(model.datacollector.model_vars)

print('Total deaths: {}'.format(
    model.datacollector.model_vars['Deaths'][-1]
))


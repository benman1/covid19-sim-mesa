from numba import jit
from mesa import Model
from mesa.time import RandomActivation
from person import Person
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import matplotlib.pyplot as plt


@jit(nopython=False)
def active_cases(model):
    return sum([
        1
        for agent in model.schedule.agents
        if agent.infected
    ])


@jit(nopython=False)
def total_hospitalized(model):
    return sum([
        1
        for agent in model.schedule.agents
        if agent.hospitalized
    ])


@jit(nopython=False)
def total_deaths(model):
    return sum([
        1
        for agent in model.schedule.agents
        if not agent.alive
    ])


@jit(nopython=False)
def total_immune(model):
    return sum([
        1
        for agent in model.schedule.agents
        if agent.immune
    ])


@jit(nopython=False)
def get_hospital_takeup(model):
    """are there free hospital beds? show big spike!"""
    return model.hospital_takeup * model.num_agents


@jit(nopython=False)
def get_lockdown(model):
    """Are we in lockdown? Show big spike"""
    return (model.lockdown > 0) * 6000


class Simulation(Model):
    """A model with agents."""
    def __init__(self, params, seed=None):
        #self.num_agents = params.get('num_persons')
        self.num_agents = int(
            params.get('density')
            * params.get('grid_x')
            * params.get('grid_y')
        )
        self.grid = MultiGrid(
            params.get('grid_x'),
            params.get('grid_y'),
            True
        )
        self.schedule = RandomActivation(self)
        self.start_infected = params.get('initial_infected')
        self.recovery_period = params.get('recovery_period')
        self.infect_rate = params.get('infect_rate')
        self.critical_rate = params.get('critical_rate') / self.recovery_period
        self.free_beds = int(
            params.get('hospital_capacity_rate')
            * self.num_agents
            * 0.2
        )# free beds
        self.hospital_takeup = True  # are hospitals at capacity?
        self.active_ratio = params.get('active_ratio')
        self.immunity_chance = params.get('immunity_chance')
        self.quarantine_rate = params.get('quarantine_rate') / self.recovery_period
        self.lockdown_policy = params.get('lockdown_policy')
        self.lockdown = False
        self.hospital_period = params.get('hospital_period')
        self.hospital_factor = 0.2  # less likely to die in hospital
        print(f'Free beds in the hospital: {self.free_beds}')
        print(f'Population: {self.num_agents}')

        self.running = True
        self.current_cycle = 0
        self.create_agents()
        self.set_reporters()

    def create_agents(self):
        """Create agents"""
        for i in range(self.num_agents):
            a = Person(i, self)
            if self.random.random() < self.start_infected:
                a.set_infected()
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def set_reporters(self):
        self.datacollector = DataCollector(
            model_reporters={
                'Active Cases': active_cases,
                'Deaths': total_deaths,
                'Immune': total_immune,
                'Hospitalized': total_hospitalized,
                #'Hospital_capacity': get_hospital_takeup,
                'Lockdown': get_lockdown,
            })

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.hospital_takeup = self.datacollector.model_vars[
            'Hospitalized'
        ][-1] < self.free_beds
        self.schedule.step()
        if self.lockdown:
            # count down
            self.lockdown -= 1
        else:
            self.lockdown =  self.lockdown_policy(
                self.datacollector.model_vars['Active Cases'],
                self.datacollector.model_vars['Deaths'],
                self.num_agents
            )
        self.current_cycle += 1

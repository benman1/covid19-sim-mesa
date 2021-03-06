from mesa import Agent
import numpy as np

class Person(Agent):
    """An agent with fixed initial health and quarantine status."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = True
        self.infected = False
        self.hospitalized = False
        self.immune = False
        self.quarantined = False  # self quarantine
        self.time_infected = 0

    def move_to_next(self):
        """Move to next adjacent cell"""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def set_infected(self):
        """Person set as infected if not immune"""
        if not self.immune:
            self.infected = True
            self.time_infected = 0

    def infect_others(self):
        """Infect others in same cell based on infection rate"""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for cellmate in cellmates:
                if self.random.random() < self.model.infect_rate:
                    cellmate.set_infected()

    def while_infected(self):
        """While infected, infect others, see if die from infection or recover"""
        self.time_infected += 1
        if self.hospitalized:
            # stay in bed. do nothing; maybe die
            if self.random.random() < self.model.die_in_hospital_rate:
                self.die()
                return
            self.hospitalized -= 1
            if not self.hospitalized:
                self.recover()
                return
        if self.random.random() < self.model.quarantine_rate:
            self.quarantined = True
        if self.time_infected < self.model.recovery_period:
            if self.random.random() < self.model.critical_rate:
                if self.model.hospital_takeup:
                    self.hospitalized = self.model.hospital_period
                    self.quarantined = True
                else:
                    self.die()
        else:
            self.recover()

    def move(self):
        # If a person is infected
        if self.infected:
            self.while_infected()
            # Move to a new position if not in quarantine or staying in place
            if not (self.quarantined or self.model.lockdown):
                self.infect_others()  # infect others in same cell
        if not (self.quarantined or self.model.lockdown):
            self.move_to_next()

    def recover(self):
        """person has passed the recovery period so no longer infected."""
        self.infected = False
        self.quarantined = False
        self.time_infected = 0
        if self.random.random() < self.model.immunity_chance:
            self.immune = True

    def die(self):
        """Person dies from infection"""
        self.alive = False
        self.hospitalized = False
        self.quarantined = False
        self.infected = False

    def step(self):
        if self.alive:
            self.move()

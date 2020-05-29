from mesa import Agent
import numpy as np

class Person(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = True
        self.infected = False
        self.hospitalized = False
        self.immune = False
        self.in_quarantine = False  # self quarantine
        self.time_infected = 0

    def move_to_next(self):
        ''' Move to next adjacent cell '''
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def set_quarantine(self):
        ''' Person has been infected and in quarantine '''
        self.in_quarantine = True

    def set_infected(self):
        ''' Person set as infected if not immune '''
        if not self.immune:
            self.infected = True
            self.time_infected = 0

    def infect_others(self):
        ''' Infect others in same cell based on infection rate '''
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for cellmate in cellmates:
                if self.random.random() < self.model.infect_rate:
                    cellmate.set_infected()

    def while_infected(self):
        ''' While infected, infect others, see if die from infection or recover '''
        self.time_infected += 1
        if self.hospitalized:
            # stay in bed. do nothing; maybe die
            if self.random.random() < (
                    self.model.critical_rate *
                    self.model.hospital_factor
            ):
                self.alive = False
                self.hospitalized = False
                self.infected = False
                return
            self.hospitalized - 1
            return
        if self.random.random() < (self.model.quarantine_rate / self.model.recovery_period):
            self.set_quarantine()
        if not self.in_quarantine:
            self.infect_others()  # infect others in same cell
        if self.time_infected < self.model.recovery_period:
            if self.random.random() < self.model.critical_rate:
                if self.model.hospital_takeup:
                    self.hospitalized = self.model.hospital_period
                    self.set_quarantine()
                else:
                    self.alive = False  # person died from infection
                    self.infected = False
        else:  # person has passed the recovery period so no longer infected
            self.infected = False
            self.quarantine = False
            if self.random.random() < self.model.immunity_chance:
                self.immune = True

    def move(self):
        # Move to a new position if not in quarantine or staying in place
        if self.in_quarantine or self.model.lockdown:
            pass
        else:
            self.move_to_next()
        # If a person is infected
        if self.infected:
            self.while_infected()

    def step(self):
        if self.alive:
            self.move()

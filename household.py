import random
import numpy as np

# Properties:
#   A) Power (production)
#   B) Power (consumption)
#   C) Storage (total capacity)
#   D) Storage (capacity used)
#                  0,1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,16, 17,18,19,20, 21,22,23
power_cons_rate = [0.020444838,0.019947656,0.019037708,0.017077946,0.01655477,0.01611958,0.015475257,0.015288126,0.016532257,0.016002537,0.016663428,0.016531193,0.017324408,0.016847986,0.016691198,0.016650697,0.016736932,0.016514935,0.017412728,0.017562819,0.017837759,0.019147254,0.02041525,0.02078909] #rate of consumption (kW used per household)
power_cons_rate = [n*1000 for n in power_cons_rate]
power_prod_rate = [0.0000100031,0.00000756331,0.00000685355,0.0000066983,0.00000565585,0.00000538969,0.00000510135,0.00000474647,0.00000465775,0.00000339351,0.001094572,0.00401636,0.005363649,0.005977164,0.006284664,0.006376378,0.006422977,0.006185765,0.006015557,0.005603922,0.004832465,0.002998618,0.000425896,0.000209887] #rate of production (kW produced per household)
power_prod_rate = [0,0,0,0, 0,0,0.00000510135,0.00000474647,0.00000465775,0.00000339351,0.001094572,0.00401636,0.005363649,0.005977164,0.006284664,0.006376378,0.006422977,0.006185765,0.006015557,0.005603922,0,0,0,0] #rate of production (kW produced per household)
power_prod_rate = [n*1000 for n in power_prod_rate]

total_households = 1#502870         #number of total households in california

class Household:

    # parameterized constructor
    # def __init__(self, prod_percentage, powerP, powerC, storeC, storeU):
    def __init__(self, producer, storeC, prod_percentage):
        self.power_production = 0
        self.power_consumption = 0
        self.storage_capacity = 0
        self.storage_used = 0

        #setup producing & consuiming
        self.producer = producer
        if self.producer:
            self.production_rate = [i/(total_households*prod_percentage)*np.random.normal(2.577831,6.53793,1)[0] for i in power_prod_rate]
            self.storage_capacity = storeC
            self.storage_used = self.storage_capacity*random.uniform(0, 0.5)
        else:
            self.production_rate = [0 for i in range(24)]
        self.usage_rate = [(i/total_households)*np.random.normal(17.483598,2.455371,1)[0] for i in power_cons_rate]
        self.max_cons_hour = self.usage_rate.index(max(self.usage_rate))

        #totals per day
        # self.power_consumption = powerC     # set
        self.hour = 0

    def get_produciton(self):
        return self.production_rate[self.hour]

    def get_consumption(self):
        return self.usage_rate[self.hour]

    def get_SC(self):
        self.storage_capacity

    def get_storage_used(self):
        return self.storage_used

    #determine how much to charge the battery
    #solar_power = how much power available to charge
    #retuns = left over power after charging
    def charge_battery(self, solar_power):
        if solar_power == 0:
            return 0

        left = self.storage_capacity - self.storage_used        #find availabe capacity
        # print("BATT ", self.storage_capacity, "-", self.storage_used, "=",  left)
        if left>0:                                              #if battery !full
            if left >= solar_power:                              #if generated power < battery capacity left
                self.storage_used += solar_power                #dump full amount in battery
                return 0
            else:                                                #if there isnt enough capacity left
                self.storage_used += (solar_power-left)         #charge up to max
                return -1*(left-solar_power)                    #return the rest
        return solar_power

    #steps time forward 1 hr
    #returns (demand, net demand, produced, stored)
    def step(self):
        self.hour = (self.hour+1)%24
        demand = self.get_consumption()*random.uniform(0.6,1.4)
        produced = self.get_produciton()*random.uniform(0.7,1.3)
        leftover = self.charge_battery(produced)
        stored = self.get_storage_used()

        net_demand = demand

        if leftover > 0:
            net_demand -= leftover

        # print(demand, net_demand, stored)
        if(((self.hour>20) or (self.hour<8)) and (stored>0)):
            if(stored>=net_demand):
                net_demand = 0
                self.storage_used -= net_demand
            else:
                # net_demand -= stored
                # self.storage_used = 0
                usable_power = self.storage_capacity/2
                net_demand -= min(stored, usable_power)
                self.storage_used = self.storage_used-min(stored, usable_power)



        return (demand, net_demand, produced, stored)

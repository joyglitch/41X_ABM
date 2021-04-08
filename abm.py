from household import *
import random
import matplotlib.pyplot as plt

time_step = 1                              #hourly rate
num_days = 1                               #number of days of simulation

num_agents = 1502870                        #number of residential households
percent_solargen = 1                       #percentage of the population with solar panels + batteries
percent_no_solargen = 1 - percent_solargen  #percentage of the population without solar panels + batteries
average_storage_capacity = 9.95               #this will be in killiwatt hours

agents = []
demand_list = []
net_demand_list = []
production_list = []
storage_list = []
time_step_list = [0]


for i in range(num_agents):                                     #generate all agents
    storage_cap = average_storage_capacity*random.uniform(0.5, 1.5)
    producer = random.random()<=percent_solargen
    agents.append(Household(producer, storage_cap, percent_solargen))
print(str(num_agents) + " Agents Created")

total_steps = round((num_days*24)/time_step)
for i in range(total_steps):
    tempD=0
    tempN=0
    tempP=0
    tempS=0
    for agent in agents:                                        #step though 1 agent 1 hour
        demand, net_demand, produced, stored = agent.step()
        tempD+=demand                                           #add all agent's hourly stats together
        tempN+=net_demand
        tempP+=produced
        tempS+=stored
        # print(demand, net_demand, produced, stored)

    demand_list.append(tempD)                                   #make a list of all hourly stats
    net_demand_list.append(tempN)
    production_list.append(tempP)
    storage_list.append(tempS)
    # print(time_step_list[-1])
    time_step_list.append(time_step_list[-1]+1)

# fig=plt.figure()
# ax=fig.add_axes([0,0,1,1])
time_step_list = time_step_list[:-1]
plt.plot(time_step_list, demand_list, '-r')
plt.plot(time_step_list, net_demand_list, '-b')
plt.plot(time_step_list, production_list, '-y')
plt.plot(time_step_list, storage_list, '-g')
plt.legend(['Total Demand','Net Demand','Production','Storage'])
plt.title("California Energy Demand Over One Day")
plt.ylabel("Power (kWh)")
plt.xlabel("Time (hours)")
plt.show()

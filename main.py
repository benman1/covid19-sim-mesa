#! /bin/python3

if __name__ == "__main__":
    # execute only if run as a script
    from run import *

    model = Simulation(sim_params)
    current_cycle = 0
    cycles_to_run = sim_params.get('cycles')
    print(cycles_to_run)
    print(sim_params)
    while 1:
        model.step()
        if cycles_to_run > 0 and current_cycle >= cycles_to_run:
            break
        current_cycle += 1

    model_data = model.datacollector.get_model_vars_dataframe()
    model_data.plot()
    print(model_data)
    plt.show()

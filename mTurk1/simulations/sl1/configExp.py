import os
from mTurk1.python.database_functions import sim_path, agent_path, view_path



class ExperimentSettings:
    
    #Name the simulation
    sim_name='Simulation_constant_speed_1'
    #Name the experiment
    exp_name='Experiment_2'

    #Setup folder location
    setup_folder=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'setup_files'))

    sim1=sim_path(setup_folder,"sim_settings1.json")
    agent1=agent_path(setup_folder,"constant_speed_agents1.json")
    view1=view_path(setup_folder,"views_1.json")
    view2=view_path(setup_folder,"views_2.json")
    view3=view_path(setup_folder,"views_3.json")
    view4=view_path(setup_folder,"views_4.json")
    view5=view_path(setup_folder,"views_4.json")
    
    sim_list=[sim1]
    agent_list=[agent1]
    view_list=[view1,view2,view3,view4,view5]
    
    

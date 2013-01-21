import os
from mTurk1.python.database_functions import sim_path, agent_path, view_path



class ExperimentSettings:
    
    #Name the simulation
    sim_name='Simulation_0.1'
    #Name the experiment
    exp_name='experiment_1'

    #Setup folder location
    setup_folder=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'setup_files'))

    sim1=sim_path(setup_folder,"sim_settings_test_0.1.json")
    agent1=agent_path(setup_folder,"agent_settings_test_0.1.json")
    view1=view_path(setup_folder,"view_settings_test_0.1.json")
    view2=view_path(setup_folder,"view_settings_test_0.1.json")
    view3=view_path(setup_folder,"view_settings_test_0.1.json")
    view4=view_path(setup_folder,"view_settings_test_0.1.json")
    view5=view_path(setup_folder,"view_settings_test_0.1.json")
    view6=view_path(setup_folder,"view_settings_test_0.1.json")
    view7=view_path(setup_folder,"view_settings_test_0.1.json")
    view8=view_path(setup_folder,"view_settings_test_0.1.json")
    view9=view_path(setup_folder,"view_settings_test_0.1.json")
    view10=view_path(setup_folder,"view_settings_test_0.1.json")

    
    sim_list=[sim1]
    agent_list=[agent1]
    view_list=[view1,view2,view3,view4,view5,view6,view7,view8,view9,view10]
    
    
